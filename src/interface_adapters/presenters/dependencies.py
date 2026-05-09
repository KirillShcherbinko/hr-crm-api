from functools import lru_cache

from fastapi import Depends
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import Settings
from src.infrastructure.database.db import get_db
from src.infrastructure.storage.minio_client import get_minio_client

# ──────────────────────────────────────────────────────────────
# 📦 REPOSITORIES
# ──────────────────────────────────────────────────────────────
from src.interface_adapters.repositories.auth import AuthRepository
from src.interface_adapters.repositories.user import UserRepository
from src.interface_adapters.repositories.candidate import CandidateRepository
from src.interface_adapters.repositories.vacancy import VacancyRepository
from src.interface_adapters.repositories.stage import VacancyStageRepository
from src.interface_adapters.repositories.vacancy_candidate import VacancyCandidateRepository
from src.interface_adapters.repositories.pipeline import PipelineTemplateRepository
from src.interface_adapters.repositories.email import EmailRepository
from src.interface_adapters.repositories.analytics import AnalyticsRepository

# ──────────────────────────────────────────────────────────────
# 🎯 USE CASES
# ──────────────────────────────────────────────────────────────
from src.use_cases.auth.login_use_case import LoginUseCase
from src.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from src.use_cases.auth.logout_use_case import LogoutUseCase
from src.use_cases.users.create_recruiter_use_case import CreateRecruiterUseCase
from src.use_cases.users.get_current_user_use_case import GetCurrentUserUseCase
from src.use_cases.users.get_user_use_case import GetUserUseCase
from src.use_cases.users.list_users_use_case import ListUsersUseCase
from src.use_cases.users.update_profile_use_case import UpdateUserProfileUseCase
from src.use_cases.users.update_user_role_use_case import UpdateUserRoleUseCase
from src.use_cases.users.deactivate_user_use_case import DeactivateUserUseCase
from src.use_cases.candidates.create_candidate_use_case import CreateCandidateUseCase
from src.use_cases.candidates.get_candidate_use_case import GetCandidateUseCase
from src.use_cases.candidates.list_candidates_use_case import ListCandidatesUseCase
from src.use_cases.candidates.update_candidate_use_case import UpdateCandidateUseCase
from src.use_cases.candidates.delete_candidate_use_case import DeleteCandidateUseCase
from src.use_cases.candidates.attach_resume_use_case import AttachResumeUseCase
from src.use_cases.candidates.detach_resume_use_case import DetachResumeUseCase
from src.use_cases.candidates.get_candidate_emails_use_case import GetCandidateEmailsUseCase
from src.use_cases.vacancies.create_vacancy_use_case import CreateVacancyUseCase
from src.use_cases.vacancies.get_vacancy_use_case import GetVacancyUseCase
from src.use_cases.vacancies.list_vacancies_use_case import ListVacanciesUseCase
from src.use_cases.vacancies.update_vacancy_use_case import UpdateVacancyUseCase
from src.use_cases.vacancies.close_vacancy_use_case import CloseVacancyUseCase
from src.use_cases.vacancies.delete_vacancy_use_case import DeleteVacancyUseCase
from src.use_cases.stages.list_stages_use_case import ListVacancyStagesUseCase
from src.use_cases.stages.create_stage_use_case import CreateVacancyStageUseCase
from src.use_cases.stages.update_stage_use_case import UpdateVacancyStageUseCase
from src.use_cases.stages.delete_stage_use_case import DeleteVacancyStageUseCase
from src.use_cases.stages.reorder_stages_use_case import ReorderVacancyStagesUseCase
from src.use_cases.vacancy_candidates.list_vacancy_candidates_use_case import ListVacancyCandidatesUseCase
from src.use_cases.vacancy_candidates.assign_candidate_to_vacancy_use_case import AssignCandidateToVacancyUseCase
from src.use_cases.vacancy_candidates.unassign_candidate_from_vacancy_use_case import UnassignCandidateFromVacancyUseCase
from src.use_cases.vacancy_candidates.move_candidate_stage_use_case import MoveCandidateStageUseCase
from src.use_cases.vacancy_candidates.get_candidate_transitions_use_case import GetCandidateTransitionsUseCase
from src.use_cases.pipeline.list_pipeline_templates_use_case import ListPipelineTemplatesUseCase
from src.use_cases.pipeline.get_pipeline_template_use_case import GetPipelineTemplateUseCase
from src.use_cases.pipeline.create_pipeline_template_use_case import CreatePipelineTemplateUseCase
from src.use_cases.pipeline.update_pipeline_template_use_case import UpdatePipelineTemplateUseCase
from src.use_cases.pipeline.delete_pipeline_template_use_case import DeletePipelineTemplateUseCase
from src.use_cases.pipeline.add_pipeline_stage_use_case import AddPipelineStageUseCase
from src.use_cases.pipeline.update_pipeline_stage_use_case import UpdatePipelineStageUseCase
from src.use_cases.pipeline.delete_pipeline_stage_use_case import DeletePipelineStageUseCase
from src.use_cases.pipeline.apply_template_to_vacancy_use_case import ApplyTemplateToVacancyUseCase
from src.use_cases.emails.send_email_use_case import SendEmailUseCase
from src.use_cases.emails.list_emails_use_case import ListEmailsUseCase
from src.use_cases.emails.get_email_use_case import GetEmailUseCase
from src.use_cases.analytics.get_vacancy_analytics_use_case import GetVacancyAnalyticsUseCase
from src.use_cases.analytics.get_recruiter_load_use_case import GetRecruiterLoadUseCase
from src.use_cases.analytics.get_recruiter_stats_use_case import GetRecruiterStatsUseCase
from src.use_cases.analytics.get_summary_analytics_use_case import GetSummaryAnalyticsUseCase


# ──────────────────────────────────────────────────────────────
# 🔧 BASE DEPENDENCIES
# ──────────────────────────────────────────────────────────────
@lru_cache
def get_settings() -> Settings:
    return Settings()


# ──────────────────────────────────────────────────────────────
# 🔐 AUTH USE CASES
# ──────────────────────────────────────────────────────────────
def get_login_use_case(
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings)
) -> LoginUseCase:
    return LoginUseCase(
        user_repo=UserRepository(session),
        auth_repo=AuthRepository(session),
        secret_key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        access_exp=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_exp=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )


def get_refresh_token_use_case(
    session: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings)
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(
        user_repo=UserRepository(session),
        auth_repo=AuthRepository(session),
        secret_key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        access_exp=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def get_logout_use_case(
    session: AsyncSession = Depends(get_db)
) -> LogoutUseCase:
    return LogoutUseCase(auth_repo=AuthRepository(session))


# ──────────────────────────────────────────────────────────────
# 👥 USERS USE CASES
# ──────────────────────────────────────────────────────────────
def get_create_recruiter_use_case(
        session: AsyncSession = Depends(get_db)) -> CreateRecruiterUseCase:
    return CreateRecruiterUseCase(user_repo=UserRepository(session))


def get_current_user_use_case(
        session: AsyncSession = Depends(get_db)) -> GetCurrentUserUseCase:
    return GetCurrentUserUseCase(user_repo=UserRepository(session))


def get_user_use_case(
        session: AsyncSession = Depends(get_db)) -> GetUserUseCase:
    return GetUserUseCase(user_repo=UserRepository(session))


def get_list_users_use_case(
        session: AsyncSession = Depends(get_db)) -> ListUsersUseCase:
    return ListUsersUseCase(user_repo=UserRepository(session))


def get_update_profile_use_case(
        session: AsyncSession = Depends(get_db)) -> UpdateUserProfileUseCase:
    return UpdateUserProfileUseCase(user_repo=UserRepository(session))


def get_update_role_use_case(
        session: AsyncSession = Depends(get_db)) -> UpdateUserRoleUseCase:
    return UpdateUserRoleUseCase(user_repo=UserRepository(session))


def get_deactivate_user_use_case(
        session: AsyncSession = Depends(get_db)) -> DeactivateUserUseCase:
    return DeactivateUserUseCase(user_repo=UserRepository(session))


# ──────────────────────────────────────────────────────────────
# 🧑‍💼 CANDIDATES USE CASES
# ──────────────────────────────────────────────────────────────
def get_create_candidate_use_case(
        session: AsyncSession = Depends(get_db)) -> CreateCandidateUseCase:
    return CreateCandidateUseCase(candidate_repo=CandidateRepository(session))


def get_candidate_use_case(
        session: AsyncSession = Depends(get_db)) -> GetCandidateUseCase:
    return GetCandidateUseCase(candidate_repo=CandidateRepository(session))


def get_list_candidates_use_case(
        session: AsyncSession = Depends(get_db)) -> ListCandidatesUseCase:
    return ListCandidatesUseCase(candidate_repo=CandidateRepository(session))


def get_update_candidate_use_case(
        session: AsyncSession = Depends(get_db)) -> UpdateCandidateUseCase:
    return UpdateCandidateUseCase(candidate_repo=CandidateRepository(session))


def get_delete_candidate_use_case(
        session: AsyncSession = Depends(get_db)) -> DeleteCandidateUseCase:
    return DeleteCandidateUseCase(candidate_repo=CandidateRepository(session))


def get_attach_resume_use_case(
    session: AsyncSession = Depends(get_db),
    minio: Minio = Depends(get_minio_client)
) -> AttachResumeUseCase:
    return AttachResumeUseCase(
        candidate_repo=CandidateRepository(session), minio_client=minio)


def get_detach_resume_use_case(
    session: AsyncSession = Depends(get_db),
    minio: Minio = Depends(get_minio_client)
) -> DetachResumeUseCase:
    return DetachResumeUseCase(
        candidate_repo=CandidateRepository(session), minio_client=minio)


def get_candidate_emails_use_case(
        session: AsyncSession = Depends(get_db)) -> GetCandidateEmailsUseCase:
    return GetCandidateEmailsUseCase(
        candidate_repo=CandidateRepository(session))


# ──────────────────────────────────────────────────────────────
# 💼 VACANCIES USE CASES
# ──────────────────────────────────────────────────────────────
def get_create_vacancy_use_case(
        session: AsyncSession = Depends(get_db)) -> CreateVacancyUseCase:
    return CreateVacancyUseCase(vacancy_repo=VacancyRepository(session))


def get_vacancy_use_case(
        session: AsyncSession = Depends(get_db)) -> GetVacancyUseCase:
    return GetVacancyUseCase(vacancy_repo=VacancyRepository(session))


def get_list_vacancies_use_case(
        session: AsyncSession = Depends(get_db)) -> ListVacanciesUseCase:
    return ListVacanciesUseCase(vacancy_repo=VacancyRepository(session))


def get_update_vacancy_use_case(
        session: AsyncSession = Depends(get_db)) -> UpdateVacancyUseCase:
    return UpdateVacancyUseCase(vacancy_repo=VacancyRepository(session))


def get_close_vacancy_use_case(
        session: AsyncSession = Depends(get_db)) -> CloseVacancyUseCase:
    return CloseVacancyUseCase(vacancy_repo=VacancyRepository(session))


def get_delete_vacancy_use_case(
        session: AsyncSession = Depends(get_db)) -> DeleteVacancyUseCase:
    return DeleteVacancyUseCase(vacancy_repo=VacancyRepository(session))


# ──────────────────────────────────────────────────────────────
# 🔄 VACANCY STAGES USE CASES
# ──────────────────────────────────────────────────────────────
def get_list_vacancy_stages_use_case(
        session: AsyncSession = Depends(get_db)) -> ListVacancyStagesUseCase:
    return ListVacancyStagesUseCase(stage_repo=VacancyStageRepository(session))


def get_create_vacancy_stage_use_case(
        session: AsyncSession = Depends(get_db)) -> CreateVacancyStageUseCase:
    return CreateVacancyStageUseCase(
        stage_repo=VacancyStageRepository(session))


def get_update_vacancy_stage_use_case(
        session: AsyncSession = Depends(get_db)) -> UpdateVacancyStageUseCase:
    return UpdateVacancyStageUseCase(
        stage_repo=VacancyStageRepository(session))


def get_delete_vacancy_stage_use_case(
        session: AsyncSession = Depends(get_db)) -> DeleteVacancyStageUseCase:
    return DeleteVacancyStageUseCase(
        stage_repo=VacancyStageRepository(session))


def get_reorder_vacancy_stages_use_case(
        session: AsyncSession = Depends(get_db)) -> ReorderVacancyStagesUseCase:
    return ReorderVacancyStagesUseCase(
        stage_repo=VacancyStageRepository(session))


# ──────────────────────────────────────────────────────────────
# 🤝 VACANCY CANDIDATES USE CASES
# ──────────────────────────────────────────────────────────────
def get_list_vacancy_candidates_use_case(
        session: AsyncSession = Depends(get_db)) -> ListVacancyCandidatesUseCase:
    return ListVacancyCandidatesUseCase(
        vc_repo=VacancyCandidateRepository(session))


def get_assign_candidate_use_case(session: AsyncSession = Depends(
        get_db)) -> AssignCandidateToVacancyUseCase:
    return AssignCandidateToVacancyUseCase(
        vc_repo=VacancyCandidateRepository(session))


def get_unassign_candidate_use_case(session: AsyncSession = Depends(
        get_db)) -> UnassignCandidateFromVacancyUseCase:
    return UnassignCandidateFromVacancyUseCase(
        vc_repo=VacancyCandidateRepository(session))


def get_move_candidate_stage_use_case(
        session: AsyncSession = Depends(get_db)) -> MoveCandidateStageUseCase:
    return MoveCandidateStageUseCase(
        vc_repo=VacancyCandidateRepository(session))


def get_candidate_transitions_use_case(
        session: AsyncSession = Depends(get_db)) -> GetCandidateTransitionsUseCase:
    return GetCandidateTransitionsUseCase(
        vc_repo=VacancyCandidateRepository(session))


# ──────────────────────────────────────────────────────────────
# 🗂️ PIPELINE TEMPLATES USE CASES
# ──────────────────────────────────────────────────────────────
def get_list_pipeline_templates_use_case(
        session: AsyncSession = Depends(get_db)) -> ListPipelineTemplatesUseCase:
    return ListPipelineTemplatesUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


def get_pipeline_template_use_case(
        session: AsyncSession = Depends(get_db)) -> GetPipelineTemplateUseCase:
    return GetPipelineTemplateUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


def get_create_pipeline_template_use_case(
        session: AsyncSession = Depends(get_db)) -> CreatePipelineTemplateUseCase:
    return CreatePipelineTemplateUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


def get_update_pipeline_template_use_case(
        session: AsyncSession = Depends(get_db)) -> UpdatePipelineTemplateUseCase:
    return UpdatePipelineTemplateUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


def get_delete_pipeline_template_use_case(
        session: AsyncSession = Depends(get_db)) -> DeletePipelineTemplateUseCase:
    return DeletePipelineTemplateUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


def get_add_pipeline_stage_use_case(
        session: AsyncSession = Depends(get_db)) -> AddPipelineStageUseCase:
    return AddPipelineStageUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


def get_update_pipeline_stage_use_case(
        session: AsyncSession = Depends(get_db)) -> UpdatePipelineStageUseCase:
    return UpdatePipelineStageUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


def get_delete_pipeline_stage_use_case(
        session: AsyncSession = Depends(get_db)) -> DeletePipelineStageUseCase:
    return DeletePipelineStageUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


def get_apply_template_use_case(session: AsyncSession = Depends(
        get_db)) -> ApplyTemplateToVacancyUseCase:
    return ApplyTemplateToVacancyUseCase(
        pipeline_repo=PipelineTemplateRepository(session))


# ──────────────────────────────────────────────────────────────
# 📧 EMAILS USE CASES
# ──────────────────────────────────────────────────────────────
def get_send_email_use_case(
        session: AsyncSession = Depends(get_db)) -> SendEmailUseCase:
    return SendEmailUseCase(email_repo=EmailRepository(session))


def get_list_emails_use_case(
        session: AsyncSession = Depends(get_db)) -> ListEmailsUseCase:
    return ListEmailsUseCase(email_repo=EmailRepository(session))


def get_email_use_case(
        session: AsyncSession = Depends(get_db)) -> GetEmailUseCase:
    return GetEmailUseCase(email_repo=EmailRepository(session))


# ──────────────────────────────────────────────────────────────
# 📊 ANALYTICS USE CASES
# ──────────────────────────────────────────────────────────────
def get_vacancy_analytics_use_case(
        session: AsyncSession = Depends(get_db)) -> GetVacancyAnalyticsUseCase:
    return GetVacancyAnalyticsUseCase(
        analytics_repo=AnalyticsRepository(session))


def get_recruiter_load_use_case(
        session: AsyncSession = Depends(get_db)) -> GetRecruiterLoadUseCase:
    return GetRecruiterLoadUseCase(analytics_repo=AnalyticsRepository(session))


def get_recruiter_stats_use_case(
        session: AsyncSession = Depends(get_db)) -> GetRecruiterStatsUseCase:
    return GetRecruiterStatsUseCase(
        analytics_repo=AnalyticsRepository(session))


def get_summary_analytics_use_case(
        session: AsyncSession = Depends(get_db)) -> GetSummaryAnalyticsUseCase:
    return GetSummaryAnalyticsUseCase(
        analytics_repo=AnalyticsRepository(session))
