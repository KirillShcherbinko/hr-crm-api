from fastapi_mail import FastMail, MessageSchema
from src.config.email_config import conf

fastmail = FastMail(conf)


async def send_email_async(email: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html"
    )

    await fastmail.send_message(message)
