"""Outcome record model."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OutcomeRecord(BaseModel):
    """Execution result produced after a robot action."""

    model_config = ConfigDict(extra="forbid", frozen=True)

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
