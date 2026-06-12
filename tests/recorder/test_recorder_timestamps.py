from datetime import UTC, datetime

from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_recorder_adds_timezone_aware_recording_timestamps() -> None:
    bundle = ExperienceRecorder(InMemoryStore()).record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    )

    start = datetime.fromtimestamp(
        bundle.outcome.metrics["recorded_start_timestamp"], tz=UTC
    )
    end = datetime.fromtimestamp(
        bundle.outcome.metrics["recorded_end_timestamp"], tz=UTC
    )

    assert start.tzinfo is UTC
    assert end.tzinfo is UTC
    assert bundle.stored_at.tzinfo is UTC
    assert start <= end
