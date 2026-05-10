from typing import Dict, Any, List
from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class GetCandidateEmailsUseCase:
    def __init__(
        self,
        candidate_repo: ICandidateRepository): self.candidate_repo = candidate_repo

    async def execute(self, candidate_id: UUID) -> List[Dict[str, Any]]:
        return await self.candidate_repo.get_emails_history(candidate_id)
