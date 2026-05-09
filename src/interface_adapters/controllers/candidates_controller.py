from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.interface_adapters.presenters.dependencies import *
from src.interface_adapters.presenters.guards import get_current_user, require_recruiter
from src.interface_adapters.presenters.schemas import CandidateCreateRequest, CandidateUpdateRequest
from uuid import UUID

router = APIRouter(prefix="/api/v1/candidates", tags=["candidates"])


@router.get("/", response_model=list[dict])
async def list_candidates(skip=0, limit=50, filters: str = "", _=Depends(
        get_current_user), uc=Depends(get_list_candidates_use_case)):
    f = dict(pair.split("=") for pair in filters.split(",") if "=" in pair)
    return await uc.execute(filters=f, skip=skip, limit=limit)


@router.get("/{candidate_id}", response_model=dict)
async def get_candidate(candidate_id: UUID, _=Depends(
        get_current_user), uc=Depends(get_candidate_use_case)):
    try:
        return await uc.execute(candidate_id=candidate_id)
    except ValueError:
        raise HTTPException(404, "Candidate not found")


@router.post("/", response_model=dict, status_code=201)
async def create_candidate(req: CandidateCreateRequest, current=Depends(
        require_recruiter), uc=Depends(get_create_candidate_use_case)):
    return await uc.execute(data=req.model_dump(), created_by=current["sub"])


@router.patch("/{candidate_id}", response_model=dict)
async def update_candidate(candidate_id: UUID, req: CandidateUpdateRequest, _=Depends(
        require_recruiter), uc=Depends(get_update_candidate_use_case)):
    try:
        return await uc.execute(candidate_id=candidate_id, data=req.model_dump(exclude_unset=True))
    except ValueError:
        raise HTTPException(404, "Candidate not found")


@router.delete("/{candidate_id}", status_code=204)
async def delete_candidate(candidate_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_delete_candidate_use_case)):
    await uc.execute(candidate_id=candidate_id)


@router.post("/{candidate_id}/resume", response_model=dict)
async def attach_resume(candidate_id: UUID, file: UploadFile = File(...), _=Depends(
        require_recruiter), uc=Depends(get_attach_resume_use_case)):
    return await uc.execute(candidate_id=candidate_id, file_name=file.filename, file_bytes=await file.read())


@router.delete("/{candidate_id}/resume", status_code=204)
async def detach_resume(candidate_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_detach_resume_use_case)):
    await uc.execute(candidate_id=candidate_id)


@router.get("/{candidate_id}/emails", response_model=list[dict])
async def get_emails(candidate_id: UUID, _=Depends(
        get_current_user), uc=Depends(get_candidate_emails_use_case)):
    return await uc.execute(candidate_id=candidate_id)
