from pathlib import Path

from robot_experience_memory.recorder import SensorReference
from robot_experience_memory.ros2 import (
    RosbagReference,
    rosbag_sensor_reference,
    rosbag_uri,
)


def test_rosbag_reference_converts_to_sensor_reference() -> None:
    reference = RosbagReference(
        uri="file:///tmp/run.db3",
        topic="/camera/image",
        message_type="sensor_msgs/msg/Image",
        start_time=1.0,
        end_time=2.0,
    )

    sensor = reference.to_sensor_reference()

    assert isinstance(sensor, SensorReference)
    assert sensor.name == "/camera/image"
    assert sensor.media_type == "application/x-rosbag"
    assert sensor.metadata["kind"] == "rosbag"
    assert sensor.metadata["message_type"] == "sensor_msgs/msg/Image"


def test_rosbag_uri_preserves_existing_uri() -> None:
    assert rosbag_uri("s3://bucket/run") == "s3://bucket/run"


def test_rosbag_uri_converts_path_to_file_uri(tmp_path: Path) -> None:
    bag = tmp_path / "run"

    assert rosbag_uri(bag).startswith("file://")


def test_rosbag_sensor_reference_uses_explicit_sensor_id(tmp_path: Path) -> None:
    sensor = rosbag_sensor_reference(
        tmp_path / "run",
        topic="/odom",
        message_type="nav_msgs/msg/Odometry",
        sensor_id="odom-bag",
    )

    assert sensor.name == "odom-bag"
    assert sensor.metadata["topic"] == "/odom"
