from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.email import Email as EmailModel, EmailStatus
from src.interface_adapters.presenters.mappers import map_email
from src.interface_adapters.repositories.email import IEmailRepository
from .base import BaseRepository


class EmailRepository(IEmailRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def send(
            self, email_data: Dict[str, Any], sent_by: UUID) -> Dict[str, Any]:
        model = EmailModel(
            **email_data,
            sent_by=sent_by,
            status=EmailStatus.pending)
        self.session.add(model)
        await self.commit()
        await self.refresh(model)
        return map_email(model)

    async def list(self, filters: Dict[str, Any], skip: int = 0,
                   limit: int = 50) -> List[Dict[str, Any]]:
        stmt = select(EmailModel).offset(skip).limit(limit)
        if "candidate_id" in filters:
            stmt = stmt.where(EmailModel.candidate_id
                              == filters["candidate_id"])
        if "vacancy_id" in filters:
            stmt = stmt.where(EmailModel.vacancy_id == filters["vacancy_id"])
        if "status" in filters:
            stmt = stmt.where(EmailModel.status == filters["status"])
        result = await self.session.execute(stmt)
        return [map_email(m) for m in result.scalars().all()]

    async def get_by_id(self, email_id: UUID) -> Optional[Dict[str, Any]]:
        stmt = select(EmailModel).where(EmailModel.id == email_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return map_email(model) if model else None
