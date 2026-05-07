from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.vacancy import IVacancyRepository


class CreateVacancyUseCase:
    def __init__(self, repo: IVacancyRepository): self.repo = repo

    async def execute(self, data: Dict[str, Any],
                      created_by: UUID) -> Dict[str, Any]:
        return await self.repo.create(data, created_by)
