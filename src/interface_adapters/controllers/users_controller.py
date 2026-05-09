from fastapi import APIRouter, Depends, status, HTTPException
from src.interface_adapters.presenters.dependencies import *
from src.interface_adapters.presenters.guards import get_current_user, require_admin
from src.interface_adapters.presenters.schemas import UserCreateRequest, UserUpdateRequest
from uuid import UUID

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/", response_model=list[dict])
async def list_users(skip=0, limit=50, _=Depends(
        require_admin), uc=Depends(get_list_users_use_case)):
    return await uc.execute(skip=skip, limit=limit)


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


@router.patch("/{user_id}", response_model=dict)
async def update_user(user_id: UUID, req: UserUpdateRequest, _=Depends(
        require_admin), uc=Depends(get_update_profile_use_case)):
    try:
        return await uc.execute(user_id=user_id, data=req.model_dump(exclude_unset=True))
    except ValueError:
        raise HTTPException(404, "User not found")


@router.patch("/{user_id}/role", response_model=dict)
async def update_role(user_id: UUID, new_role: str, _=Depends(
        require_admin), uc=Depends(get_update_role_use_case)):
    try:
        return await uc.execute(user_id=user_id, new_role=new_role)
    except ValueError:
        raise HTTPException(404, "User not found")


@router.patch("/{user_id}/deactivate", status_code=204)
async def deactivate(user_id: UUID, _=Depends(require_admin),
                     uc=Depends(get_deactivate_user_use_case)):
    await uc.execute(user_id=user_id)


@router.get("/me", response_model=dict)
async def get_me(current: dict = Depends(get_current_user),
                 uc=Depends(get_current_user_use_case)):
    return await uc.execute(user_id=current["sub"])
