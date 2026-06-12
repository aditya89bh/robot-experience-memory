from robot_experience_memory.replay import ReplayEngine
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_replay_tracks_statistics() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", robot_id="robot-a", action_type="navigate"))
    store.put(
        make_bundle(
            "exp-2", robot_id="robot-b", action_type="grasp", success=False
        )
    )

    result = ReplayEngine(store).replay()

    assert result.statistics.total_experiences == 2
    assert result.statistics.success_count == 1
    assert result.statistics.failure_count == 1
    assert result.statistics.action_type_counts == {"navigate": 1, "grasp": 1}
    assert result.statistics.robot_id_counts == {"robot-a": 1, "robot-b": 1}
    assert result.statistics.replay_duration_seconds >= 0.0
