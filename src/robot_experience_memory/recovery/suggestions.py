"""Recovery suggestion models."""

from typing import Literal

from pydantic import Field, field_validator

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.recovery.traces import RecoveryTrace

SuggestionType = Literal["retry", "fallback", "escalate", "no_action"]


class RecoverySuggestion(MemoryModel):
    """Actionable deterministic recovery suggestion."""

    suggestion_type: SuggestionType
    rationale: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    related_experience_ids: tuple[str, ...] = Field(default_factory=tuple)
    trace: RecoveryTrace | None = None

    @field_validator("rationale")
    @classmethod
    def strip_rationale(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "rationale must be non-empty"
            raise ValueError(msg)
        return stripped
