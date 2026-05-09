from fastapi import APIRouter
from src.infrastructure.tasks.tasks import send_email_task

router = APIRouter()


@router.post("/test-task")
async def test_task():
    send_email_task.delay("test@example.com")
    return {"status": "task sent"}
