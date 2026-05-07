from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.vacancy_candidate import IVacancyCandidateRepository
from src.infrastructure.tasks.worker import recalculate_vacancy_analytics_task


class MoveCandidateStageUseCase:
    def __init__(self, repo: IVacancyCandidateRepository): self.repo = repo

    async def execute(self, vacancy_candidate_id: UUID,
                      new_stage_id: UUID, moved_by: UUID) -> Dict[str, Any]:
        result = await self.repo.move_stage(vacancy_candidate_id, new_stage_id, moved_by)
        # Обновляем аналитику по вакансии асинхронно
        recalculate_vacancy_analytics_task.delay(
            str(vacancy_candidate_id))  # или vacancy_id, если передаётся
        return result
