import pytest

from robot_experience_memory.recorder import (
    ExperienceRecorder,
    RecordContext,
    RecorderHookError,
)
from robot_experience_memory.store import ExperienceBundle, InMemoryStore


def test_recorder_runs_before_and_after_hooks() -> None:
    seen: list[str] = []

    def before(context: RecordContext) -> None:
        seen.append(context.bundle.experience_id)

    def after(bundle: ExperienceBundle) -> None:
        seen.append(bundle.experience_id)

    bundle = ExperienceRecorder(
        InMemoryStore(), before_record_hooks=[before], after_record_hooks=[after]
    ).record(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "arrived"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    )

    assert seen == [bundle.experience_id, bundle.experience_id]


def test_recorder_wraps_hook_failures() -> None:
    def before(_: RecordContext) -> None:
        raise RuntimeError("boom")

    recorder = ExperienceRecorder(InMemoryStore(), before_record_hooks=[before])

    with pytest.raises(RecorderHookError):
        recorder.record(
            state={},
            action={"action_type": "navigate", "command": "move_to"},
            outcome={"success": True, "summary": "arrived"},
            metadata={"robot_id": "robot-a", "environment": "lab"},
        )
