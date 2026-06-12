from robot_experience_memory.replay import ReplayEngine
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_replay_preserves_stable_store_order() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))
    store.put(make_bundle("exp-2"))

    events = ReplayEngine(store).replay()
    started_ids = [
        event.experience_id
        for event in events
        if event.event_type == "experience_started"
    ]

    assert started_ids == ["exp-1", "exp-2"]


def test_replay_emits_sequential_bundle_events() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    events = ReplayEngine(store).replay()

    assert [event.event_type for event in events] == [
        "replay_started",
        "experience_started",
        "state_observed",
        "action_replayed",
        "outcome_observed",
        "experience_completed",
        "replay_completed",
    ]
