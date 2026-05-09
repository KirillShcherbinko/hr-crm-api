from typing import Dict, Any
from uuid import UUID
from src.interface_adapters.repositories.email import IEmailRepository


class GetEmailUseCase:
    def __init__(
        self,
        email_repo: IEmailRepository): self.email_repo = email_repo

    async def execute(self, email_id: UUID) -> Dict[str, Any]:
        e = await self.email_repo.get_by_id(email_id)
        if not e:
            raise ValueError("Email not found")
        return e
