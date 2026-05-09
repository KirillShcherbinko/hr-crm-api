from fastapi import APIRouter, Depends, status, HTTPException
from src.interface_adapters.presenters.dependencies import *
from src.interface_adapters.presenters.guards import get_current_user, require_recruiter
from src.interface_adapters.presenters.schemas import EmailSendRequest
from uuid import UUID

router = APIRouter(tags=["Emails"])


@router.post("/", response_model=dict, status_code=201)
async def send_email(req: EmailSendRequest, current=Depends(
        require_recruiter), uc=Depends(get_send_email_use_case)):
    return await uc.execute(data=req.model_dump(), sent_by=current["sub"])


@router.get("/", response_model=list[dict])
async def list_emails(skip=0, limit=50, candidate_id: UUID | None = None, vacancy_id: UUID
                      | None = None, _=Depends(get_current_user), uc=Depends(get_list_emails_use_case)):
    filters = {}
    if candidate_id:
        filters["candidate_id"] = candidate_id
    if vacancy_id:
        filters["vacancy_id"] = vacancy_id
    return await uc.execute(filters=filters, skip=skip, limit=limit)


@router.get("/{email_id}", response_model=dict)
async def get_email(email_id: UUID, _=Depends(
        get_current_user), uc=Depends(get_email_use_case)):
    try:
        return await uc.execute(email_id=email_id)
    except ValueError:
        raise HTTPException(404, "Email not found")
