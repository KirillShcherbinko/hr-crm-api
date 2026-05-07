from __future__ import annotations
import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Stage:
    id: uuid.UUID
    name: str
    order_index: int
    is_final: bool = False
    vacancy_id: Optional[uuid.UUID] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Stage name cannot be empty")
        if self.order_index < 0:
            raise ValueError("Order index must be non-negative")

    @staticmethod
    def validate_transition(current_index: int, target_index: int,
                            allow_skip: bool = False, allow_backward: bool = False) -> None:
        """Валидация перехода кандидата между этапами согласно требованиям отчёта."""
        if not allow_backward and target_index < current_index:
            raise ValueError("Cannot move candidate backward in the pipeline")
        if not allow_skip and abs(target_index - current_index) > 1:
            raise ValueError("Cannot skip stages in the pipeline")
