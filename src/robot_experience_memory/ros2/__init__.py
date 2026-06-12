"""Optional ROS2 integration helpers.

This package is safe to import without ROS2 installed. Helpers that need real
ROS2 APIs perform lazy imports and raise OptionalDependencyError when required.
"""

from robot_experience_memory.ros2.availability import (
    import_rclpy,
    is_rclpy_available,
    require_rclpy,
)
from robot_experience_memory.ros2.errors import (
    OptionalDependencyError,
    ROS2IntegrationError,
)

__all__ = [
    "OptionalDependencyError",
    "ROS2IntegrationError",
    "import_rclpy",
    "is_rclpy_available",
    "require_rclpy",
]
