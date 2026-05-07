from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.analytics import IAnalyticsRepository


class GetRecruiterStatsUseCase:
    def __init__(self, repo: IAnalyticsRepository): self.repo = repo

    async def execute(self, recruiter_id: UUID) -> Dict[str, Any]:
        return await self.repo.get_recruiter_stats(recruiter_id)
