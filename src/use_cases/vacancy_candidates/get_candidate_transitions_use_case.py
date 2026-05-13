from typing import Dict, Any, List
from uuid import UUID
from src.interface_adapters.repositories.vacancy_candidate import IVacancyCandidateRepository


class GetCandidateTransitionsUseCase:
    def __init__(
        self,
        vc_repo: IVacancyCandidateRepository): self.vc_repo = vc_repo

    async def execute(
            self, vacancy_candidate_id: UUID) -> List[Dict[str, Any]]:
        return await self.vc_repo.get_transitions(vacancy_candidate_id)
