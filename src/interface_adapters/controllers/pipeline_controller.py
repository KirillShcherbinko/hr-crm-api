from fastapi import APIRouter, Depends, HTTPException
from src.interface_adapters.presenters.dependencies import *
from src.interface_adapters.presenters.guards import get_current_user, require_recruiter
from src.interface_adapters.presenters.schemas import TemplateCreateRequest, TemplateUpdateRequest, StageCreateRequest, StageUpdateRequest
from uuid import UUID

router = APIRouter(
    prefix="/api/v1/pipeline-templates",
    tags=["pipeline-templates"])


@router.get("/", response_model=list[dict])
async def list_templates(_=Depends(get_current_user),
                         uc=Depends(get_list_pipeline_templates_use_case)):
    return await uc.execute()


@router.get("/{template_id}", response_model=dict)
async def get_template(template_id: UUID, _=Depends(
        get_current_user), uc=Depends(get_pipeline_template_use_case)):
    try:
        return await uc.execute(template_id=template_id)
    except ValueError:
        raise HTTPException(404, "Template not found")


@router.post("/", response_model=dict, status_code=201)
async def create_template(req: TemplateCreateRequest, current=Depends(
        require_recruiter), uc=Depends(get_create_pipeline_template_use_case)):
    return await uc.execute(data=req.model_dump(), created_by=current["sub"])


@router.patch("/{template_id}", response_model=dict)
async def update_template(template_id: UUID, req: TemplateUpdateRequest, _=Depends(
        require_recruiter), uc=Depends(get_update_pipeline_template_use_case)):
    try:
        return await uc.execute(template_id=template_id, data=req.model_dump(exclude_unset=True))
    except ValueError:
        raise HTTPException(404, "Template not found")


@router.delete("/{template_id}", status_code=204)
async def delete_template(template_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_delete_pipeline_template_use_case)):
    await uc.execute(template_id=template_id)


@router.post("/{template_id}/stages", response_model=dict, status_code=201)
async def add_stage(template_id: UUID, req: StageCreateRequest, _=Depends(
        require_recruiter), uc=Depends(get_add_pipeline_stage_use_case)):
    return await uc.execute(template_id=template_id, pipeline_data=req.model_dump())


@router.patch("/{template_id}/stages/{stage_id}", response_model=dict)
async def update_stage(template_id: UUID, stage_id: UUID, req: StageUpdateRequest, _=Depends(
        require_recruiter), uc=Depends(get_update_pipeline_stage_use_case)):
    try:
        return await uc.execute(stage_id=stage_id, pipeline_data=req.model_dump(exclude_unset=True))
    except ValueError:
        raise HTTPException(404, "Stage not found")


@router.delete("/{template_id}/stages/{stage_id}", status_code=204)
async def delete_stage(template_id: UUID, stage_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_delete_pipeline_stage_use_case)):
    await uc.execute(stage_id=stage_id)


@router.post("/apply", response_model=list[dict])
async def apply_template(template_id: UUID, vacancy_id: UUID, _=Depends(
        require_recruiter), uc=Depends(get_apply_template_use_case)):
    return await uc.execute(template_id=template_id, vacancy_id=vacancy_id)
