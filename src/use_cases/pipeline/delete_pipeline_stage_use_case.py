from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class DeletePipelineStageUseCase:
    def __init__(
        self,
        pipeline_repo: IPipelineTemplateRepository): self.pipeline_repo = pipeline_repo

    async def execute(self, stage_id: UUID) -> None:
        await self.pipeline_repo.delete_stage(stage_id)
