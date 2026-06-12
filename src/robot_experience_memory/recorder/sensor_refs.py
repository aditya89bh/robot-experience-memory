"""Lightweight sensor reference models for recorder captures."""

from datetime import datetime
from typing import Any

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.timestamps import utc_now


class SensorReference(MemoryModel):
    """Reference to external sensor data without embedding binary payloads."""

    name: str = Field(min_length=1)
    uri: str = Field(min_length=1)
    media_type: str | None = None
    timestamp: datetime = Field(default_factory=utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)
