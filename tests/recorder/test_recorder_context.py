import pytest

from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_context_manager_records_success() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(store)

    with recorder.capture(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    ) as capture:
        pass

    assert capture.bundle is not None
    assert capture.bundle.outcome.success is True
    assert store.get(capture.bundle.experience_id) == capture.bundle


def test_context_manager_records_exception_and_reraises() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(store)

    with pytest.raises(RuntimeError), recorder.capture(
        state={},
        action={"action_type": "navigate", "command": "move_to"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
    ):
        raise RuntimeError("blocked")

    [bundle] = store.list()
    assert bundle.outcome.success is False
    assert bundle.outcome.error_code == "exception.RuntimeError"
