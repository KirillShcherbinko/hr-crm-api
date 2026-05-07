from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class DeletePipelineStageUseCase:
    def __init__(self, repo: IPipelineTemplateRepository): self.repo = repo

    async def execute(self, stage_id: UUID) -> None:
        await self.repo.delete_stage(stage_id)
