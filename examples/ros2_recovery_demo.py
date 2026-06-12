"""Publish deterministic recovery suggestions to a ROS2-like publisher."""

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.recovery import RecoveryEngine
from robot_experience_memory.ros2 import publish_recovery_suggestion
from robot_experience_memory.store import ExperienceBundle, InMemoryStore
from robot_experience_memory.timestamps import utc_now


class PrintPublisher:
    def publish(self, message: object) -> None:
        print(message)


def make_failed_navigation() -> ExperienceBundle:
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id="exp-failed",
            state_id="state-failed",
            action_id="action-failed",
            outcome_id="outcome-failed",
            metadata_id="metadata-failed",
        ),
        state=StateSnapshot(state_id="state-failed"),
        action=ActionRecord(
            action_id="action-failed",
            action_type="navigate",
            command="navigate_to_pose",
        ),
        outcome=OutcomeRecord(
            outcome_id="outcome-failed",
            success=False,
            summary="navigation blocked",
        ),
        metadata=Metadata(
            metadata_id="metadata-failed",
            robot_id="robot-a",
            environment="demo-lab",
            tags=("ros2", "navigation"),
        ),
        stored_at=utc_now(),
    )


def main() -> None:
    store = InMemoryStore()
    failed = make_failed_navigation()
    store.put(failed)

    engine = RecoveryEngine(store)
    suggestion = engine.suggest_recovery(failed)
    publish_recovery_suggestion(PrintPublisher(), suggestion)


if __name__ == "__main__":
    main()
