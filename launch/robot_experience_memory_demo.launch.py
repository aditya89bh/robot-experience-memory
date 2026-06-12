"""Optional ROS2 launch descriptor example.

This file intentionally avoids importing `launch` so it can be inspected in
non-ROS environments. ROS2 users can adapt `demo_configuration()` into a real
LaunchDescription in their own package.
"""

from __future__ import annotations


def demo_configuration() -> dict[str, object]:
    """Return a lightweight description of the demo integration topology."""
    return {
        "nodes": [
            {
                "name": "experience_recorder",
                "topics": ["/robot_experience/outcome", "/robot_experience/replay"],
            },
            {
                "name": "recovery_advisor",
                "services": ["/robot_experience/recover"],
            },
        ],
        "notes": "Adapt this descriptor in a ROS2 package with launch installed.",
    }


def generate_launch_description() -> dict[str, object]:
    """Return a non-ROS placeholder launch description."""
    return demo_configuration()
