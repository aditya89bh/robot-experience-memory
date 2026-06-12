"""Replay engine for stored robot experience memories."""

import time
from dataclasses import dataclass

from robot_experience_memory.replay.callbacks import ReplayEventCallback
from robot_experience_memory.replay.config import ReplayConfig
from robot_experience_memory.replay.errors import ReplayCallbackError
from robot_experience_memory.replay.events import ReplayEvent
from robot_experience_memory.replay.statistics import ReplayStatistics, build_statistics
from robot_experience_memory.store import (
    ExperienceBundle,
    ExperienceFilter,
    MemoryStore,
    Pagination,
)


@dataclass(frozen=True)
class ReplayResult:
    """Replay events plus aggregate statistics."""

    events: list[ReplayEvent]
    statistics: ReplayStatistics


class ReplayEngine:
    """Replay stored experience bundles as structured events."""

    def __init__(
        self,
        store: MemoryStore,
        config: ReplayConfig | None = None,
        callbacks: list[ReplayEventCallback] | None = None,
    ) -> None:
        self.store = store
        self.config = config or ReplayConfig()
        self.callbacks = callbacks or []

    def replay(
        self,
        *,
        filters: ExperienceFilter | None = None,
        pagination: Pagination | None = None,
    ) -> ReplayResult:
        """Replay selected stored bundles and return events with statistics."""
        started = time.monotonic()
        replayed_bundles: list[ExperienceBundle] = []
        events: list[ReplayEvent] = []
        self._emit(events, ReplayEvent.create("replay_started"))
        for bundle in self.store.list(filters=filters, pagination=pagination):
            replayed_bundles.append(bundle)
            self._emit(events, ReplayEvent.create("experience_started", bundle=bundle))
            if self.config.include_state_events:
                self._emit(events, ReplayEvent.create("state_observed", bundle=bundle))
            if self.config.include_action_events:
                self._emit(events, ReplayEvent.create("action_replayed", bundle=bundle))
            if self.config.include_outcome_events:
                self._emit(
                    events, ReplayEvent.create("outcome_observed", bundle=bundle)
                )
            self._emit(
                events, ReplayEvent.create("experience_completed", bundle=bundle)
            )
            self._sleep_between_experiences()
        self._emit(events, ReplayEvent.create("replay_completed"))
        duration = time.monotonic() - started
        return ReplayResult(
            events=events,
            statistics=build_statistics(
                replayed_bundles, replay_duration_seconds=duration
            ),
        )

    def _sleep_between_experiences(self) -> None:
        if self.config.deterministic or self.config.speed_multiplier == 0.0:
            return
        delay_seconds = 1.0 / self.config.speed_multiplier
        time.sleep(delay_seconds)

    def _emit(self, events: list[ReplayEvent], event: ReplayEvent) -> None:
        events.append(event)
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as exc:  # noqa: BLE001
                raise ReplayCallbackError("replay event callback failed") from exc
