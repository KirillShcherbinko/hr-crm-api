from typing import Dict, Any, List
from src.interface_adapters.repositories.email import IEmailRepository


class ListEmailsUseCase:
    def __init__(
        self,
        email_repo: IEmailRepository): self.email_repo = email_repo

    async def execute(
            self, filters: Dict[str, Any], skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.email_repo.list(filters, skip, limit)
