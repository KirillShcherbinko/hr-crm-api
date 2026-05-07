from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]: ...
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[Dict[str, Any]]: ...
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]: ...

    @abstractmethod
    async def list_users(self,
                         skip: int = 0,
                         limit: int = 50) -> List[Dict[str,
                                                       Any]]: ...

    @abstractmethod
    async def update_profile(self,
                             user_id: UUID,
                             data: Dict[str,
                                        Any]) -> Dict[str,
                                                      Any]: ...

    @abstractmethod
    async def update_role(self,
                          user_id: UUID,
                          new_role: str) -> Dict[str,
                                                 Any]: ...

    @abstractmethod
    async def deactivate(self, user_id: UUID) -> None: ...
