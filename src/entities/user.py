from __future__ import annotations
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    RECRUITER = "recruiter"
    HIRING_MANAGER = "hiring_manager"


@dataclass
class User:
    id: uuid.UUID
    email: str
    full_name: str
    role: UserRole
    is_active: bool = True
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")
        if not self.full_name or not self.full_name.strip():
            raise ValueError("Full name cannot be empty")

    def change_role(self, new_role: UserRole) -> None:
        self.role = new_role

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True
