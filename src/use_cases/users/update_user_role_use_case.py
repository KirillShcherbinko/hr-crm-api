from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.user import IUserRepository


class UpdateUserRoleUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: UUID, new_role: str) -> Dict[str, Any]:
        return await self.user_repo.update_role(user_id, new_role)
