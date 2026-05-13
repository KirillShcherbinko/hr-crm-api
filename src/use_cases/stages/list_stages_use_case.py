from typing import Dict, Any, List
from uuid import UUID
from src.interface_adapters.repositories.stage import IVacancyStageRepository


class ListVacancyStagesUseCase:
    def __init__(
        self,
        stage_repo: IVacancyStageRepository): self.stage_repo = stage_repo

    async def execute(self, vacancy_id: UUID) -> List[Dict[str, Any]]:
        return await self.stage_repo.list_by_vacancy(vacancy_id)
