import pytest
from pydantic import ValidationError

from robot_experience_memory import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)


def test_all_models_round_trip_through_json() -> None:
    models = [
        ExperienceRecord(
            experience_id="exp-1",
            state_id="state-1",
            action_id="action-1",
            outcome_id="outcome-1",
            metadata_id="metadata-1",
        ),
        StateSnapshot(
            state_id="state-1",
            joint_positions={"elbow": 0.2},
            sensor_readings={"range_m": 1.5},
        ),
        ActionRecord(
            action_id="action-1",
            action_type="grasp",
            command="close_gripper",
            parameters={"force": 0.4},
        ),
        OutcomeRecord(
            outcome_id="outcome-1",
            success=True,
            summary="Object grasped",
            metrics={"confidence": 0.91},
        ),
        Metadata(
            metadata_id="metadata-1",
            robot_id="robot-a",
            operator="aditya",
            environment="lab",
            tags=("grasp", "replay"),
        ),
    ]

    for model in models:
        assert type(model).from_json(model.to_json()) == model


def test_models_are_immutable() -> None:
    action = ActionRecord(action_id="action-1", action_type="stop", command="halt")

    with pytest.raises(ValidationError, match="frozen"):
        action.command = "move"
