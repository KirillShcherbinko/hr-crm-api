from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .vacancy import Vacancy, VacancyCandidate


class VacancyStage(Base):
    __tablename__ = "vacancy_stages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vacancies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    is_final: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False)

    vacancy: Mapped["Vacancy"] = relationship(back_populates="stages")
    current_candidates: Mapped[list["VacancyCandidate"]] = relationship(
        back_populates="current_stage", foreign_keys="[VacancyCandidate.current_stage_id]"
    )
    from_transitions: Mapped[list["StageTransition"]] = relationship(
        back_populates="from_stage", foreign_keys="[StageTransition.from_stage_id]"
    )
    to_transitions: Mapped[list["StageTransition"]] = relationship(
        back_populates="to_stage", foreign_keys="[StageTransition.to_stage_id]"
    )


class StageTransition(Base):
    __tablename__ = "stage_transitions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    vacancy_candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vacancy_candidates.id"), nullable=False)
    from_stage_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("vacancy_stages.id"), nullable=True)
    to_stage_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("vacancy_stages.id"), nullable=False)
    moved_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    moved_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)

    vacancy_candidate: Mapped["VacancyCandidate"] = relationship(
        back_populates="transitions")
    from_stage: Mapped[Optional["VacancyStage"]] = relationship(
        "VacancyStage", foreign_keys="[StageTransition.from_stage_id]", back_populates="from_transitions"
    )
    to_stage: Mapped["VacancyStage"] = relationship(
        "VacancyStage", foreign_keys="[StageTransition.to_stage_id]", back_populates="to_transitions"
    )
