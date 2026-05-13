from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class DeletePipelineTemplateUseCase:
    def __init__(
        self,
        pipeline_repo: IPipelineTemplateRepository): self.pipeline_repo = pipeline_repo

    async def execute(self, template_id: UUID) -> None:
        await self.pipeline_repo.delete(template_id)
