from typing import Dict, Any, List
from uuid import UUID
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository


class ApplyTemplateToVacancyUseCase:
    def __init__(self, repo: IPipelineTemplateRepository): self.repo = repo

    async def execute(self, template_id: UUID,
                      vacancy_id: UUID) -> List[Dict[str, Any]]:
        return await self.repo.apply_to_vacancy(template_id, vacancy_id)
