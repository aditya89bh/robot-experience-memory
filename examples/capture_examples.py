"""Runnable examples for experience capture APIs."""

from robot_experience_memory.recorder import ExperienceRecorder, SensorReference
from robot_experience_memory.store import InMemoryStore


def main() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(
        store,
        default_environment="lab",
        default_operator="example-operator",
    )

    recorder.record(
        state={"battery_level": 95.0},
        action={"action_type": "navigate", "command": "move_to"},
        outcome={"success": True, "summary": "manual record complete"},
        metadata={"robot_id": "robot-a", "tags": ("manual",)},
    )

    with recorder.capture(
        state={},
        action={"action_type": "grasp", "command": "close_gripper"},
        metadata={"robot_id": "robot-a", "tags": ("context",)},
    ):
        pass

    @recorder.record_function(
        state={},
        action={"action_type": "compute", "command": "plan_path"},
        metadata={"robot_id": "robot-a", "tags": ("decorator",)},
    )
    def plan_path() -> str:
        return "path-ready"

    plan_path()

    try:
        with recorder.capture(
            state={},
            action={"action_type": "recover", "command": "retry"},
            metadata={"robot_id": "robot-a", "tags": ("exception",)},
        ):
            raise RuntimeError("simulated recovery failure")
    except RuntimeError:
        pass

    recorder.record(
        state={},
        action={"action_type": "inspect", "command": "capture_frame"},
        outcome={"success": True, "summary": "sensor reference captured"},
        metadata={"robot_id": "robot-a", "tags": ("sensor",)},
        sensor_references=[
            SensorReference(
                name="front_camera",
                uri="file:///tmp/front-camera-frame.jpg",
                media_type="image/jpeg",
            )
        ],
    )

    print(f"captured {len(store.list())} experiences")


if __name__ == "__main__":
    main()
