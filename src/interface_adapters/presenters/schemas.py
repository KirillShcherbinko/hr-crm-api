from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID


class LoginRequest(BaseModel):
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreateRequest(BaseModel):
    full_name: str
    email: EmailStr
    role: str = "recruiter"


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class RoleUpdateRequest(BaseModel):
    new_role: str = Field(..., pattern="^(admin|recruiter)$")


class CandidateCreateRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None


class CandidateUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class VacancyCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None


class VacancyUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class StageCreateRequest(BaseModel):
    name: str
    is_final: bool = False


class StageUpdateRequest(BaseModel):
    name: Optional[str] = None
    is_final: Optional[bool] = None


class ReorderStagesRequest(BaseModel):
    stage_ids: List[UUID]


class AssignCandidateRequest(BaseModel):
    candidate_id: UUID


class MoveCandidateRequest(BaseModel):
    new_stage_id: UUID


class TemplateCreateRequest(BaseModel):
    name: str


class TemplateUpdateRequest(BaseModel):
    name: Optional[str] = None


class ApplyTemplateRequest(BaseModel):
    template_id: UUID
    vacancy_id: UUID


class EmailSendRequest(BaseModel):
    candidate_id: UUID
    vacancy_id: Optional[UUID] = None
    subject: str
    body: str
