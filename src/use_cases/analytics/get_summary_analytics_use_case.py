from typing import Dict, Any
from src.interface_adapters.repositories.analytics import IAnalyticsRepository


class GetSummaryAnalyticsUseCase:
    def __init__(self, repo: IAnalyticsRepository): self.repo = repo

    async def execute(self) -> Dict[str, Any]:
        return await self.repo.get_summary()
