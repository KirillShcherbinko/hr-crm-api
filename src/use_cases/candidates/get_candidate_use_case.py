from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class GetCandidateUseCase:
    def __init__(
        self,
        candidate_repo: ICandidateRepository): self.candidate_repo = candidate_repo

    async def execute(self, candidate_id: UUID) -> Dict[str, Any]:
        c = await self.candidate_repo.get_by_id(candidate_id)
        if not c:
            raise ValueError("Candidate not found")
        return c
