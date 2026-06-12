"""Smoke tests for optional ROS2 integration surfaces."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import robot_experience_memory
import robot_experience_memory.ros2 as ros2


def test_main_package_and_ros2_helpers_import_without_rclpy() -> None:
    assert robot_experience_memory.__name__ == "robot_experience_memory"
    assert ros2.OptionalDependencyError.__name__ == "OptionalDependencyError"
    assert callable(ros2.capture_action_execution)
    assert callable(ros2.publish_replay_event)
    assert callable(ros2.rosbag_sensor_reference)


def test_ros2_public_exports_are_resolvable() -> None:
    missing = [name for name in ros2.__all__ if not hasattr(ros2, name)]
    assert missing == []


def test_demo_launch_descriptor_is_importable_without_ros2() -> None:
    path = Path("launch/robot_experience_memory_demo.launch.py")
    spec = importlib.util.spec_from_file_location("rem_demo_launch", path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    description = module.generate_launch_description()
    assert description["nodes"][0]["name"] == "experience_recorder"
