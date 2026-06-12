"""Action record model."""

from typing import Any

from pydantic import Field, field_validator

from robot_experience_memory.models.base import MemoryModel


class ActionRecord(MemoryModel):
    """Action executed by the robot."""


    action_id: str = Field(min_length=1)
    action_type: str = Field(min_length=1)
    command: str = Field(min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)
    controller: str | None = Field(default=None, min_length=1)

    @field_validator("action_type", "command")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "action text fields must be non-empty"
            raise ValueError(msg)
        return stripped
