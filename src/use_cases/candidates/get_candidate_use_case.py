from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class GetCandidateUseCase:
    def __init__(self, repo: ICandidateRepository): self.repo = repo

    async def execute(self, candidate_id: UUID) -> Dict[str, Any]:
        c = await self.repo.get_by_id(candidate_id)
        if not c:
            raise ValueError("Candidate not found")
        return c
