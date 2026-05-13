from uuid import UUID
from src.interface_adapters.repositories.stage import IVacancyStageRepository


class DeleteVacancyStageUseCase:
    def __init__(
        self,
        stage_repo: IVacancyStageRepository): self.stage_repo = stage_repo

    async def execute(self, stage_id: UUID) -> None:
        await self.stage_repo.delete(stage_id)
