from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.candidate import Candidate as CandidateModel
from src.infrastructure.database.models.email import Email
from src.interface_adapters.presenters.mappers import map_candidate, map_email
from src.interface_adapters.repositories.candidate import ICandidateRepository
from .base import BaseRepository


class CandidateRepository(ICandidateRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(
            self, candidate_data: Dict[str, Any], created_by: UUID) -> Dict[str, Any]:
        model = CandidateModel(**candidate_data, created_by=created_by)
        self.session.add(model)
        await self.commit()
        await self.refresh(model)
        return map_candidate(model)

    async def get_by_id(self, candidate_id: UUID) -> Optional[Dict[str, Any]]:
        stmt = select(CandidateModel).where(CandidateModel.id == candidate_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return map_candidate(model) if model else None

    async def list(self, filters: Dict[str, Any], skip: int = 0,
                   limit: int = 50) -> List[Dict[str, Any]]:
        stmt = select(CandidateModel).offset(skip).limit(limit)
        # Фильтрация (пример): if "email" in filters: stmt =
        # stmt.where(CandidateModel.email == filters["email"])
        result = await self.session.execute(stmt)
        return [map_candidate(m) for m in result.scalars().all()]

    async def update(self, candidate_id: UUID,
                     candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(CandidateModel).where(CandidateModel.id == candidate_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("Candidate not found")

        for key, value in candidate_data.items():
            if hasattr(model, key) and key not in (
                    "id", "created_by", "created_at"):
                setattr(model, key, value)
        await self.commit()
        await self.refresh(model)
        return map_candidate(model)

    async def delete(self, candidate_id: UUID) -> None:
        stmt = select(CandidateModel).where(CandidateModel.id == candidate_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.commit()

    async def attach_resume(self, candidate_id: UUID,
                            file_url: str) -> Dict[str, Any]:
        stmt = select(CandidateModel).where(CandidateModel.id == candidate_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("Candidate not found")
        model.resume_url = file_url
        await self.commit()
        await self.refresh(model)
        return map_candidate(model)

    async def detach_resume(self, candidate_id: UUID) -> Dict[str, Any]:
        stmt = select(CandidateModel).where(CandidateModel.id == candidate_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("Candidate not found")
        model.resume_url = None
        await self.commit()
        await self.refresh(model)
        return map_candidate(model)

    async def get_emails_history(
            self, candidate_id: UUID) -> List[Dict[str, Any]]:
        stmt = select(Email).where(
            Email.candidate_id == candidate_id).order_by(
            Email.sent_at.desc())
        result = await self.session.execute(stmt)
        return [map_email(m) for m in result.scalars().all()]
