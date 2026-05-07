from __future__ import annotations
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class EmailStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


@dataclass
class Email:
    id: uuid.UUID
    candidate_id: uuid.UUID
    subject: str
    body: str
    sent_by: uuid.UUID
    status: EmailStatus = EmailStatus.PENDING
    vacancy_id: Optional[uuid.UUID] = None
    sent_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.subject or not self.subject.strip():
            raise ValueError("Email subject cannot be empty")
        if not self.body or not self.body.strip():
            raise ValueError("Email body cannot be empty")

    def mark_sent(self, sent_at: datetime) -> None:
        if self.status != EmailStatus.PENDING:
            raise ValueError("Can only mark pending emails as sent")
        self.status = EmailStatus.SENT
        self.sent_at = sent_at

    def mark_failed(self) -> None:
        if self.status != EmailStatus.PENDING:
            raise ValueError("Can only mark pending emails as failed")
        self.status = EmailStatus.FAILED
