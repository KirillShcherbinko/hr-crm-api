from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.analytics import IAnalyticsRepository


class GetVacancyAnalyticsUseCase:
    def __init__(
        self,
        analytics_repo: IAnalyticsRepository): self.analytics_repo = analytics_repo

    async def execute(self, vacancy_id: UUID) -> Dict[str, Any]:
        return await self.analytics_repo.get_vacancy_stats(vacancy_id)
