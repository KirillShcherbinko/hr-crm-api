from uuid import UUID
from src.interface_adapters.repositories.stage import IVacancyStageRepository


class DeleteVacancyStageUseCase:
    def __init__(self, repo: IVacancyStageRepository): self.repo = repo

    async def execute(self, stage_id: UUID) -> None:
        await self.repo.delete(stage_id)
