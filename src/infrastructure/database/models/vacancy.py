from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import VacancyStatus

if TYPE_CHECKING:
    from .user import User
    from .stage import VacancyStage, StageTransition
    from .candidate import Candidate
    from .email import Email


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[VacancyStatus] = mapped_column(
        Enum(VacancyStatus), nullable=False, default=VacancyStatus.draft)
    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    closed_at: Mapped[Optional[datetime.datetime]
                      ] = mapped_column(DateTime, nullable=True)

    creator: Mapped["User"] = relationship(back_populates="created_vacancies")
    stages: Mapped[list["VacancyStage"]] = relationship(
        back_populates="vacancy", cascade="all, delete-orphan")
    candidate_links: Mapped[list["VacancyCandidate"]
                            ] = relationship(back_populates="vacancy")
    emails: Mapped[list["Email"]] = relationship(back_populates="vacancy_link")
    analytics: Mapped[Optional["VacancyAnalytics"]] = relationship(
        back_populates="vacancy", cascade="all, delete-orphan"
    )


class VacancyCandidate(Base):
    __tablename__ = "vacancy_candidates"
    __table_args__ = (
        UniqueConstraint(
            "vacancy_id",
            "candidate_id",
            name="uq_vacancy_candidate"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vacancies.id"), nullable=False)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id"), nullable=False)
    current_stage_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("vacancy_stages.id"), nullable=True)
    assigned_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    assigned_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)

    vacancy: Mapped["Vacancy"] = relationship(back_populates="candidate_links")
    candidate: Mapped["Candidate"] = relationship(
        back_populates="vacancy_links")
    current_stage: Mapped[Optional["VacancyStage"]] = relationship(
        back_populates="current_candidates")
    transitions: Mapped[list["StageTransition"]] = relationship(
        back_populates="vacancy_candidate", cascade="all, delete-orphan")


class VacancyAnalytics(Base):
    __tablename__ = "vacancy_analytics"

    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vacancies.id"), primary_key=True)
    total_candidates: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="0")
    days_open: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    vacancy: Mapped["Vacancy"] = relationship(back_populates="analytics")
