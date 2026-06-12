from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_recorder_adds_non_negative_duration_metric() -> None:
    bundle = ExperienceRecorder(InMemoryStore()).record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    )

    assert "duration_seconds" in bundle.outcome.metrics
    assert bundle.outcome.metrics["duration_seconds"] >= 0.0
