from __future__ import annotations
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class VacancyStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"


@dataclass
class Vacancy:
    id: uuid.UUID
    title: str
    status: VacancyStatus = VacancyStatus.DRAFT
    description: Optional[str] = None
    created_by: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Vacancy title cannot be empty")

    def publish(self) -> None:
        if self.status != VacancyStatus.DRAFT:
            raise ValueError("Vacancy can only be published from draft status")
        self.status = VacancyStatus.OPEN
        self.updated_at = datetime.now()

    def close(self) -> None:
        if self.status not in (VacancyStatus.OPEN, VacancyStatus.DRAFT):
            raise ValueError("Can only close open or draft vacancies")
        self.status = VacancyStatus.CLOSED
        self.closed_at = datetime.now()
        self.updated_at = datetime.now()

    def update_details(
            self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now()
        self.validate()
