from datetime import UTC, datetime

from robot_experience_memory.replay import ReplayConfig, ReplayEngine
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_deterministic_replay_uses_stable_event_timestamps() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    result = ReplayEngine(store, ReplayConfig(deterministic=True)).replay()

    assert {event.timestamp for event in result.events} == {
        datetime(1970, 1, 1, tzinfo=UTC)
    }


def test_deterministic_replay_avoids_sleep(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    calls: list[float] = []
    monkeypatch.setattr(
        "robot_experience_memory.replay.engine.time.sleep", calls.append
    )
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    ReplayEngine(store, ReplayConfig(deterministic=True)).replay()

    assert calls == []
