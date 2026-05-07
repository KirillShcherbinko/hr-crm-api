from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class DeleteCandidateUseCase:
    def __init__(self, repo: ICandidateRepository): self.repo = repo

    async def execute(self, candidate_id: UUID) -> None:
        await self.repo.delete(candidate_id)
