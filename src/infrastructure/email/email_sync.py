import asyncio
from .email_service import send_email_async


def send_email_sync(email: str, subject: str, body: str):
    asyncio.run(send_email_async(email, subject, body))
