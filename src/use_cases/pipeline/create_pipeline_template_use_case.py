from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class CreatePipelineTemplateUseCase:
    def __init__(self, repo: IPipelineTemplateRepository): self.repo = repo

    async def execute(self, data: Dict[str, Any],
                      created_by: UUID) -> Dict[str, Any]:
        return await self.repo.create(data, created_by)
