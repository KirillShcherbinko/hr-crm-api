from typing import List, Dict, Any
from src.interface_adapters.repositories.user import IUserRepository


class ListUsersUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, skip: int = 0,
                      limit: int = 50) -> List[Dict[str, Any]]:
        return await self.user_repo.list_users(skip, limit)
