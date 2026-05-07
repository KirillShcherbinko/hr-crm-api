from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.analytics import IAnalyticsRepository


class GetVacancyAnalyticsUseCase:
    def __init__(self, repo: IAnalyticsRepository): self.repo = repo

    async def execute(self, vacancy_id: UUID) -> Dict[str, Any]:
        return await self.repo.get_vacancy_stats(vacancy_id)
