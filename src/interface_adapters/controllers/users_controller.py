from fastapi import APIRouter, Depends, status, HTTPException
from src.interface_adapters.presenters.dependencies import *
from src.interface_adapters.presenters.guards import get_current_user, require_admin
from src.interface_adapters.presenters.schemas import RoleUpdateRequest, UserCreateRequest, UserUpdateRequest
from uuid import UUID

router = APIRouter(tags=["Users"])


@router.get("/", response_model=list[dict])
async def list_users(skip=0, limit=50, _=Depends(
        require_admin), uc=Depends(get_list_users_use_case)):
    return await uc.execute(skip=skip, limit=limit)


@router.get("/me", response_model=dict)
async def get_me(current: dict = Depends(get_current_user),
                 uc=Depends(get_current_user_use_case)):
    return await uc.execute(user_id=current["sub"])


@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: UUID, _=Depends(require_admin),
                   uc=Depends(get_user_use_case)):
    try:
        return await uc.execute(user_id=user_id)
    except ValueError:
        raise HTTPException(404, "User not found")


@router.post("/", response_model=dict, status_code=201)
async def create_user(req: UserCreateRequest, _=Depends(
        require_admin), uc=Depends(get_create_recruiter_use_case)):
    return await uc.execute(full_name=req.full_name, email=req.email, role=req.role)


@router.patch("/", response_model=dict)
async def update_profile(
    req: UserUpdateRequest,
    current_user: dict = Depends(get_current_user),
    uc=Depends(get_update_profile_use_case)
):
    try:
        return await uc.execute(user_id=current_user["sub"], data=req.model_dump(exclude_unset=True))
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/{user_id}/role", response_model=dict)
async def update_role(
    user_id: UUID,
    req: RoleUpdateRequest,
    _=Depends(require_admin),
    uc=Depends(get_update_role_use_case)
):
    try:
        return await uc.execute(user_id=user_id, new_role=req.new_role)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/{user_id}/deactivate", status_code=204)
async def deactivate(user_id: UUID, _=Depends(require_admin),
                     uc=Depends(get_deactivate_user_use_case)):
    await uc.execute(user_id=user_id)
