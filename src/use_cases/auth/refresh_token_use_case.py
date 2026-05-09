from typing import Dict
import datetime
from passlib.context import CryptContext
from jwt import encode, decode, ExpiredSignatureError
from src.interface_adapters.repositories.auth import IAuthRepository
from src.interface_adapters.repositories.user import IUserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RefreshTokenUseCase:
    def __init__(self, user_repo: IUserRepository, auth_repo: IAuthRepository,
                 secret_key: str, algorithm: str = "HS256", access_exp: int = 30):
        self.user_repo = user_repo
        self.auth_repo = auth_repo
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_exp = access_exp

    async def execute(self, refresh_token: str) -> Dict[str, str]:
        stored = await self.auth_repo.get_active_token(refresh_token)
        if not stored:
            raise ValueError("Invalid or revoked refresh token")

        try:
            payload = decode(
                refresh_token,
                self.secret_key,
                algorithms=[
                    self.algorithm])
        except ExpiredSignatureError:
            raise ValueError("Refresh token expired")

        user = await self.user_repo.get_by_id(payload["sub"])
        if not user or not user["is_active"]:
            raise ValueError("User account is inactive")

        now = datetime.datetime.now(datetime.timezone.utc)
        access_token = encode(
            {
                "sub": str(
                    user["id"]),
                "role": user["role"],
                "exp": now
                + datetime.timedelta(
                    minutes=self.access_exp)},
            self.secret_key,
            self.algorithm)
        return {"access_token": access_token, "token_type": "bearer"}
