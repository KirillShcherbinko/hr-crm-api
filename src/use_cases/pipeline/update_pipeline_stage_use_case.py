from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class UpdatePipelineStageUseCase:
    def __init__(self, repo: IPipelineTemplateRepository): self.repo = repo

    async def execute(self, stage_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.repo.update_stage(stage_id, data)
