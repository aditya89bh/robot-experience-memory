from robot_experience_memory.models import (
    ActionRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.ros2 import (
    action_from_execution_event,
    bundle_from_execution_event,
    metadata_from_execution_event,
    outcome_from_execution_event,
    state_from_execution_event,
)
from robot_experience_memory.store import ExperienceBundle


def test_execution_event_adapters_build_models() -> None:
    event = {
        "experience_id": "exp-ros",
        "state": {"state_id": "state-ros", "battery_level": 88.0},
        "action_type": "navigate",
        "command": "move_to",
        "success": False,
        "error_code": "blocked",
        "robot_id": "robot-a",
        "environment": "lab",
        "tags": ("ros2", "navigation"),
    }

    assert isinstance(state_from_execution_event(event), StateSnapshot)
    assert isinstance(action_from_execution_event(event), ActionRecord)
    assert isinstance(outcome_from_execution_event(event), OutcomeRecord)
    assert isinstance(metadata_from_execution_event(event), Metadata)


def test_bundle_from_execution_event_uses_related_model_ids() -> None:
    bundle = bundle_from_execution_event(
        {
            "experience_id": "exp-ros",
            "state": {"state_id": "state-ros"},
            "action": {
                "action_id": "action-ros",
                "action_type": "dock",
                "command": "dock",
            },
            "outcome": {
                "outcome_id": "outcome-ros",
                "success": True,
                "summary": "docked",
            },
            "metadata": {
                "metadata_id": "metadata-ros",
                "robot_id": "robot-a",
                "environment": "lab",
            },
        }
    )

    assert isinstance(bundle, ExperienceBundle)
    assert bundle.experience.experience_id == "exp-ros"
    assert bundle.experience.state_id == "state-ros"
    assert bundle.experience.action_id == "action-ros"
    assert bundle.experience.outcome_id == "outcome-ros"
    assert bundle.experience.metadata_id == "metadata-ros"
