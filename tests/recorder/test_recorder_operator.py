from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_recorder_uses_default_operator() -> None:
    bundle = ExperienceRecorder(InMemoryStore(), default_operator="aditya").record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    )

    assert bundle.metadata.operator == "aditya"


def test_recorder_allows_operator_override() -> None:
    bundle = ExperienceRecorder(InMemoryStore(), default_operator="aditya").record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
        operator="teleop",
    )

    assert bundle.metadata.operator == "teleop"
