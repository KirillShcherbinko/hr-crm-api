from typing import Dict, Any
from src.interface_adapters.repositories.user import IUserRepository
from src.infrastructure.tasks.tasks import send_email_task
import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateRecruiterUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, full_name: str, email: str,
                      role: str = "recruiter") -> Dict[str, Any]:
        temp_password = secrets.token_urlsafe(12)
        hashed_pw = pwd_context.hash(temp_password)

        user_data = {
            "full_name": full_name,
            "email": email,
            "hashed_password": hashed_pw,
            "role": role}
        created = await self.user_repo.create(user_data)

        # Асинхронная отправка данных для входа
        send_email_task.delay(
            email=email,
            subject="Доступ к HR CRM",
            body=f"Здравствуйте, {full_name}. Ваш логин: {email}, временный пароль: {temp_password}"
        )
        return created
