import importlib

import pytest

from robot_experience_memory.ros2 import OptionalDependencyError, availability


def test_ros2_package_imports_without_rclpy() -> None:
    module = importlib.import_module("robot_experience_memory.ros2")

    assert hasattr(module, "is_rclpy_available")


def test_is_rclpy_available_returns_bool() -> None:
    assert isinstance(availability.is_rclpy_available(), bool)


def test_require_rclpy_raises_clear_error_when_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_import_rclpy() -> object:
        raise OptionalDependencyError("missing rclpy")

    monkeypatch.setattr(availability, "import_rclpy", fake_import_rclpy)

    with pytest.raises(OptionalDependencyError, match="missing rclpy"):
        availability.require_rclpy()
