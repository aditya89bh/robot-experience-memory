import pytest

from robot_experience_memory.ros2 import (
    LifecycleNodeAdapter,
    OptionalDependencyError,
    lifecycle_state_from_node,
    require_lifecycle_support,
)


class FakeLifecycleNode:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name


def test_lifecycle_adapter_snapshots_fake_node() -> None:
    adapter = LifecycleNodeAdapter(FakeLifecycleNode("memory_node"))

    state = adapter.snapshot("active", reason="configured")

    assert state.node_name == "memory_node"
    assert state.state == "active"
    assert state.details == {"reason": "configured"}


def test_lifecycle_state_from_node_helper() -> None:
    state = lifecycle_state_from_node(FakeLifecycleNode("memory_node"), "inactive")

    assert state.node_name == "memory_node"
    assert state.state == "inactive"


def test_require_lifecycle_support_raises_when_rclpy_missing() -> None:
    with pytest.raises(OptionalDependencyError, match="ROS2 support"):
        require_lifecycle_support()
