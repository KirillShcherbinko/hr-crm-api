from uuid import UUID
from src.interface_adapters.repositories.vacancy import IVacancyRepository


class DeleteVacancyUseCase:
    def __init__(self, repo: IVacancyRepository): self.repo = repo

    async def execute(self, vacancy_id: UUID) -> None:
        await self.repo.delete(vacancy_id)
