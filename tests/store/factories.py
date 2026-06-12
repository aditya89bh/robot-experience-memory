from datetime import datetime

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.store import ExperienceBundle
from robot_experience_memory.timestamps import utc_now


def make_bundle(
    experience_id: str = "exp-1",
    *,
    robot_id: str = "robot-a",
    environment: str = "lab",
    operator: str | None = "aditya",
    tag: str = "nav",
    success: bool = True,
    action_type: str = "navigate",
    stored_at: datetime | None = None,
    error_code: str | None = None,
) -> ExperienceBundle:
    suffix = experience_id.removeprefix("exp-")
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id=experience_id,
            state_id=f"state-{suffix}",
            action_id=f"action-{suffix}",
            outcome_id=f"outcome-{suffix}",
            metadata_id=f"metadata-{suffix}",
        ),
        state=StateSnapshot(state_id=f"state-{suffix}"),
        action=ActionRecord(
            action_id=f"action-{suffix}",
            action_type=action_type,
            command="move",
        ),
        outcome=OutcomeRecord(
            outcome_id=f"outcome-{suffix}",
            success=success,
            summary="ok" if success else "failed",
            error_code=error_code,
        ),
        metadata=Metadata(
            metadata_id=f"metadata-{suffix}",
            robot_id=robot_id,
            operator=operator,
            environment=environment,
            tags=(tag,),
        ),
        stored_at=stored_at or utc_now(),
    )
