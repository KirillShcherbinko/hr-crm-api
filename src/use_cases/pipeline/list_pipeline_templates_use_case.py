from typing import Dict, Any, List, Optional
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class ListPipelineTemplatesUseCase:
    def __init__(
        self,
        pipeline_repo: IPipelineTemplateRepository): self.pipeline_repo = pipeline_repo

    async def execute(self) -> List[Dict[str, Any]
                                    ]: return await self.pipeline_repo.list()
