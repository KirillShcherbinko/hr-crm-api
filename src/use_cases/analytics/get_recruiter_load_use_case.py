from typing import Dict, Any, List
from src.interface_adapters.repositories.analytics import IAnalyticsRepository


class GetRecruiterLoadUseCase:
    def __init__(
        self,
        analytics_repo: IAnalyticsRepository): self.analytics_repo = analytics_repo

    async def execute(self) -> List[Dict[str, Any]]:
        return await self.analytics_repo.get_recruiter_load()
