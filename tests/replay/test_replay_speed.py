from robot_experience_memory.replay import ReplayConfig, ReplayEngine
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_replay_speed_zero_avoids_sleep(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    calls: list[float] = []
    monkeypatch.setattr(
        "robot_experience_memory.replay.engine.time.sleep", calls.append
    )
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    ReplayEngine(store, ReplayConfig(speed_multiplier=0.0)).replay()

    assert calls == []


def test_replay_speed_uses_inverse_multiplier(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    calls: list[float] = []
    monkeypatch.setattr(
        "robot_experience_memory.replay.engine.time.sleep", calls.append
    )
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    ReplayEngine(store, ReplayConfig(speed_multiplier=2.0)).replay()

    assert calls == [0.5]
