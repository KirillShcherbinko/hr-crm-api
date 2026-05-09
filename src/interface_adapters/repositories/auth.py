from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from uuid import UUID


class IAuthRepository(ABC):
    @abstractmethod
    async def save_refresh_token(
        self,
        user_id: UUID,
        token: str,
        expires_at: Any) -> None: ...

    @abstractmethod
    async def get_active_token(self,
                               token: str) -> Optional[Dict[str,
                                                            Any]]: ...

    @abstractmethod
    async def revoke_token(self, token_id: UUID) -> None: ...
    @abstractmethod
    async def revoke_all_by_user(self, user_id: UUID) -> None: ...
