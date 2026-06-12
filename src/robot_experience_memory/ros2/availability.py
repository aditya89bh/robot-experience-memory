"""Availability checks for optional ROS2 dependencies."""

from __future__ import annotations

import importlib.util
from types import ModuleType
from typing import cast

from robot_experience_memory.ros2.errors import OptionalDependencyError


def is_rclpy_available() -> bool:
    """Return whether ``rclpy`` can be imported in this environment."""
    return importlib.util.find_spec("rclpy") is not None


def import_rclpy() -> ModuleType:
    """Import and return ``rclpy`` or raise a clear optional dependency error."""
    try:
        import rclpy  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise OptionalDependencyError(
            "ROS2 support requires the optional 'rclpy' package. "
            "Install ROS2/rclpy or use duck-typed test helpers."
        ) from exc
    return cast(ModuleType, rclpy)


def require_rclpy() -> ModuleType:
    """Return ``rclpy`` when available, otherwise raise OptionalDependencyError."""
    return import_rclpy()
