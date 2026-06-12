"""Replay engine for stored robot experience memories."""

import time

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
            if self.config.include_state_events:
                events.append(ReplayEvent.create("state_observed", bundle=bundle))
            if self.config.include_action_events:
                events.append(ReplayEvent.create("action_replayed", bundle=bundle))
            if self.config.include_outcome_events:
                events.append(ReplayEvent.create("outcome_observed", bundle=bundle))
            events.append(ReplayEvent.create("experience_completed", bundle=bundle))
            self._sleep_between_experiences()
        events.append(ReplayEvent.create("replay_completed"))
        return events

    def _sleep_between_experiences(self) -> None:
        if self.config.deterministic or self.config.speed_multiplier == 0.0:
            return
        delay_seconds = 1.0 / self.config.speed_multiplier
        time.sleep(delay_seconds)
