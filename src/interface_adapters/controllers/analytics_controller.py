from fastapi import APIRouter, Depends
from src.interface_adapters.presenters.dependencies import *
from uuid import UUID

from src.interface_adapters.presenters.guards import get_current_user, require_admin

router = APIRouter(tags=["Analytics"])


@router.get("/vacancies/{vacancy_id}", response_model=dict)
async def vacancy_stats(vacancy_id: UUID, _=Depends(
        get_current_user), uc=Depends(get_vacancy_analytics_use_case)):
    return await uc.execute(vacancy_id=vacancy_id)


@router.get("/recruiters", response_model=list[dict])
async def recruiter_load(_=Depends(require_admin),
                         uc=Depends(get_recruiter_load_use_case)):
    return await uc.execute()


@router.get("/recruiters/{recruiter_id}", response_model=dict)
async def recruiter_stats(recruiter_id: UUID, _=Depends(
        require_admin), uc=Depends(get_recruiter_stats_use_case)):
    return await uc.execute(recruiter_id=recruiter_id)


@router.get("/summary", response_model=dict)
async def summary(_=Depends(get_current_user),
                  uc=Depends(get_summary_analytics_use_case)):
    return await uc.execute()
