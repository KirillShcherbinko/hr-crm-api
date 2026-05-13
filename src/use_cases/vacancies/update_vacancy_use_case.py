from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.vacancy import IVacancyRepository


class UpdateVacancyUseCase:
    def __init__(
        self,
        vacancy_repo: IVacancyRepository): self.vacancy_repo = vacancy_repo

    async def execute(self, vacancy_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.vacancy_repo.update(vacancy_id, data)
