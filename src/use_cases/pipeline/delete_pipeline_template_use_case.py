from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class DeletePipelineTemplateUseCase:
    def __init__(self, repo: IPipelineTemplateRepository): self.repo = repo

    async def execute(self, template_id: UUID) -> None:
        await self.repo.delete(template_id)
