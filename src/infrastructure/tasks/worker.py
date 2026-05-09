from celery import Celery
from src.config.settings import settings

celery_app = Celery(
    "worker",
    broker=settings.RABBITMQ_URL,
    backend="rpc://"
)

celery_app.autodiscover_tasks(["src.infrastructure.tasks"], force=True)

import src.infrastructure.tasks.tasks  # noqa: F401
