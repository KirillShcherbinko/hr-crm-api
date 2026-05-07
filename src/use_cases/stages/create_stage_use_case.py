from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.stage import IVacancyStageRepository


class CreateVacancyStageUseCase:
    def __init__(self, repo: IVacancyStageRepository): self.repo = repo

    async def execute(self, vacancy_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.repo.create(vacancy_id, data)
