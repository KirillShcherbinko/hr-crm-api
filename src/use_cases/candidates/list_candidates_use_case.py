from typing import Dict, Any, List
from src.interface_adapters.repositories.candidate import ICandidateRepository


class ListCandidatesUseCase:
    def __init__(self, repo: ICandidateRepository): self.repo = repo

    async def execute(
            self, filters: Dict[str, Any], skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.repo.list(filters, skip, limit)
