from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.stage import IVacancyStageRepository


class CreateVacancyStageUseCase:
    def __init__(
        self,
        stage_repo: IVacancyStageRepository): self.stage_repo = stage_repo

    async def execute(self, vacancy_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.stage_repo.create(vacancy_id, data)
