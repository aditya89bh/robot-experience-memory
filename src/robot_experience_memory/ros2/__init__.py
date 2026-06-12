"""Optional ROS2 integration helpers.

This package is safe to import without ROS2 installed. Helpers that need real
ROS2 APIs perform lazy imports and raise OptionalDependencyError when required.
"""

from robot_experience_memory.ros2.adapters import (
    action_from_execution_event,
    bundle_from_execution_event,
    metadata_from_execution_event,
    outcome_from_execution_event,
    state_from_execution_event,
)
from robot_experience_memory.ros2.availability import (
    import_rclpy,
    is_rclpy_available,
    require_rclpy,
)
from robot_experience_memory.ros2.capture import (
    ROS2ActionCapture,
    capture_action_execution,
)
from robot_experience_memory.ros2.errors import (
    OptionalDependencyError,
    ROS2IntegrationError,
)
from robot_experience_memory.ros2.lifecycle import (
    LifecycleNodeAdapter,
    LifecycleState,
    lifecycle_state_from_node,
    require_lifecycle_support,
)
from robot_experience_memory.ros2.publishers import (
    outcome_to_payload,
    publish_outcome,
    publish_payload,
    publish_recovery_suggestion,
    publish_replay_event,
    recovery_suggestion_to_payload,
    replay_event_to_payload,
)
from robot_experience_memory.ros2.rosbag import (
    RosbagReference,
    rosbag_sensor_reference,
    rosbag_uri,
)

__all__ = [
    "LifecycleNodeAdapter",
    "LifecycleState",
    "OptionalDependencyError",
    "action_from_execution_event",
    "bundle_from_execution_event",
    "capture_action_execution",
    "ROS2ActionCapture",
    "ROS2IntegrationError",
    "RosbagReference",
    "import_rclpy",
    "is_rclpy_available",
    "metadata_from_execution_event",
    "outcome_to_payload",
    "publish_outcome",
    "publish_payload",
    "publish_recovery_suggestion",
    "publish_replay_event",
    "recovery_suggestion_to_payload",
    "lifecycle_state_from_node",
    "replay_event_to_payload",
    "rosbag_sensor_reference",
    "rosbag_uri",
    "require_lifecycle_support",
    "outcome_from_execution_event",
    "require_rclpy",
    "state_from_execution_event",
]
