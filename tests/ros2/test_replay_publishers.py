import json

from robot_experience_memory.replay import ReplayEvent
from robot_experience_memory.ros2 import publish_replay_event, replay_event_to_payload
from tests.store.factories import make_bundle


class FakePublisher:
    def __init__(self) -> None:
        self.messages: list[object] = []

    def publish(self, message: object) -> None:
        self.messages.append(message)


def test_replay_event_to_payload_is_json_safe() -> None:
    event = ReplayEvent.create("experience_started", bundle=make_bundle("exp-1"))

    payload = replay_event_to_payload(event)

    assert payload["event_type"] == "experience_started"
    assert payload["experience_id"] == "exp-1"
    json.dumps(payload)


def test_publish_replay_event_publishes_json_by_default() -> None:
    publisher = FakePublisher()
    event = ReplayEvent.create("replay_started")

    message = publish_replay_event(publisher, event)

    assert publisher.messages == [message]
    assert json.loads(str(message))["event_type"] == "replay_started"


def test_publish_replay_event_accepts_message_factory() -> None:
    publisher = FakePublisher()
    event = ReplayEvent.create("replay_completed")

    message = publish_replay_event(
        publisher,
        event,
        message_factory=lambda payload: (payload["event_type"],),
    )

    assert message == ("replay_completed",)
    assert publisher.messages == [message]
