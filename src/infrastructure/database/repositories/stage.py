from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.stage import VacancyStage as VacancyStageModel
from src.interface_adapters.presenters.mappers import map_vacancy_stage
from src.interface_adapters.repositories.stage import IVacancyStageRepository
from .base import BaseRepository


class VacancyStageRepository(IVacancyStageRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_by_vacancy(self, vacancy_id: UUID) -> List[Dict[str, Any]]:
        stmt = select(VacancyStageModel).where(
            VacancyStageModel.vacancy_id == vacancy_id).order_by(
            VacancyStageModel.order_index)
        result = await self.session.execute(stmt)
        return [map_vacancy_stage(m) for m in result.scalars().all()]

    async def create(self, vacancy_id: UUID,
                     stage_data: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(VacancyStageModel).where(
            VacancyStageModel.vacancy_id == vacancy_id).order_by(
            VacancyStageModel.order_index.desc()).limit(1)
        res = await self.session.execute(stmt)
        last_stage = res.scalar_one_or_none()
        new_idx = (last_stage.order_index + 1) if last_stage else 0

        model = VacancyStageModel(
            vacancy_id=vacancy_id,
            **stage_data,
            order_index=new_idx)
        self.session.add(model)
        await self.commit()
        await self.refresh(model)
        return map_vacancy_stage(model)

    async def update(self, stage_id: UUID,
                     stage_data: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(VacancyStageModel).where(
            VacancyStageModel.id == stage_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("Stage not found")
        for k, v in stage_data.items():
            if hasattr(model, k):
                setattr(model, k, v)
        await self.commit()
        await self.refresh(model)
        return map_vacancy_stage(model)

    async def delete(self, stage_id: UUID) -> None:
        stmt = select(VacancyStageModel).where(
            VacancyStageModel.id == stage_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.commit()

    async def reorder(self, vacancy_id: UUID,
                      new_order: List[UUID]) -> List[Dict[str, Any]]:
        for idx, stage_id in enumerate(new_order):
            stmt = select(VacancyStageModel).where(
                VacancyStageModel.id == stage_id,
                VacancyStageModel.vacancy_id == vacancy_id)
            res = await self.session.execute(stmt)
            model = res.scalar_one_or_none()
            if model:
                model.order_index = idx
        await self.commit()

        # Возвращаем обновлённый список
        return await self.list_by_vacancy(vacancy_id)
