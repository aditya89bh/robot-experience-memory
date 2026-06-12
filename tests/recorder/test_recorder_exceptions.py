from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_recorder_captures_exception_as_failed_outcome() -> None:
    recorder = ExperienceRecorder(InMemoryStore())
    exception = ValueError("bad waypoint")

    bundle = recorder.capture_exception(
        exception,
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    )

    assert bundle.outcome.success is False
    assert bundle.outcome.error_code == "exception.ValueError"
    assert "bad waypoint" in bundle.outcome.summary
    assert "failure" in bundle.metadata.tags
