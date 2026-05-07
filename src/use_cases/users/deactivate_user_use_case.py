from uuid import UUID
from src.interface_adapters.repositories.user import IUserRepository


class DeactivateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: UUID) -> None:
        await self.user_repo.deactivate(user_id)
