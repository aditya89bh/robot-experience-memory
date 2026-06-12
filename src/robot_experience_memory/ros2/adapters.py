"""Adapters for generic ROS-like execution event dictionaries."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from robot_experience_memory.identifiers import generate_experience_id
from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.store import ExperienceBundle
from robot_experience_memory.timestamps import utc_now

ExecutionEvent = Mapping[str, Any]


def _mapping(event: ExecutionEvent, key: str) -> dict[str, Any]:
    value = event.get(key, {})
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def state_from_execution_event(event: ExecutionEvent) -> StateSnapshot:
    """Convert a ROS-like event mapping into a StateSnapshot."""
    data = _mapping(event, "state")
    data.setdefault(
        "state_id", event.get("state_id") or generate_experience_id("state")
    )
    return StateSnapshot.model_validate(data)


def action_from_execution_event(event: ExecutionEvent) -> ActionRecord:
    """Convert a ROS-like event mapping into an ActionRecord."""
    data = _mapping(event, "action")
    data.setdefault(
        "action_id", event.get("action_id") or generate_experience_id("action")
    )
    data.setdefault("action_type", event.get("action_type") or "unknown")
    data.setdefault("command", event.get("command") or data["action_type"])
    return ActionRecord.model_validate(data)


def outcome_from_execution_event(event: ExecutionEvent) -> OutcomeRecord:
    """Convert a ROS-like event mapping into an OutcomeRecord."""
    data = _mapping(event, "outcome")
    data.setdefault(
        "outcome_id", event.get("outcome_id") or generate_experience_id("outcome")
    )
    data.setdefault("success", bool(event.get("success", True)))
    data.setdefault("summary", event.get("summary") or "ROS2 execution event")
    if event.get("error_code") is not None:
        data.setdefault("error_code", event["error_code"])
    return OutcomeRecord.model_validate(data)


def metadata_from_execution_event(event: ExecutionEvent) -> Metadata:
    """Convert a ROS-like event mapping into Metadata."""
    data = _mapping(event, "metadata")
    data.setdefault(
        "metadata_id", event.get("metadata_id") or generate_experience_id("metadata")
    )
    data.setdefault("robot_id", event.get("robot_id") or "unknown-robot")
    data.setdefault("environment", event.get("environment") or "unknown")
    if event.get("operator") is not None:
        data.setdefault("operator", event["operator"])
    if event.get("tags") is not None:
        data.setdefault("tags", tuple(event["tags"]))
    return Metadata.model_validate(data)


def bundle_from_execution_event(event: ExecutionEvent) -> ExperienceBundle:
    """Convert a ROS-like event mapping into an ExperienceBundle."""
    state = state_from_execution_event(event)
    action = action_from_execution_event(event)
    outcome = outcome_from_execution_event(event)
    metadata = metadata_from_execution_event(event)
    experience = ExperienceRecord(
        experience_id=str(event.get("experience_id") or generate_experience_id()),
        state_id=state.state_id,
        action_id=action.action_id,
        outcome_id=outcome.outcome_id,
        metadata_id=metadata.metadata_id,
    )
    return ExperienceBundle(
        experience=experience,
        state=state,
        action=action,
        outcome=outcome,
        metadata=metadata,
        stored_at=utc_now(),
    )
