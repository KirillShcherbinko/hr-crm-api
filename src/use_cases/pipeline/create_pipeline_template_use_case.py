from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class CreatePipelineTemplateUseCase:
    def __init__(
        self,
        pipeline_repo: IPipelineTemplateRepository): self.pipeline_repo = pipeline_repo

    async def execute(self, data: Dict[str, Any],
                      created_by: UUID) -> Dict[str, Any]:
        return await self.pipeline_repo.create(data, created_by)
