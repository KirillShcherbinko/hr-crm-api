from uuid import UUID
from src.interface_adapters.repositories.candidate import ICandidateRepository


class DeleteCandidateUseCase:
    def __init__(
        self,
        candidate_repo: ICandidateRepository): self.candidate_repo = candidate_repo

    async def execute(self, candidate_id: UUID) -> None:
        await self.candidate_repo.delete(candidate_id)
