from typing import Dict, Any
from uuid import UUID
from fastapi import HTTPException
from src.infrastructure.tasks.tasks import recalculate_vacancy_analytics_task
from src.interface_adapters.repositories.vacancy_candidate import IVacancyCandidateRepository


class MoveCandidateStageUseCase:
    def __init__(self, vc_repo: IVacancyCandidateRepository):
        self.vc_repo = vc_repo

    async def execute(self, vacancy_id: UUID, candidate_id: UUID,
                      new_stage_id: UUID, moved_by: UUID) -> Dict[str, Any]:
        link = await self.vc_repo.get_by_vacancy_and_candidate(vacancy_id, candidate_id)

        if not link:
            raise HTTPException(
                status_code=404,
                detail="Candidate is not assigned to this vacancy")

        result = await self.vc_repo.move_stage(link.id, new_stage_id, moved_by)

        recalculate_vacancy_analytics_task.delay(str(vacancy_id))
        return result
