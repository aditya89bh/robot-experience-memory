from robot_experience_memory.replay import (
    ReplayConfig,
    ReplayEngine,
    ReplayEvent,
    ReplayInterrupted,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_replay_stop_on_failure_marks_result_interrupted() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", success=False))
    store.put(make_bundle("exp-2", success=True))

    result = ReplayEngine(store, ReplayConfig(stop_on_failure=True)).replay()

    assert result.interrupted is True
    assert result.interruption_reason == "experience failed: exp-1"
    assert result.events[-1].event_type == "replay_interrupted"


def test_callback_can_interrupt_replay() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    def callback(event: ReplayEvent) -> None:
        if event.event_type == "experience_started":
            raise ReplayInterrupted("operator stopped replay")

    result = ReplayEngine(store, callbacks=[callback]).replay()

    assert result.interrupted is True
    assert result.interruption_reason == "operator stopped replay"
