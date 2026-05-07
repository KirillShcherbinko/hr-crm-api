import datetime
from typing import Dict
from passlib.context import CryptContext
from jwt import encode
from src.interface_adapters.repositories.auth import IAuthRepository
from src.interface_adapters.repositories.user import IUserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginUseCase:
    def __init__(self, user_repo: IUserRepository, auth_repo: IAuthRepository, secret_key: str,
                 algorithm: str = "HS256", access_exp: int = 30, refresh_exp: int = 1440):
        self.user_repo = user_repo
        self.auth_repo = auth_repo
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_exp = access_exp
        self.refresh_exp = refresh_exp

    async def execute(self, email: str, password: str) -> Dict[str, str]:
        user = await self.user_repo.get_by_email(email)
        if not user or not user["is_active"]:
            raise ValueError("Invalid credentials or account inactive")

        if not pwd_context.verify(password, user["hashed_password"]):
            raise ValueError("Invalid credentials")

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

        refresh_token = encode(
            {
                "sub": str(
                    user["id"]),
                "exp": now
                + datetime.timedelta(
                    minutes=self.refresh_exp)},
            self.secret_key,
            self.algorithm)
        refresh_token_hash = pwd_context.hash(refresh_token)

        await self.auth_repo.save_refresh_token(user["id"], refresh_token_hash, now + datetime.timedelta(minutes=self.refresh_exp))

        return {"access_token": access_token,
                "refresh_token": refresh_token, "token_type": "bearer"}
