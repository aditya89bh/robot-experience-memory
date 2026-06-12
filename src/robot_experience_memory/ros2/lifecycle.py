"""Optional lifecycle-node helpers for ROS2 workflows."""

from __future__ import annotations

from typing import Any, Protocol

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.ros2.availability import require_rclpy


class LifecycleNodeLike(Protocol):
    """Minimal lifecycle-node protocol used by tests and integrations."""

    def get_name(self) -> str:
        """Return the node name."""


class LifecycleState(MemoryModel):
    """Framework-neutral lifecycle state snapshot."""

    node_name: str = Field(min_length=1)
    state: str = Field(min_length=1)
    details: dict[str, Any] = Field(default_factory=dict)


class LifecycleNodeAdapter:
    """Small adapter around a ROS2 lifecycle node-like object."""

    def __init__(self, node: LifecycleNodeLike) -> None:
        self.node = node

    def snapshot(self, state: str, **details: Any) -> LifecycleState:
        """Capture the node lifecycle state without importing ROS2 APIs."""
        return LifecycleState(
            node_name=self.node.get_name(),
            state=state,
            details=dict(details),
        )


def require_lifecycle_support() -> object:
    """Return rclpy when lifecycle usage needs real ROS2 support."""
    return require_rclpy()


def lifecycle_state_from_node(
    node: LifecycleNodeLike,
    state: str,
    **details: Any,
) -> LifecycleState:
    """Create a lifecycle state snapshot from a node-like object."""
    return LifecycleNodeAdapter(node).snapshot(state, **details)
