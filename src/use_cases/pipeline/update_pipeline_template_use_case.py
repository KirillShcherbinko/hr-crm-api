from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class UpdatePipelineTemplateUseCase:
    def __init__(
        self,
        pipeline_repo: IPipelineTemplateRepository): self.pipeline_repo = pipeline_repo

    async def execute(self, template_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.pipeline_repo.update(template_id, data)
