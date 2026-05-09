from fastapi import APIRouter, Depends, HTTPException
from src.interface_adapters.presenters.dependencies import *
from src.interface_adapters.presenters.guards import get_current_user, require_recruiter
from src.interface_adapters.presenters.schemas import VacancyCreateRequest, VacancyUpdateRequest, StageCreateRequest, StageUpdateRequest, ReorderStagesRequest
from uuid import UUID

router = APIRouter(prefix="/api/v1/vacancies", tags=["vacancies"])


@router.get("/", response_model=list[dict])
async def list_vacancies(skip=0, limit=50, status_filter: str = "", _=Depends(
        get_current_user), uc=Depends(get_list_vacancies_use_case)):
    return await uc.execute(filters={"status": status_filter} if status_filter else {}, skip=skip, limit=limit)


@router.get("/{vacancy_id}", response_model=dict)
async def get_vacancy(vacancy_id: UUID, _=Depends(
        get_current_user), uc=Depends(get_vacancy_use_case)):
    try:
        return await uc.execute(vacancy_id=vacancy_id)
    except ValueError:
        raise HTTPException(404, "Vacancy not found")


@router.post("/", response_model=dict, status_code=201)
async def create_vacancy(req: VacancyCreateRequest, current=Depends(
        require_recruiter), uc=Depends(get_create_vacancy_use_case)):
    return await uc.execute(data=req.model_dump(), created_by=current["sub"])


@router.patch("/{vacancy_id}", response_model=dict)
async def update_vacancy(vacancy_id: UUID, req: VacancyUpdateRequest, _=Depends(
        require_recruiter), uc=Depends(get_update_vacancy_use_case)):
    try:
        return await uc.execute(vacancy_id=vacancy_id, data=req.model_dump(exclude_unset=True))
    except ValueError:
        raise HTTPException(404, "Vacancy not found")


@router.post("/{vacancy_id}/close", response_model=dict)
async def close_vacancy(vacancy_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_close_vacancy_use_case)):
    return await uc.execute(vacancy_id=vacancy_id)


@router.delete("/{vacancy_id}", status_code=204)
async def delete_vacancy(vacancy_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_delete_vacancy_use_case)):
    await uc.execute(vacancy_id=vacancy_id)

# --- STAGES ---


@router.get("/{vacancy_id}/stages", response_model=list[dict])
async def list_stages(vacancy_id: UUID, _=Depends(
        get_current_user), uc=Depends(get_list_vacancy_stages_use_case)):
    return await uc.execute(vacancy_id=vacancy_id)


@router.post("/{vacancy_id}/stages", response_model=dict, status_code=201)
async def add_stage(vacancy_id: UUID, req: StageCreateRequest, _=Depends(
        require_recruiter), uc=Depends(get_create_vacancy_stage_use_case)):
    return await uc.execute(vacancy_id=vacancy_id, stage_data=req.model_dump())


@router.patch("/{vacancy_id}/stages/{stage_id}", response_model=dict)
async def update_stage(vacancy_id: UUID, stage_id: UUID, req: StageUpdateRequest, _=Depends(
        require_recruiter), uc=Depends(get_update_vacancy_stage_use_case)):
    try:
        return await uc.execute(stage_id=stage_id, stage_data=req.model_dump(exclude_unset=True))
    except ValueError:
        raise HTTPException(404, "Stage not found")


@router.delete("/{vacancy_id}/stages/{stage_id}", status_code=204)
async def delete_stage(vacancy_id: UUID, stage_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_delete_vacancy_stage_use_case)):
    await uc.execute(stage_id=stage_id)


@router.post("/{vacancy_id}/stages/reorder", response_model=list[dict])
async def reorder_stages(vacancy_id: UUID, req: ReorderStagesRequest, _=Depends(
        require_recruiter), uc=Depends(get_reorder_vacancy_stages_use_case)):
    return await uc.execute(vacancy_id=vacancy_id, new_order=req.stage_ids)

# --- VACANCY CANDIDATES ---


@router.get("/{vacancy_id}/candidates", response_model=list[dict])
async def list_vc(vacancy_id: UUID, _=Depends(get_current_user),
                  uc=Depends(get_list_vacancy_candidates_use_case)):
    return await uc.execute(vacancy_id=vacancy_id)


@router.post("/{vacancy_id}/candidates", response_model=dict, status_code=201)
async def assign_candidate(vacancy_id: UUID, candidate_id: UUID, current=Depends(
        require_recruiter), uc=Depends(get_assign_candidate_use_case)):
    return await uc.execute(vacancy_id=vacancy_id, candidate_id=candidate_id, assigned_by=current["sub"])


@router.delete("/{vacancy_id}/candidates/{candidate_id}", status_code=204)
async def unassign_candidate(vacancy_id: UUID, candidate_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_unassign_candidate_use_case)):
    await uc.execute(vacancy_id=vacancy_id, candidate_id=candidate_id)


@router.post("/{vacancy_id}/candidates/{candidate_id}/move",
             response_model=dict)
async def move_stage(vacancy_id: UUID, candidate_id: UUID, new_stage_id: UUID, current=Depends(
        require_recruiter), uc=Depends(get_move_candidate_stage_use_case)):
    return await uc.execute(vacancy_candidate_id=candidate_id, new_stage_id=new_stage_id, moved_by=current["sub"])


@router.get("/{vacancy_id}/candidates/{candidate_id}/transitions",
            response_model=list[dict])
async def get_transitions(vacancy_id: UUID, candidate_id: UUID, _=Depends(
        get_current_user), uc=Depends(get_candidate_transitions_use_case)):
    return await uc.execute(vacancy_candidate_id=candidate_id)
