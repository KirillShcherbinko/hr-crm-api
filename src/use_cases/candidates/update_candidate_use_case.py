from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class UpdateCandidateUseCase:
    def __init__(
        self,
        candidate_repo: ICandidateRepository): self.candidate_repo = candidate_repo

    async def execute(self, candidate_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.candidate_repo.update(candidate_id, data)
