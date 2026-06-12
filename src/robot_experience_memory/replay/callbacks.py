"""Replay callback types."""

from collections.abc import Callable

from robot_experience_memory.replay.events import ReplayEvent

ReplayEventCallback = Callable[[ReplayEvent], None]
