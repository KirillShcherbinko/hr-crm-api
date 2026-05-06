from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import UserRole

if TYPE_CHECKING:
    from .candidate import Candidate
    from .vacancy import Vacancy
    from .pipeline import PipelineTemplate
    from .email import Email


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)

    created_candidates: Mapped[list["Candidate"]
                               ] = relationship(back_populates="creator")
    created_vacancies: Mapped[list["Vacancy"]
                              ] = relationship(back_populates="creator")
    created_templates: Mapped[list["PipelineTemplate"]
                              ] = relationship(back_populates="creator")
    sent_emails: Mapped[list["Email"]] = relationship(back_populates="sender")
