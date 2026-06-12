from robot_experience_memory.replay import ReplayEngine
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_replay_event_visualization_dict_is_json_safe() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", robot_id="robot-a", action_type="navigate"))

    event = ReplayEngine(store).replay().events[1]
    data = event.to_visualization_dict()

    assert data == {
        "event_type": "experience_started",
        "experience_id": "exp-1",
        "robot_id": "robot-a",
        "action_type": "navigate",
        "success": True,
        "timestamp": event.timestamp.isoformat(),
        "summary": "ok",
    }
