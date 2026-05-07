from .base import Base
from .user import User
from .candidate import Candidate
from .vacancy import Vacancy, VacancyCandidate
from .stage import VacancyStage, StageTransition
from .pipeline import PipelineTemplate, PipelineTemplateStage
from .email import Email

# Все модели должны быть импортированы здесь, чтобы SQLAlchemy
# мог собрать полную схему перед выполнением миграций.
__all__ = [
    "Base", "User", "Candidate", "Vacancy", "VacancyCandidate",
    "VacancyStage", "StageTransition", "PipelineTemplate",
    "PipelineTemplateStage", "Email", "VacancyAnalytics",
    "StageAnalytics", "RecruiterAnalytics", "RefreshToken"
]
