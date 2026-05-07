from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.user import User as UserModel, UserRole
from src.interface_adapters.presenters.mappers import map_user
from src.interface_adapters.repositories.user import IUserRepository
from .base import BaseRepository


class UserRepository(IUserRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        model = UserModel(**user_data)
        self.session.add(model)
        await self.commit()
        await self.refresh(model)
        return map_user(model)

    async def get_by_id(self, user_id: UUID) -> Optional[Dict[str, Any]]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return map_user(model) if model else None

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return map_user(model) if model else None

    async def list_users(self, skip: int = 0,
                         limit: int = 50) -> List[Dict[str, Any]]:
        stmt = select(UserModel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return [map_user(m) for m in result.scalars().all()]

    async def update_profile(
            self, user_id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("User not found")
        for k, v in data.items():
            if hasattr(model, k) and k not in ("id", "role", "created_at"):
                setattr(model, k, v)
        await self.commit()
        await self.refresh(model)
        return map_user(model)

    async def update_role(self, user_id: UUID,
                          new_role: str) -> Dict[str, Any]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError("User not found")
        model.role = UserRole(new_role)
        await self.commit()
        await self.refresh(model)
        return map_user(model)

    async def deactivate(self, user_id: UUID) -> None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.is_active = False
            await self.commit()
