from robot_experience_memory.recorder import ExperienceRecorder, SensorReference
from robot_experience_memory.store import InMemoryStore


def test_recorder_end_to_end_capture_features() -> None:
    after_seen: list[str] = []
    store = InMemoryStore()
    after_hooks = [lambda bundle: after_seen.append(bundle.experience_id)]
    recorder = ExperienceRecorder(
        store,
        default_environment="lab",
        default_operator="aditya",
        after_record_hooks=after_hooks,
    )

    manual = recorder.record(
        state={},
        action={"action_type": "inspect", "command": "capture"},
        outcome={"success": True, "summary": "ok"},
        metadata={"robot_id": "robot-a"},
        sensor_references=[SensorReference(name="camera", uri="file:///tmp/frame.jpg")],
    )

    assert manual.metadata.environment == "lab"
    assert manual.metadata.operator == "aditya"
    assert "success" in manual.metadata.tags
    assert manual.outcome.metrics["duration_seconds"] >= 0.0
    assert manual.outcome.artifacts == ["file:///tmp/frame.jpg"]
    assert after_seen == [manual.experience_id]

    failure = recorder.capture_exception(
        RuntimeError("blocked"),
        state={},
        action={"action_type": "recover", "command": "retry"},
        metadata={"robot_id": "robot-a"},
    )

    assert failure.outcome.success is False
    assert failure.outcome.error_code == "exception.RuntimeError"
    assert "failure" in failure.metadata.tags
