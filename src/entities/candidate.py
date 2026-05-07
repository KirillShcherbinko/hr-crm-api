from __future__ import annotations
import uuid
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Candidate:
    id: uuid.UUID
    full_name: str
    email: str
    phone: Optional[str] = None
    resume_url: Optional[str] = None
    created_by: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.full_name or not self.full_name.strip():
            raise ValueError("Full name cannot be empty")
        if not re.match(
                r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.email):
            raise ValueError("Invalid email format")
        if self.phone and not re.match(r"^\+?[1-9]\d{1,14}$", self.phone):
            raise ValueError("Invalid phone format (E.164)")
        if self.resume_url and not self.resume_url.startswith(
                ("http://", "https://")):
            raise ValueError("Resume URL must be a valid HTTP/HTTPS link")

    def update_contact(
            self, phone: Optional[str], resume_url: Optional[str]) -> None:
        self.phone = phone
        self.resume_url = resume_url
        self.updated_at = datetime.now()
        self.validate()
