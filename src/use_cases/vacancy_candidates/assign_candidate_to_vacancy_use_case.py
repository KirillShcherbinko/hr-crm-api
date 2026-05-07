from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.vacancy_candidate import IVacancyCandidateRepository


class AssignCandidateToVacancyUseCase:
    def __init__(self, repo: IVacancyCandidateRepository): self.repo = repo

    async def execute(self, vacancy_id: UUID, candidate_id: UUID,
                      assigned_by: UUID) -> Dict[str, Any]:
        return await self.repo.assign(vacancy_id, candidate_id, assigned_by)
