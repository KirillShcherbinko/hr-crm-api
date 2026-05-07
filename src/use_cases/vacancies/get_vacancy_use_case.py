from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.vacancy import IVacancyRepository


class GetVacancyUseCase:
    def __init__(self, repo: IVacancyRepository): self.repo = repo

    async def execute(self, vacancy_id: UUID) -> Dict[str, Any]:
        v = await self.repo.get_by_id(vacancy_id)
        if not v:
            raise ValueError("Vacancy not found")
        return v
