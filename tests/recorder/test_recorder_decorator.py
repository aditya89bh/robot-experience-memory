import pytest

from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore


def test_decorator_records_success_and_preserves_return_value() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(store)

    @recorder.record_function(
        state={},
        action={"action_type": "compute", "command": "plan"},
        metadata={"robot_id": "robot-a", "environment": "sim"},
    )
    def plan() -> int:
        return 42

    assert plan() == 42
    [bundle] = store.list()
    assert bundle.outcome.success is True
    assert plan.__name__ == "plan"


def test_decorator_records_exception_and_reraises() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(store)

    @recorder.record_function(
        state={},
        action={"action_type": "compute", "command": "plan"},
        metadata={"robot_id": "robot-a", "environment": "sim"},
    )
    def fail() -> None:
        raise ValueError("bad plan")

    with pytest.raises(ValueError):
        fail()

    [bundle] = store.list()
    assert bundle.outcome.success is False
    assert bundle.outcome.error_code == "exception.ValueError"
