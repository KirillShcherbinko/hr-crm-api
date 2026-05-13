from sqlalchemy.exc import IntegrityError
import logging
import uuid
import datetime
from sqlalchemy import func

from src.infrastructure.database.db import get_db
from src.infrastructure.database.db_sync import get_sync_session
from src.infrastructure.email.email_sync import send_email_sync
from .worker import celery_app

# Импорты ORM-моделей для аналитики
from src.infrastructure.database.models.vacancy import Vacancy, VacancyCandidate, VacancyAnalytics
from src.infrastructure.database.models.stage import VacancyStage, StageAnalytics, StageTransition
from src.infrastructure.database.models.user import RecruiterAnalytics


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, email: str, subject: str, body: str) -> None:
    """Отправка email кандидату с ретраями при падении SMTP."""
    try:
        send_email_sync(email, subject, body)
    except Exception as exc:
        self.retry(exc=exc)


# src/infrastructure/tasks/tasks.py
# ... остальные импорты моделей ...

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def recalculate_vacancy_analytics_task(self, vacancy_id: str) -> None:
    """Пересчёт агрегатов по вакансии: кол-во кандидатов, дни открытия."""
    try:
        vacancy_uuid = uuid.UUID(vacancy_id)

        with get_sync_session() as session:
            # ✅ 1. Защита от гонки условий / удаления
            vacancy = session.query(Vacancy).filter(
                Vacancy.id == vacancy_uuid).first()
            if not vacancy:
                logger.warning(
                    f"Vacancy {vacancy_id} not found. Skipping analytics.")
                # Выходим без ошибки. Если это была гонка, ретрай сработает при
                # следующем вызове.
                return

            total_candidates = session.query(func.count(VacancyCandidate.id)).filter(
                VacancyCandidate.vacancy_id == vacancy_uuid
            ).scalar() or 0

            days_open = None
            now = datetime.datetime.now()
            if vacancy.status == "closed" and vacancy.closed_at:
                days_open = (vacancy.closed_at - vacancy.created_at).days
            elif vacancy.created_at:
                days_open = (now - vacancy.created_at).days

            # Upsert
            analytics = session.query(VacancyAnalytics).filter(
                VacancyAnalytics.vacancy_id == vacancy_uuid
            ).first()

            if analytics:
                analytics.total_candidates = total_candidates
                analytics.days_open = days_open
                analytics.updated_at = now
            else:
                session.add(VacancyAnalytics(
                    vacancy_id=vacancy_uuid,
                    total_candidates=total_candidates,
                    days_open=days_open
                ))
            # commit() вызывается автоматически в get_sync_session()

    except IntegrityError as e:
        logger.warning(
            f"IntegrityError for vacancy {vacancy_id}: {e}. Retrying...")
        self.retry(exc=e, countdown=60)
    except Exception as exc:
        logger.error(f"Unexpected error in analytics task: {exc}")
        self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def recalculate_stage_analytics_task(self, vacancy_id: str) -> None:
    """Пересчёт метрик по этапам воронки: кол-во кандидатов, среднее время."""
    try:
        vacancy_uuid = uuid.UUID(vacancy_id)

        # Используем синхронную сессию
        with get_sync_session() as session:
            stages = session.query(VacancyStage).filter(
                VacancyStage.vacancy_id == vacancy_uuid
            ).order_by(VacancyStage.order_index).all()

            now = datetime.datetime.now()
            for stage in stages:
                candidates_count = session.query(func.count(VacancyCandidate.id)).filter(
                    VacancyCandidate.current_stage_id == stage.id
                ).scalar() or 0

                # Расчёт среднего времени на этапе через историю переходов
                transitions_in = session.query(StageTransition).filter(
                    StageTransition.to_stage_id == stage.id
                ).all()

                avg_days = None
                if transitions_in:
                    days_list = []
                    for t_in in transitions_in:
                        # Ищем следующий переход ИЗ этого этапа
                        t_out = session.query(StageTransition).filter(
                            StageTransition.vacancy_candidate_id == t_in.vacancy_candidate_id,
                            StageTransition.from_stage_id == stage.id,
                            StageTransition.moved_at > t_in.moved_at
                        ).order_by(StageTransition.moved_at).first()

                        end = t_out.moved_at if t_out else now
                        days_list.append(
                            (end - t_in.moved_at).total_seconds() / 86400)

                    avg_days = sum(days_list) / \
                        len(days_list) if days_list else None

                # Upsert
                analytics = session.query(StageAnalytics).filter(
                    StageAnalytics.vacancy_stage_id == stage.id
                ).first()

                if analytics:
                    analytics.candidates_count = candidates_count
                    analytics.avg_days_in_stage = avg_days
                    analytics.updated_at = now
                else:
                    session.add(StageAnalytics(
                        vacancy_stage_id=stage.id,
                        candidates_count=candidates_count,
                        avg_days_in_stage=avg_days
                    ))
            # session.commit() не нужен
    except Exception as exc:
        self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def recalculate_recruiter_analytics_task(self, recruiter_id: str) -> None:
    """Пересчёт нагрузки рекрутера: открытые вакансии, назначенные кандидаты."""
    try:
        recruiter_uuid = uuid.UUID(recruiter_id)

        # Используем синхронную сессию
        with get_sync_session() as session:
            open_vacancies = session.query(func.count(Vacancy.id)).filter(
                Vacancy.created_by == recruiter_uuid,
                Vacancy.status == "open"
            ).scalar() or 0

            total_assigned = session.query(func.count(VacancyCandidate.id)).filter(
                VacancyCandidate.assigned_by == recruiter_uuid
            ).scalar() or 0

            analytics = session.query(RecruiterAnalytics).filter(
                RecruiterAnalytics.recruiter_id == recruiter_uuid
            ).first()

            now = datetime.datetime.now()
            if analytics:
                analytics.open_vacancies_count = open_vacancies
                analytics.total_candidates_assigned = total_assigned
                analytics.updated_at = now
            else:
                session.add(RecruiterAnalytics(
                    recruiter_id=recruiter_uuid,
                    open_vacancies_count=open_vacancies,
                    total_candidates_assigned=total_assigned
                ))
            # session.commit() не нужен
    except Exception as exc:
        self.retry(exc=exc)
