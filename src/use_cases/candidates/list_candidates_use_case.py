from typing import Dict, Any, List
from src.interface_adapters.repositories.candidate import ICandidateRepository


class ListCandidatesUseCase:
    def __init__(
        self,
        candidate_repo: ICandidateRepository): self.candidate_repo = candidate_repo

    async def execute(
            self, filters: Dict[str, Any], skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.candidate_repo.list(filters, skip, limit)
