"""Duck-typed ROS2 publisher helpers."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any, Protocol

from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.recovery import RecoverySuggestion


class PublisherLike(Protocol):
    """Minimal publisher protocol used by ROS2 helpers."""

    def publish(self, message: object) -> None:
        """Publish a message object."""


MessageFactory = Callable[[Mapping[str, Any]], object]


def outcome_to_payload(outcome: OutcomeRecord) -> dict[str, Any]:
    """Return a JSON-safe payload for an OutcomeRecord."""
    return {
        "outcome_id": outcome.outcome_id,
        "success": outcome.success,
        "summary": outcome.summary,
        "error_code": outcome.error_code,
        "metrics": dict(outcome.metrics),
        "artifacts": list(outcome.artifacts),
    }


def recovery_suggestion_to_payload(
    suggestion: RecoverySuggestion,
) -> dict[str, Any]:
    """Return a JSON-safe payload for a RecoverySuggestion."""
    return {
        "suggestion_type": suggestion.suggestion_type,
        "rationale": suggestion.rationale,
        "confidence": suggestion.confidence,
        "related_experience_ids": list(suggestion.related_experience_ids),
        "trace": suggestion.trace.to_dict() if suggestion.trace is not None else None,
    }


def publish_payload(
    publisher: PublisherLike,
    payload: Mapping[str, Any],
    *,
    message_factory: MessageFactory | None = None,
) -> object:
    """Publish a JSON-safe payload using a duck-typed publisher."""
    message = message_factory(payload) if message_factory is not None else json.dumps(
        payload,
        sort_keys=True,
    )
    publisher.publish(message)
    return message


def publish_outcome(
    publisher: PublisherLike,
    outcome: OutcomeRecord,
    *,
    message_factory: MessageFactory | None = None,
) -> object:
    """Publish an OutcomeRecord as JSON or a caller-provided message object."""
    return publish_payload(
        publisher,
        outcome_to_payload(outcome),
        message_factory=message_factory,
    )


def publish_recovery_suggestion(
    publisher: PublisherLike,
    suggestion: RecoverySuggestion,
    *,
    message_factory: MessageFactory | None = None,
) -> object:
    """Publish a RecoverySuggestion as JSON or a caller-provided message object."""
    return publish_payload(
        publisher,
        recovery_suggestion_to_payload(suggestion),
        message_factory=message_factory,
    )
