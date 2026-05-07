from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.pipeline import PipelineTemplate as PipelineTemplateModel, PipelineTemplateStage as TemplateStageModel
from src.infrastructure.database.models.stage import VacancyStage as VacancyStageModel
from src.interface_adapters.presenters.mappers import map_template, map_vacancy_stage
from src.interface_adapters.repositories.pipeline import IPipelineTemplateRepository
from .base import BaseRepository


class PipelineTemplateRepository(IPipelineTemplateRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list(self) -> List[Dict[str, Any]]:
        stmt = select(PipelineTemplateModel)
        result = await self.session.execute(stmt)
        return [map_template(m) for m in result.scalars().all()]

    async def get_by_id(self, template_id: UUID) -> Optional[Dict[str, Any]]:
        stmt = select(PipelineTemplateModel).where(
            PipelineTemplateModel.id == template_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return map_template(model, include_stages=True) if model else None

    async def create(self, data: Dict[str, Any],
                     created_by: UUID) -> Dict[str, Any]:
        model = PipelineTemplateModel(**data, created_by=created_by)
        self.session.add(model)
        await self.commit()
        await self.refresh(model)
        return map_template(model)

    async def update(self, template_id: UUID,
                     pipline_data: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(PipelineTemplateModel).where(
            PipelineTemplateModel.id == template_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("Template not found")
        for k, v in pipline_data.items():
            if hasattr(model, k):
                setattr(model, k, v)
        await self.commit()
        await self.refresh(model)
        return map_template(model)

    async def delete(self, template_id: UUID) -> None:
        stmt = select(PipelineTemplateModel).where(
            PipelineTemplateModel.id == template_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.commit()

    async def add_stage(self, template_id: UUID,
                        pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(func.max(TemplateStageModel.order_index)).where(
            TemplateStageModel.template_id == template_id)
        res = await self.session.execute(stmt)
        max_idx = res.scalar() or -1

        model = TemplateStageModel(
            template_id=template_id,
            **pipeline_data,
            order_index=max_idx + 1)
        self.session.add(model)
        await self.commit()
        await self.refresh(model)
        return {"id": model.id, "name": model.name,
                "order_index": model.order_index, "is_final": model.is_final}

    async def update_stage(self, stage_id: UUID,
                           pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(TemplateStageModel).where(
            TemplateStageModel.id == stage_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("Stage not found")
        for k, v in pipeline_data.items():
            if hasattr(model, k):
                setattr(model, k, v)
        await self.commit()
        await self.refresh(model)
        return {"id": model.id, "name": model.name,
                "order_index": model.order_index, "is_final": model.is_final}

    async def delete_stage(self, stage_id: UUID) -> None:
        stmt = select(TemplateStageModel).where(
            TemplateStageModel.id == stage_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.commit()

    async def apply_to_vacancy(
            self, template_id: UUID, vacancy_id: UUID) -> List[Dict[str, Any]]:
        stmt = select(TemplateStageModel).where(
            TemplateStageModel.template_id == template_id).order_by(
            TemplateStageModel.order_index)
        result = await self.session.execute(stmt)
        stages = result.scalars().all()

        created_stages = []
        for s in stages:
            vs = VacancyStageModel(
                vacancy_id=vacancy_id,
                name=s.name,
                order_index=s.order_index,
                is_final=s.is_final)
            self.session.add(vs)
            created_stages.append(vs)

        await self.commit()
        return [map_vacancy_stage(vs) for vs in created_stages]
