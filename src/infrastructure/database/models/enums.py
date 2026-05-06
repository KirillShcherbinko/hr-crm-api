import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    recruiter = "recruiter"


class VacancyStatus(str, enum.Enum):
    draft = "draft"
    open = "open"
    closed = "closed"


class EmailStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"
