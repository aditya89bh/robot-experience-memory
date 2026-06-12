from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_recorder_uses_default_environment() -> None:
    bundle = ExperienceRecorder(
        InMemoryStore(), default_environment="warehouse"
    ).record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a"},
    )

    assert bundle.metadata.environment == "warehouse"


def test_recorder_allows_environment_override() -> None:
    bundle = ExperienceRecorder(
        InMemoryStore(), default_environment="warehouse"
    ).record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a"},
        environment="field",
    )

    assert bundle.metadata.environment == "field"
