from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_recorder_adds_success_tag() -> None:
    bundle = ExperienceRecorder(InMemoryStore()).record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a", "environment": "lab", "tags": ("nav",)},
    )

    assert bundle.metadata.tags == ("nav", "success")


def test_recorder_adds_failure_tag() -> None:
    bundle = ExperienceRecorder(InMemoryStore()).record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": False, "summary": "blocked"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    )

    assert bundle.metadata.tags == ("failure",)
