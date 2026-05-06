from src.infrastructure.tasks.email_tasks import send_email_task


class SendEmailUseCase:

    def execute(self, email: str, subject: str, body: str):
        send_email_task.delay(email, subject, body)
