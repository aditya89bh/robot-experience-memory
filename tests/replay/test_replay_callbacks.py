import pytest

from robot_experience_memory.replay import (
    ReplayCallbackError,
    ReplayEngine,
    ReplayEvent,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_replay_callbacks_receive_events() -> None:
    seen: list[str] = []
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    def callback(event: ReplayEvent) -> None:
        seen.append(event.event_type)

    ReplayEngine(store, callbacks=[callback]).replay()

    assert seen[0] == "replay_started"
    assert "experience_started" in seen
    assert seen[-1] == "replay_completed"


def test_replay_callback_errors_are_wrapped() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    def callback(_: ReplayEvent) -> None:
        raise RuntimeError("boom")

    with pytest.raises(ReplayCallbackError):
        ReplayEngine(store, callbacks=[callback]).replay()
