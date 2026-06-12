"""Recovery policy configuration."""

from pydantic import Field, model_validator

from robot_experience_memory.models.base import MemoryModel


class RecoveryPolicy(MemoryModel):
    """Deterministic thresholds controlling recovery suggestions."""

    max_retries: int = Field(default=1, ge=0)
    escalation_threshold: int = Field(default=3, ge=1)
    minimum_confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_thresholds(self) -> "RecoveryPolicy":
        if self.escalation_threshold <= self.max_retries:
            msg = "escalation_threshold must be greater than max_retries"
            raise ValueError(msg)
        return self
