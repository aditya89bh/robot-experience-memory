from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from robot_experience_memory.replay import (
    ReplayCallbackError,
    ReplayConfig,
    ReplayEngine,
    ReplayEvent,
    ReplayInterrupted,
    ReplayReport,
)
from robot_experience_memory.store import ExperienceFilter, InMemoryStore, Pagination
from tests.store.factories import make_bundle


def populated_store() -> InMemoryStore:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", robot_id="robot-a", action_type="navigate"))
    store.put(
        make_bundle("exp-2", robot_id="robot-b", action_type="grasp", success=False)
    )
    return store


def test_replay_engine_initialization_and_config_validation() -> None:
    engine = ReplayEngine(populated_store(), ReplayConfig(speed_multiplier=0.0))
    assert engine.config.speed_multiplier == 0.0
    with pytest.raises(ValidationError):
        ReplayConfig(speed_multiplier=-0.1)


def test_comprehensive_replay_order_filtering_and_report() -> None:
    report = ReplayEngine(
        populated_store(), ReplayConfig(speed_multiplier=0.0)
    ).replay(pagination=Pagination(limit=2))

    assert isinstance(report, ReplayReport)
    assert [
        event.experience_id
        for event in report.events
        if event.event_type == "experience_started"
    ] == ["exp-1", "exp-2"]
    assert report.total_experiences == 2
    assert report.success_count == 1
    assert report.failure_count == 1
    assert report.statistics.action_type_counts == {"navigate": 1, "grasp": 1}


def test_comprehensive_event_serialization_and_filtering() -> None:
    report = ReplayEngine(populated_store(), ReplayConfig(speed_multiplier=0.0)).replay(
        filters=ExperienceFilter(success=False)
    )

    event = next(
        event for event in report.events if event.event_type == "experience_started"
    )
    assert event.to_visualization_dict()["success"] is False
    assert report.to_dict()["total_experiences"] == 1


def test_comprehensive_callbacks_determinism_and_interruption(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    calls: list[float] = []
    monkeypatch.setattr(
        "robot_experience_memory.replay.engine.time.sleep", calls.append
    )
    seen: list[str] = []

    def callback(event: ReplayEvent) -> None:
        seen.append(event.event_type)
        if event.event_type == "action_replayed":
            raise ReplayInterrupted("manual stop")

    report = ReplayEngine(
        populated_store(), ReplayConfig(deterministic=True), callbacks=[callback]
    ).replay()

    assert calls == []
    assert report.interrupted is True
    assert report.interruption_reason == "manual stop"
    assert report.started_at == datetime(1970, 1, 1, tzinfo=UTC)
    assert "action_replayed" in seen


def test_comprehensive_callback_error_path() -> None:
    def callback(_: ReplayEvent) -> None:
        raise RuntimeError("bad callback")

    with pytest.raises(ReplayCallbackError):
        ReplayEngine(populated_store(), callbacks=[callback]).replay()
