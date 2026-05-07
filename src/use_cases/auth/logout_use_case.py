from passlib.context import CryptContext
from src.interface_adapters.repositories.auth import IAuthRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LogoutUseCase:
    def __init__(self, auth_repo: IAuthRepository):
        self.auth_repo = auth_repo

    async def execute(self, refresh_token: str) -> None:
        token_hash = pwd_context.hash(refresh_token)
        stored = await self.auth_repo.get_active_token(token_hash)
        if stored:
            await self.auth_repo.revoke_token(stored["id"])
