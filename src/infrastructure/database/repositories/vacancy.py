from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.infrastructure.database.models.vacancy import Vacancy as VacancyModel, VacancyStatus
from src.interface_adapters.presenters.mappers import map_vacancy
from src.interface_adapters.repositories.vacancy import IVacancyRepository
from .base import BaseRepository


class VacancyRepository(IVacancyRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(
            self, vacancy_data: Dict[str, Any], created_by: UUID) -> Dict[str, Any]:
        model = VacancyModel(**vacancy_data, created_by=created_by)
        self.session.add(model)
        await self.commit()
        await self.refresh(model)
        return map_vacancy(model)

    async def get_by_id(self, vacancy_id: UUID) -> Optional[Dict[str, Any]]:
        stmt = select(VacancyModel).where(VacancyModel.id == vacancy_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return map_vacancy(model) if model else None

    async def list(self, filters: Dict[str, Any], skip: int = 0,
                   limit: int = 50) -> List[Dict[str, Any]]:
        stmt = select(VacancyModel).offset(skip).limit(limit)
        if "status" in filters:
            stmt = stmt.where(VacancyModel.status == filters["status"])
        result = await self.session.execute(stmt)
        return [map_vacancy(m) for m in result.scalars().all()]

    async def update(self, vacancy_id: UUID,
                     vacancy_data: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(VacancyModel).where(VacancyModel.id == vacancy_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("Vacancy not found")

        for key, value in vacancy_data.items():
            if hasattr(model, key) and key not in (
                    "id", "created_by", "created_at", "status", "closed_at"):
                setattr(model, key, value)
        await self.commit()
        await self.refresh(model)
        return map_vacancy(model)

    async def close(self, vacancy_id: UUID) -> Dict[str, Any]:
        stmt = select(VacancyModel).where(VacancyModel.id == vacancy_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("Vacancy not found")
        model.status = VacancyStatus.closed
        model.closed_at = datetime.now()
        await self.commit()
        await self.refresh(model)
        return map_vacancy(model)

    async def delete(self, vacancy_id: UUID) -> None:
        stmt = select(VacancyModel).where(VacancyModel.id == vacancy_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.commit()
