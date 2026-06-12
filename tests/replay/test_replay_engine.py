from robot_experience_memory.replay import ReplayEngine
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_replay_engine_replays_store_bundles_as_events() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    events = ReplayEngine(store).replay().events

    assert [event.event_type for event in events] == [
        "replay_started",
        "experience_started",
        "state_observed",
        "action_replayed",
        "outcome_observed",
        "experience_completed",
        "replay_completed",
    ]
    assert events[1].experience_id == "exp-1"
    assert events[1].bundle is not None
