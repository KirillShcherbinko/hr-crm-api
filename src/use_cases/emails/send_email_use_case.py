from typing import Dict, Any
from uuid import UUID
from src.infrastructure.tasks.tasks import send_email_task
from src.interface_adapters.repositories.email import IEmailRepository


class SendEmailUseCase:
    def __init__(
        self,
        email_repo: IEmailRepository): self.email_repo = email_repo

    async def execute(self, data: Dict[str, Any],
                      sent_by: UUID) -> Dict[str, Any]:
        record = await self.email_repo.send(data, sent_by)
        # Асинхронная отправка
        send_email_task.delay(
            email=data.get("to_email"),
            # предполагается, что email передаётся в data
            subject=data["subject"],
            body=data["body"]
        )
        return record
