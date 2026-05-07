from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.user import IUserRepository


class GetCurrentUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: UUID) -> Dict[str, Any]:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
