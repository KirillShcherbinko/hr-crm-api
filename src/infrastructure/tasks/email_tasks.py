from .worker import celery_app
from src.infrastructure.email.email_sync import send_email_sync


@celery_app.task
def send_email_task(email: str, subject: str, body: str):
    send_email_sync(email, subject, body)
