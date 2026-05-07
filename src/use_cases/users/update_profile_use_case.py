from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.user import IUserRepository


class UpdateUserProfileUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: UUID,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        data.pop("role", None)
        data.pop("is_active", None)
        return await self.user_repo.update_profile(user_id, data)
