from typing import Dict, Any
from src.interface_adapters.repositories.analytics import IAnalyticsRepository


class GetSummaryAnalyticsUseCase:
    def __init__(
        self,
        analytics_repo: IAnalyticsRepository): self.analytics_repo = analytics_repo

    async def execute(self) -> Dict[str, Any]:
        return await self.analytics_repo.get_summary()
