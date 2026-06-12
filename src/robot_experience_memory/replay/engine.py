"""Replay engine for stored robot experience memories."""

import time
from dataclasses import dataclass
from datetime import UTC, datetime

from robot_experience_memory.replay.callbacks import ReplayEventCallback
from robot_experience_memory.replay.config import ReplayConfig
from robot_experience_memory.replay.errors import ReplayCallbackError, ReplayInterrupted
from robot_experience_memory.replay.events import ReplayEvent, ReplayEventType
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
    interrupted: bool = False
    interruption_reason: str | None = None


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
        interrupted = False
        interruption_reason: str | None = None
        self._emit(events, self._create_event("replay_started"))
        try:
            for bundle in self.store.list(filters=filters, pagination=pagination):
                replayed_bundles.append(bundle)
                self._emit(
                    events, self._create_event("experience_started", bundle=bundle)
                )
                if self.config.include_state_events:
                    self._emit(
                        events, self._create_event("state_observed", bundle=bundle)
                    )
                if self.config.include_action_events:
                    self._emit(
                        events, self._create_event("action_replayed", bundle=bundle)
                    )
                if self.config.include_outcome_events:
                    self._emit(
                        events, self._create_event("outcome_observed", bundle=bundle)
                    )
                self._emit(
                    events, self._create_event("experience_completed", bundle=bundle)
                )
                if self.config.stop_on_failure and not bundle.outcome.success:
                    raise ReplayInterrupted(
                        f"experience failed: {bundle.experience_id}"
                    )
                self._sleep_between_experiences()
            self._emit(events, self._create_event("replay_completed"))
        except ReplayInterrupted as exc:
            interrupted = True
            interruption_reason = str(exc)
            self._emit(events, self._create_event("replay_interrupted"))
        duration = time.monotonic() - started
        return ReplayResult(
            events=events,
            statistics=build_statistics(
                replayed_bundles, replay_duration_seconds=duration
            ),
            interrupted=interrupted,
            interruption_reason=interruption_reason,
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
            except ReplayInterrupted:
                raise
            except Exception as exc:  # noqa: BLE001
                raise ReplayCallbackError("replay event callback failed") from exc

    def _create_event(
        self, event_type: ReplayEventType, *, bundle: ExperienceBundle | None = None
    ) -> ReplayEvent:
        """Create an event, using stable timestamps in deterministic mode."""
        timestamp = (
            datetime(1970, 1, 1, tzinfo=UTC)
            if self.config.deterministic
            else None
        )
        return ReplayEvent.create(event_type, bundle=bundle, timestamp=timestamp)
