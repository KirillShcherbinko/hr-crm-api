from uuid import UUID
from src.interface_adapters.repositories.vacancy_candidate import IVacancyCandidateRepository


class UnassignCandidateFromVacancyUseCase:
    def __init__(self, repo: IVacancyCandidateRepository): self.repo = repo

    async def execute(self, vacancy_id: UUID, candidate_id: UUID) -> None:
        await self.repo.unassign(vacancy_id, candidate_id)
