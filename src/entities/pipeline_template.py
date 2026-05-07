from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class TemplateStage:
    id: uuid.UUID
    name: str
    order_index: int
    is_final: bool = False

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Template stage name cannot be empty")
        if self.order_index < 0:
            raise ValueError("Order index must be non-negative")


@dataclass
class PipelineTemplate:
    id: uuid.UUID
    name: str
    created_by: uuid.UUID
    created_at: datetime
    stages: List[TemplateStage] = field(default_factory=list)

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Template name cannot be empty")
        if not self.stages:
            raise ValueError("Template must contain at least one stage")
        for stage in self.stages:
            stage.validate()

        orders = [s.order_index for s in self.stages]
        if len(orders) != len(set(orders)):
            raise ValueError("Stage order indices must be unique")
        if orders != sorted(orders):
            raise ValueError(
                "Stages must be provided in correct sequential order")

    def add_stage(self, stage: TemplateStage) -> None:
        self.stages.append(stage)
        self.validate()

    def remove_stage(self, stage_id: uuid.UUID) -> None:
        self.stages = [s for s in self.stages if s.id != stage_id]
        self.validate()
