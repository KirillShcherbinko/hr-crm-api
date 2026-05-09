from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class CreateCandidateUseCase:
    def __init__(self, candidate_repo: ICandidateRepository):
        self.candidate_repo = candidate_repo

    async def execute(self, data: Dict[str, Any],
                      created_by: UUID) -> Dict[str, Any]:
        return await self.candidate_repo.create(data, created_by)
