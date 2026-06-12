"""Replay engine configuration."""

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel


class ReplayConfig(MemoryModel):
    """Configuration controlling replay behavior."""

    speed_multiplier: float = Field(default=1.0, ge=0.0)
    deterministic: bool = False
    include_state_events: bool = True
    include_action_events: bool = True
    include_outcome_events: bool = True
    stop_on_failure: bool = False
