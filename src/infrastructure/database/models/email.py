from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import EmailStatus

if TYPE_CHECKING:
    from .candidate import Candidate
    from .vacancy import Vacancy
    from .user import User


class Email(Base):
    __tablename__ = "emails"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False
    )
    vacancy_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        nullable=True
    )
    sent_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)
    status: Mapped[EmailStatus] = mapped_column(
        Enum(EmailStatus), nullable=False, default=EmailStatus.pending)

    candidate: Mapped["Candidate"] = relationship(back_populates="emails")
    vacancy_link: Mapped[Optional["Vacancy"]
                         ] = relationship(back_populates="emails")
    sender: Mapped["User"] = relationship(back_populates="sent_emails")
