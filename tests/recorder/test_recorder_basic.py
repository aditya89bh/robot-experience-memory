from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_recorder_records_complete_experience() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(store)

    bundle = recorder.record(
        state={"battery_level": 90.0},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    )

    assert store.get(bundle.experience_id) == bundle
    assert bundle.state.state_id == bundle.experience.state_id
    assert bundle.action.action_type == "navigate"
