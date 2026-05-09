from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
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
    analytics: Mapped[Optional["RecruiterAnalytics"]
                      ] = relationship(back_populates="recruiter")
    refresh_tokens: Mapped[list["RefreshToken"]
                           ] = relationship(back_populates="user")


class RecruiterAnalytics(Base):
    __tablename__ = "recruiter_analytics"

    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), primary_key=True)
    open_vacancies_count: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0")
    total_candidates_assigned: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0")
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    recruiter: Mapped["User"] = relationship(back_populates="analytics")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False)
    token_hash: Mapped[str] = mapped_column(
        String(512), nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false")

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
