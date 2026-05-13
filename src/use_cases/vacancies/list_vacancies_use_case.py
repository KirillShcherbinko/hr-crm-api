from typing import Dict, Any, List
from src.interface_adapters.repositories.vacancy import IVacancyRepository


class ListVacanciesUseCase:
    def __init__(
        self,
        vacancy_repo: IVacancyRepository): self.vacancy_repo = vacancy_repo

    async def execute(
            self, filters: Dict[str, Any], skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.vacancy_repo.list(filters, skip, limit)
