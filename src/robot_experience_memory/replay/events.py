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
        timestamp: datetime | None = None,
    ) -> "ReplayEvent":
        """Create a replay event with a UTC timestamp."""
        data: dict[str, Any] = {
            "event_type": event_type,
            "timestamp": timestamp or utc_now(),
            "bundle": bundle,
        }
        if bundle is not None:
            data["experience_id"] = bundle.experience_id
        return cls.model_validate(data)

    def to_visualization_dict(self) -> dict[str, Any]:
        """Return a JSON-safe replay event shape for future UIs."""
        bundle = self.bundle
        return {
            "event_type": self.event_type,
            "experience_id": self.experience_id,
            "robot_id": bundle.metadata.robot_id if bundle is not None else None,
            "action_type": bundle.action.action_type if bundle is not None else None,
            "success": bundle.outcome.success if bundle is not None else None,
            "timestamp": self.timestamp.isoformat(),
            "summary": bundle.outcome.summary if bundle is not None else None,
        }
