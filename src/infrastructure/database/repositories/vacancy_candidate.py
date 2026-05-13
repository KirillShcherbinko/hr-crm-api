from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.vacancy import VacancyCandidate as VacancyCandidateModel
from src.infrastructure.database.models.stage import StageTransition, VacancyStage as VacancyStageModel
from src.interface_adapters.presenters.mappers import map_transition, map_vacancy_candidate
from src.interface_adapters.repositories.vacancy_candidate import IVacancyCandidateRepository
from .base import BaseRepository


class VacancyCandidateRepository(IVacancyCandidateRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_by_vacancy(self, vacancy_id: UUID) -> List[Dict[str, Any]]:
        stmt = select(VacancyCandidateModel).where(
            VacancyCandidateModel.vacancy_id == vacancy_id)
        result = await self.session.execute(stmt)
        return [map_vacancy_candidate(m) for m in result.scalars().all()]

    async def assign(self, vacancy_id: UUID, candidate_id: UUID,
                     assigned_by: UUID) -> Dict[str, Any]:
        # Находим начальный этап (order_index = 0)
        stmt_stage = select(VacancyStageModel).where(
            VacancyStageModel.vacancy_id == vacancy_id, VacancyStageModel.order_index == 0
        ).limit(1)
        res = await self.session.execute(stmt_stage)
        initial_stage = res.scalar_one_or_none()

        model = VacancyCandidateModel(
            vacancy_id=vacancy_id, candidate_id=candidate_id,
            assigned_by=assigned_by, current_stage_id=initial_stage.id if initial_stage else None
        )
        self.session.add(model)
        await self.commit()
        await self.refresh(model)
        return map_vacancy_candidate(model)

    async def unassign(self, vacancy_id: UUID, candidate_id: UUID) -> None:
        stmt = select(VacancyCandidateModel).where(
            VacancyCandidateModel.vacancy_id == vacancy_id,
            VacancyCandidateModel.candidate_id == candidate_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.commit()

        # ... остальные методы ...

    async def get_by_id(
            self, link_id: UUID) -> Optional[VacancyCandidateModel]:
        """Поиск записи связи по её первичному ключу (PK vacancy_candidates)"""
        stmt = select(VacancyCandidateModel).where(
            VacancyCandidateModel.id == link_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def move_stage(self, vacancy_candidate_id: UUID,
                         new_stage_id: UUID, moved_by: UUID) -> Dict[str, Any]:
        stmt = select(VacancyCandidateModel).where(
            VacancyCandidateModel.id == vacancy_candidate_id)
        result = await self.session.execute(stmt)
        vc = result.scalar_one_or_none()
        if not vc:
            raise ValueError("Vacancy-Candidate link not found")

        old_stage_id = vc.current_stage_id
        vc.current_stage_id = new_stage_id

        transition = StageTransition(
            vacancy_candidate_id=vc.id, from_stage_id=old_stage_id,
            to_stage_id=new_stage_id, moved_by=moved_by, moved_at=datetime.now()
        )
        self.session.add(transition)
        await self.commit()
        await self.refresh(vc)
        return map_vacancy_candidate(vc)

    async def get_by_vacancy_and_candidate(
            self, vacancy_id: UUID, candidate_id: UUID):
        stmt = select(VacancyCandidateModel).where(
            VacancyCandidateModel.vacancy_id == vacancy_id,
            VacancyCandidateModel.candidate_id == candidate_id
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_transitions(
            self, vacancy_candidate_id: UUID) -> List[Dict[str, Any]]:
        stmt = select(StageTransition).where(
            StageTransition.vacancy_candidate_id == vacancy_candidate_id).order_by(
            StageTransition.moved_at)
        result = await self.session.execute(stmt)
        return [map_transition(m) for m in result.scalars().all()]
