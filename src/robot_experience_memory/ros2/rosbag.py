"""Rosbag interoperability helpers.

These helpers only create references/metadata. They intentionally do not parse or
open rosbag files, keeping ROS2 optional and lightweight.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.recorder import SensorReference


class RosbagReference(MemoryModel):
    """Reference to a rosbag resource associated with an experience."""

    uri: str = Field(min_length=1)
    topic: str | None = None
    message_type: str | None = None
    start_time: float | None = None
    end_time: float | None = None
    description: str | None = None

    def to_sensor_reference(self, *, sensor_id: str | None = None) -> SensorReference:
        """Represent this rosbag as a generic SensorReference."""
        metadata = {
            "kind": "rosbag",
            "uri": self.uri,
            "topic": self.topic,
            "message_type": self.message_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }
        if self.description is not None:
            metadata["description"] = self.description
        return SensorReference(
            name=sensor_id or self.topic or "rosbag",
            uri=self.uri,
            media_type="application/x-rosbag",
            metadata={
                key: value for key, value in metadata.items() if value is not None
            },
        )

    def to_artifact(self) -> dict[str, object]:
        """Represent this rosbag as an outcome artifact payload."""
        return {
            "kind": "rosbag",
            "uri": self.uri,
            "topic": self.topic,
            "message_type": self.message_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description,
        }


def rosbag_uri(path_or_uri: str | Path) -> str:
    """Return a normalized URI for a rosbag path or URI."""
    value = str(path_or_uri)
    if "://" in value:
        return value
    return Path(value).expanduser().resolve().as_uri()


def rosbag_sensor_reference(
    path_or_uri: str | Path,
    *,
    topic: str | None = None,
    message_type: str | None = None,
    sensor_id: str | None = None,
    description: str | None = None,
) -> SensorReference:
    """Create a SensorReference for a rosbag path or URI."""
    return RosbagReference(
        uri=rosbag_uri(path_or_uri),
        topic=topic,
        message_type=message_type,
        description=description,
    ).to_sensor_reference(sensor_id=sensor_id)
