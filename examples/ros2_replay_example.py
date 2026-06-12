"""Publish replay events to a ROS2-like publisher without requiring ROS2."""

from robot_experience_memory.replay import ReplayEvent
from robot_experience_memory.ros2 import publish_replay_event


class PrintPublisher:
    """Tiny publisher stand-in for examples and tests."""

    def publish(self, message: object) -> None:
        print(message)


def main() -> None:
    publisher = PrintPublisher()
    publish_replay_event(publisher, ReplayEvent.create("replay_started"))
    publish_replay_event(publisher, ReplayEvent.create("replay_completed"))


if __name__ == "__main__":
    main()
