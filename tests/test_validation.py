import pytest
from pydantic import ValidationError

from robot_experience_memory.models.action import ActionRecord
from robot_experience_memory.models.experience import ExperienceRecord
from robot_experience_memory.models.metadata import Metadata
from robot_experience_memory.models.outcome import OutcomeRecord
from robot_experience_memory.models.state import StateSnapshot


def test_experience_record_rejects_empty_reference() -> None:
    with pytest.raises(ValidationError):
        ExperienceRecord(
            experience_id="exp-1",
            state_id=" ",
            action_id="action-1",
            outcome_id="outcome-1",
            metadata_id="metadata-1",
        )


def test_state_snapshot_rejects_invalid_battery_level() -> None:
    with pytest.raises(ValidationError):
        StateSnapshot(state_id="state-1", battery_level=120.0)


def test_action_record_rejects_blank_command() -> None:
    with pytest.raises(ValidationError):
        ActionRecord(action_id="action-1", action_type="navigate", command=" ")


def test_outcome_record_rejects_blank_summary() -> None:
    with pytest.raises(ValidationError):
        OutcomeRecord(outcome_id="outcome-1", success=False, summary=" ")


def test_metadata_rejects_duplicate_tags() -> None:
    with pytest.raises(ValidationError):
        Metadata(
            metadata_id="metadata-1",
            robot_id="robot-a",
            environment="lab",
            tags=("recovery", "recovery"),
        )


def test_models_reject_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ActionRecord.model_validate(
            {
                "action_id": "action-1",
                "action_type": "navigate",
                "command": "move_to",
                "unknown": True,
            }
        )
