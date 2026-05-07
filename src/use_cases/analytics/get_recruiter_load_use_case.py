from typing import Dict, Any, List
from src.interface_adapters.repositories.analytics import IAnalyticsRepository


class GetRecruiterLoadUseCase:
    def __init__(self, repo: IAnalyticsRepository): self.repo = repo

    async def execute(self) -> List[Dict[str, Any]]:
        return await self.repo.get_recruiter_load()
