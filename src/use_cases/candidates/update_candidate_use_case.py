from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class UpdateCandidateUseCase:
    def __init__(self, repo: ICandidateRepository): self.repo = repo

    async def execute(self, candidate_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.repo.update(candidate_id, data)
