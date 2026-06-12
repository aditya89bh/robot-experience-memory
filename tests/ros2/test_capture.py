from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.ros2 import ROS2ActionCapture, capture_action_execution
from robot_experience_memory.store import InMemoryStore


def test_action_capture_records_execution_with_recorder() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(store)
    capture = ROS2ActionCapture(
        action_type="navigate",
        robot_id="robot-a",
        environment="lab",
        controller="nav2",
    )

    bundle = capture.record_execution(
        recorder,
        state={"battery_level": 91.0},
        command="move_to",
        parameters={"x": 1.0},
        experience_id="exp-action",
    )

    assert bundle.experience.experience_id == "exp-action"
    assert bundle.action.action_type == "navigate"
    assert bundle.action.controller == "nav2"
    assert bundle.metadata.robot_id == "robot-a"
    assert store.get("exp-action") == bundle


def test_capture_action_execution_function_records_failure() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(store)

    bundle = capture_action_execution(
        recorder,
        action_type="dock",
        robot_id="robot-a",
        state={},
        command="dock",
        success=False,
        error_code="dock.failed",
        tags=("ros2", "dock"),
    )

    assert bundle.outcome.success is False
    assert bundle.outcome.error_code == "dock.failed"
    assert "dock" in bundle.metadata.tags
