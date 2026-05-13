from typing import Dict, Any, List
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class ApplyTemplateToVacancyUseCase:
    def __init__(
        self,
        pipeline_repo: IPipelineTemplateRepository): self.pipeline_repo = pipeline_repo

    async def execute(self, template_id: UUID,
                      vacancy_id: UUID) -> List[Dict[str, Any]]:
        return await self.pipeline_repo.apply_to_vacancy(template_id, vacancy_id)
