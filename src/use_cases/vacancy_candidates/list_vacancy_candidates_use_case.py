from typing import Dict, Any, List
from uuid import UUID
from src.interface_adapters.repositories.vacancy_candidate import IVacancyCandidateRepository


class ListVacancyCandidatesUseCase:
    def __init__(
        self,
        vc_repo: IVacancyCandidateRepository): self.vc_repo = vc_repo

    async def execute(self, vacancy_id: UUID) -> List[Dict[str, Any]]:
        return await self.vc_repo.list_by_vacancy(vacancy_id)
