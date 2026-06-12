"""ROS2 integration error types."""


class ROS2IntegrationError(RuntimeError):
    """Base error for optional ROS2 integration helpers."""


class OptionalDependencyError(ROS2IntegrationError):
    """Raised when an optional ROS2 dependency is required but unavailable."""
