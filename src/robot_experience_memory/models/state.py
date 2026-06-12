"""State snapshot model."""

from typing import Any

from pydantic import Field, field_validator

from robot_experience_memory.models.base import MemoryModel


class StateSnapshot(MemoryModel):
    """Robot state captured before action execution."""


    state_id: str = Field(min_length=1)
    joint_positions: dict[str, float] = Field(default_factory=dict)
    pose: dict[str, float] | None = None
    sensor_readings: dict[str, Any] = Field(default_factory=dict)
    battery_level: float | None = Field(default=None, ge=0.0, le=100.0)

    @field_validator("joint_positions", "pose")
    @classmethod
    def require_named_values(
        cls, value: dict[str, float] | None
    ) -> dict[str, float] | None:
        if value is None:
            return value
        if any(not key.strip() for key in value):
            msg = "state value names must be non-empty"
            raise ValueError(msg)
        return value
