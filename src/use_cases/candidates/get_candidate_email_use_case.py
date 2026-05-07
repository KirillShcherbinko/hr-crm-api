from typing import Dict, Any, List
from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class GetCandidateEmailsUseCase:
    def __init__(self, repo: ICandidateRepository): self.repo = repo

    async def execute(self, candidate_id: UUID) -> List[Dict[str, Any]]:
        return await self.repo.get_emails_history(candidate_id)
