from uuid import UUID
from src.interface_adapters.repositories.vacancy import IVacancyRepository


class DeleteVacancyUseCase:
    def __init__(
        self,
        vacancy_repo: IVacancyRepository): self.vacancy_repo = vacancy_repo

    async def execute(self, vacancy_id: UUID) -> None:
        await self.vacancy_repo.delete(vacancy_id)
