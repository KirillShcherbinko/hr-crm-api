from typing import Dict, Any, List, Optional
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class ListPipelineTemplatesUseCase:
    def __init__(self, repo: IPipelineTemplateRepository): self.repo = repo

    async def execute(self) -> List[Dict[str, Any]
                                    ]: return await self.repo.list()
