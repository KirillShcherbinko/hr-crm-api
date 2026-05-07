from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class UpdatePipelineTemplateUseCase:
    def __init__(self, repo: IPipelineTemplateRepository): self.repo = repo

    async def execute(self, template_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.repo.update(template_id, data)
