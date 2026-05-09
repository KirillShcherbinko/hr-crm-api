from fastapi import APIRouter
from src.use_cases.emails.send_email_use_case import SendEmailUseCase

router = APIRouter()


@router.post("/send-email")
async def send_email():
    use_case = SendEmailUseCase()

    use_case.execute(
        email="kirill.sherbinko@gmail.com",
        subject="Test",
        body="<h1>Hello</h1>"
    )

    return {"status": "email queued"}
