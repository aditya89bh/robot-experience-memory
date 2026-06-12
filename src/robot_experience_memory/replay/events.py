"""Structured replay event models."""

from datetime import datetime
from typing import Any, Literal

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store import ExperienceBundle
from robot_experience_memory.timestamps import utc_now

ReplayEventType = Literal[
    "replay_started",
    "experience_started",
    "state_observed",
    "action_replayed",
    "outcome_observed",
    "experience_completed",
    "replay_completed",
]


class ReplayEvent(MemoryModel):
    """A structured event emitted by the replay engine."""

    event_type: ReplayEventType
    timestamp: datetime
    experience_id: str | None = None
    bundle: ExperienceBundle | None = None

    @classmethod
    def create(
        cls,
        event_type: ReplayEventType,
        *,
        bundle: ExperienceBundle | None = None,
    ) -> "ReplayEvent":
        """Create a replay event with a UTC timestamp."""
        data: dict[str, Any] = {
            "event_type": event_type,
            "timestamp": utc_now(),
            "bundle": bundle,
        }
        if bundle is not None:
            data["experience_id"] = bundle.experience_id
        return cls.model_validate(data)
