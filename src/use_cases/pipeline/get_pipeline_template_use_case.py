from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class GetPipelineTemplateUseCase:
    def __init__(
        self,
        pipeline_repo: IPipelineTemplateRepository): self.pipeline_repo = pipeline_repo

    async def execute(self, template_id: UUID) -> Dict[str, Any]:
        t = await self.pipeline_repo.get_by_id(template_id)
        if not t:
            raise ValueError("Template not found")
        return t
