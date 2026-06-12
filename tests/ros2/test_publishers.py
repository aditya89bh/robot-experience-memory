import json

from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.recovery import RecoverySuggestion
from robot_experience_memory.ros2 import (
    outcome_to_payload,
    publish_outcome,
    publish_recovery_suggestion,
)


class FakePublisher:
    def __init__(self) -> None:
        self.messages: list[object] = []

    def publish(self, message: object) -> None:
        self.messages.append(message)


def test_publish_outcome_uses_json_payload_by_default() -> None:
    publisher = FakePublisher()
    outcome = OutcomeRecord(
        outcome_id="outcome-1",
        success=False,
        summary="blocked",
        error_code="blocked",
    )

    message = publish_outcome(publisher, outcome)

    assert publisher.messages == [message]
    assert json.loads(str(message))["success"] is False
    assert outcome_to_payload(outcome)["error_code"] == "blocked"


def test_publish_outcome_accepts_message_factory() -> None:
    publisher = FakePublisher()
    outcome = OutcomeRecord(outcome_id="outcome-1", success=True, summary="ok")

    message = publish_outcome(
        publisher,
        outcome,
        message_factory=lambda payload: {"wrapped": payload["outcome_id"]},
    )

    assert message == {"wrapped": "outcome-1"}
    assert publisher.messages == [message]


def test_publish_recovery_suggestion() -> None:
    publisher = FakePublisher()
    suggestion = RecoverySuggestion(
        suggestion_type="retry",
        rationale="transient failure",
        confidence=0.7,
    )

    message = publish_recovery_suggestion(publisher, suggestion)

    assert json.loads(str(message))["suggestion_type"] == "retry"
    assert publisher.messages == [message]
