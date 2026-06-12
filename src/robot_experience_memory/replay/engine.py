"""Replay engine for stored robot experience memories."""

from robot_experience_memory.replay.config import ReplayConfig
from robot_experience_memory.replay.events import ReplayEvent
from robot_experience_memory.store import MemoryStore


class ReplayEngine:
    """Replay stored experience bundles as structured events."""

    def __init__(self, store: MemoryStore, config: ReplayConfig | None = None) -> None:
        self.store = store
        self.config = config or ReplayConfig()

    def replay(self) -> list[ReplayEvent]:
        """Replay all stored bundles and return structured replay events."""
        events = [ReplayEvent.create("replay_started")]
        for bundle in self.store.list():
            events.append(ReplayEvent.create("experience_started", bundle=bundle))
            events.append(ReplayEvent.create("experience_completed", bundle=bundle))
        events.append(ReplayEvent.create("replay_completed"))
        return events
