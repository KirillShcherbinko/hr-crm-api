from typing import Dict, Any

# ORM Models
from src.infrastructure.database.models.candidate import Candidate as CandidateModel
from src.infrastructure.database.models.vacancy import Vacancy as VacancyModel
from src.infrastructure.database.models.user import User as UserModel
from src.infrastructure.database.models.email import Email as EmailModel
from src.infrastructure.database.models.stage import VacancyStage as VacancyStageModel, StageTransition
from src.infrastructure.database.models.vacancy import VacancyCandidate as VacancyCandidateModel
from src.infrastructure.database.models.pipeline import PipelineTemplate as PipelineTemplateModel


def map_candidate(model: CandidateModel) -> Dict[str, Any]:
    return {
        "id": model.id, "full_name": model.full_name, "email": model.email,
        "phone": model.phone, "resume_url": model.resume_url,
        "created_by": model.created_by, "created_at": model.created_at, "updated_at": model.updated_at
    }


def map_vacancy(model: VacancyModel) -> Dict[str, Any]:
    return {
        "id": model.id, "title": model.title, "description": model.description,
        "status": model.status.value, "created_by": model.created_by,
        "created_at": model.created_at, "updated_at": model.updated_at, "closed_at": model.closed_at
    }


def map_user(model: UserModel) -> Dict[str, Any]:
    return {
        "id": model.id, "email": model.email, "full_name": model.full_name,
        "role": model.role.value, "is_active": model.is_active, "created_at": model.created_at
    }


def map_email(model: EmailModel) -> Dict[str, Any]:
    return {
        "id": model.id, "candidate_id": model.candidate_id, "vacancy_id": model.vacancy_id,
        "sent_by": model.sent_by, "subject": model.subject, "body": model.body,
        "sent_at": model.sent_at, "status": model.status.value
    }


def map_vacancy_stage(model: VacancyStageModel) -> Dict[str, Any]:
    return {
        "id": model.id, "vacancy_id": model.vacancy_id, "name": model.name,
        "order_index": model.order_index, "is_final": model.is_final
    }


def map_vacancy_candidate(model: VacancyCandidateModel) -> Dict[str, Any]:
    return {
        "id": model.id, "vacancy_id": model.vacancy_id, "candidate_id": model.candidate_id,
        "current_stage_id": model.current_stage_id, "assigned_by": model.assigned_by,
        "assigned_at": model.assigned_at
    }


def map_transition(model: StageTransition) -> Dict[str, Any]:
    return {
        "id": model.id, "vacancy_candidate_id": model.vacancy_candidate_id,
        "from_stage_id": model.from_stage_id, "to_stage_id": model.to_stage_id,
        "moved_by": model.moved_by, "moved_at": model.moved_at
    }


def map_template(model: PipelineTemplateModel,
                 include_stages: bool = False) -> Dict[str, Any]:
    result = {
        "id": model.id, "name": model.name, "created_by": model.created_by, "created_at": model.created_at
    }
    if include_stages:
        result["stages"] = [
            {"id": s.id,
             "name": s.name,
             "order_index": s.order_index,
             "is_final": s.is_final}
            for s in model.stages
        ]
    return result
