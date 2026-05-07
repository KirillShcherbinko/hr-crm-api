from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.vacancy import Vacancy as VacancyModel, VacancyStatus
from src.infrastructure.database.models.vacancy import VacancyCandidate, VacancyAnalytics
from src.infrastructure.database.models.user import RecruiterAnalytics
from src.interface_adapters.repositories.analytics import IAnalyticsRepository
from .base import BaseRepository


class AnalyticsRepository(IAnalyticsRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_vacancy_stats(self, vacancy_id: UUID) -> Dict[str, Any]:
        # Подтягиваем агрегаты напрямую
        stmt = select(VacancyAnalytics).where(
            VacancyAnalytics.vacancy_id == vacancy_id)
        result = await self.session.execute(stmt)
        analytics = result.scalar_one_or_none()

        if not analytics:
            return {"vacancy_id": vacancy_id,
                    "total_candidates": 0, "days_open": None}

        return {
            "vacancy_id": analytics.vacancy_id,
            "total_candidates": analytics.total_candidates,
            "days_open": analytics.days_open,
            "updated_at": analytics.updated_at
        }

    async def get_recruiter_load(self) -> List[Dict[str, Any]]:
        stmt = select(RecruiterAnalytics).order_by(
            RecruiterAnalytics.total_candidates_assigned.desc())
        result = await self.session.execute(stmt)
        return [
            {
                "recruiter_id": r.recruiter_id,
                "open_vacancies_count": r.open_vacancies_count,
                "total_candidates_assigned": r.total_candidates_assigned,
                "updated_at": r.updated_at
            } for r in result.scalars().all()
        ]

    async def get_recruiter_stats(self, recruiter_id: UUID) -> Dict[str, Any]:
        stmt = select(RecruiterAnalytics).where(
            RecruiterAnalytics.recruiter_id == recruiter_id)
        result = await self.session.execute(stmt)
        r = result.scalar_one_or_none()
        if not r:
            return {"recruiter_id": recruiter_id,
                    "open_vacancies_count": 0, "total_candidates_assigned": 0}
        return {
            "recruiter_id": r.recruiter_id, "open_vacancies_count": r.open_vacancies_count,
            "total_candidates_assigned": r.total_candidates_assigned, "updated_at": r.updated_at
        }

    async def get_summary(self) -> Dict[str, Any]:
        stmt_vacancies = select(
            func.count(
                VacancyModel.id)).where(
            VacancyModel.status == VacancyStatus.open)
        stmt_closed = select(func.count(VacancyModel.id)).where(
            VacancyModel.status == VacancyStatus.closed)
        stmt_candidates = select(
            func.count(
                VacancyCandidate.candidate_id)).distinct()

        res_open = await self.session.execute(stmt_vacancies)
        res_closed = await self.session.execute(stmt_closed)
        res_cand = await self.session.execute(stmt_candidates)

        return {
            "open_vacancies": res_open.scalar_one(),
            "closed_vacancies": res_closed.scalar_one(),
            "total_candidates_in_system": res_cand.scalar_one()
        }
