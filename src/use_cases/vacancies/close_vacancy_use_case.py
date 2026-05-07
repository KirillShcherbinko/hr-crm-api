from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.vacancy import IVacancyRepository
from src.infrastructure.tasks.worker import recalculate_vacancy_analytics_task


class CloseVacancyUseCase:
    def __init__(self, vacancy_repo: IVacancyRepository):
        self.vacancy_repo = vacancy_repo

    async def execute(self, vacancy_id: UUID) -> Dict[str, Any]:
        updated = await self.vacancy_repo.close(vacancy_id)
        recalculate_vacancy_analytics_task.delay(str(vacancy_id))
        return updated
