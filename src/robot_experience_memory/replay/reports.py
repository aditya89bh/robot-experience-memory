"""Replay report models."""

from datetime import datetime

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.replay.events import ReplayEvent
from robot_experience_memory.replay.statistics import ReplayStatistics


class ReplayReport(MemoryModel):
    """Summary of a completed or interrupted replay run."""

    started_at: datetime
    completed_at: datetime
    duration_seconds: float
    total_events: int
    total_experiences: int
    success_count: int
    failure_count: int
    interrupted: bool = False
    interruption_reason: str | None = None
    events: list[ReplayEvent]
    statistics: ReplayStatistics
