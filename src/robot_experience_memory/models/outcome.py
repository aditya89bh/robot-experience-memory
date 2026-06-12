"""Outcome record model."""

from pydantic import Field, field_validator

from robot_experience_memory.models.base import MemoryModel


class OutcomeRecord(MemoryModel):
    """Execution result produced after a robot action."""


    outcome_id: str = Field(min_length=1)
    success: bool
    summary: str = Field(min_length=1)
    error_code: str | None = Field(default=None, min_length=1)
    metrics: dict[str, float] = Field(default_factory=dict)
    artifacts: list[str] = Field(default_factory=list)

    @field_validator("summary")
    @classmethod
    def strip_summary(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "summary must be non-empty"
            raise ValueError(msg)
        return stripped
