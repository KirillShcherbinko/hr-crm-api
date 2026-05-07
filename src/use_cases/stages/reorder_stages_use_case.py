from typing import Dict, Any, List
from uuid import UUID
from src.interface_adapters.repositories.stage import IVacancyStageRepository


class ReorderVacancyStagesUseCase:
    def __init__(self, repo: IVacancyStageRepository): self.repo = repo

    async def execute(self, vacancy_id: UUID,
                      new_order: List[UUID]) -> List[Dict[str, Any]]:
        return await self.repo.reorder(vacancy_id, new_order)
