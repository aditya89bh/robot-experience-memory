from robot_experience_memory.recorder import ExperienceRecorder, SensorReference
from robot_experience_memory.store import InMemoryStore


def test_recorder_stores_sensor_references_without_binary_data() -> None:
    reference = SensorReference(
        name="front_camera",
        uri="file:///tmp/frame-001.jpg",
        media_type="image/jpeg",
        metadata={"frame_id": "front"},
    )

    bundle = ExperienceRecorder(InMemoryStore()).record(
        state={},
        action={"action_type": "inspect", "command": "capture"},
        outcome={"success": True, "summary": "captured"},
        metadata={"robot_id": "robot-a", "environment": "lab"},
        sensor_references=[reference],
    )

    stored_refs = bundle.state.sensor_readings["sensor_references"]
    assert stored_refs[0]["uri"] == "file:///tmp/frame-001.jpg"
    assert bundle.outcome.artifacts == ["file:///tmp/frame-001.jpg"]
