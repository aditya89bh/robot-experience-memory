"""Record a ROS-style action execution without requiring ROS2 imports."""

from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.ros2 import (
    capture_action_execution,
    rosbag_sensor_reference,
)
from robot_experience_memory.store import InMemoryStore


def main() -> None:
    store = InMemoryStore()
    recorder = ExperienceRecorder(store)
    rosbag_ref = rosbag_sensor_reference(
        "./bags/navigation_run",
        topic="/tf",
        message_type="tf2_msgs/msg/TFMessage",
    )

    bundle = capture_action_execution(
        recorder,
        action_type="navigate",
        robot_id="robot-a",
        environment="demo-lab",
        state={"battery_level": 92.0, "sensor_references": [rosbag_ref]},
        command="navigate_to_pose",
        parameters={"x": 1.0, "y": 2.0, "frame_id": "map"},
        success=True,
        summary="Navigation goal reached",
    )
    print(bundle.experience.experience_id)


if __name__ == "__main__":
    main()
