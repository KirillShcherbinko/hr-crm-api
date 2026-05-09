from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.user import RefreshToken
from src.interface_adapters.repositories.auth import IAuthRepository

from .base import BaseRepository


class AuthRepository(IAuthRepository, BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def save_refresh_token(
            self, user_id: UUID, token: str, expires_at: Any) -> None:
        self.session.add(
            RefreshToken(
                user_id=user_id,
                token_hash=token,
                expires_at=expires_at))
        await self.commit()

    async def get_active_token(
            self, token: str) -> Optional[Dict[str, Any]]:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token,
            RefreshToken.is_revoked == False
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return {
            "id": model.id, "user_id": model.user_id, "token_hash": model.token_hash,
            "expires_at": model.expires_at, "created_at": model.created_at, "is_revoked": model.is_revoked
        }

    async def revoke_token(self, token_id: UUID) -> None:
        stmt = select(RefreshToken).where(RefreshToken.id == token_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            model.is_revoked = True
            await self.commit()

    async def revoke_all_by_user(self, user_id: UUID) -> None:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.is_revoked == False)
        result = await self.session.execute(stmt)
        tokens = result.scalars().all()
        for t in tokens:
            t.is_revoked = True
        await self.commit()
