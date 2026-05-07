from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class GetPipelineTemplateUseCase:
    def __init__(self, repo: IPipelineTemplateRepository): self.repo = repo

    async def execute(self, template_id: UUID) -> Dict[str, Any]:
        t = await self.repo.get_by_id(template_id)
        if not t:
            raise ValueError("Template not found")
        return t
