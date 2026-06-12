from datetime import UTC, datetime

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.store import ExperienceBundle
from robot_experience_memory.store.filters import ExperienceFilter, Pagination


def make_bundle() -> ExperienceBundle:
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id="exp-1",
            state_id="state-1",
            action_id="action-1",
            outcome_id="outcome-1",
            metadata_id="metadata-1",
        ),
        state=StateSnapshot(state_id="state-1"),
        action=ActionRecord(
            action_id="action-1", action_type="navigate", command="move"
        ),
        outcome=OutcomeRecord(outcome_id="outcome-1", success=True, summary="ok"),
        metadata=Metadata(
            metadata_id="metadata-1",
            robot_id="robot-a",
            environment="lab",
            tags=("nav",),
        ),
        stored_at=datetime(2026, 1, 1, tzinfo=UTC),
    )


def test_filter_matches_bundle_fields() -> None:
    bundle = make_bundle()

    assert ExperienceFilter(robot_id="robot-a", tag="nav", success=True).matches(bundle)
    assert not ExperienceFilter(robot_id="robot-b").matches(bundle)


def test_pagination_applies_limit_and_offset() -> None:
    bundles = [make_bundle(), make_bundle(), make_bundle()]

    assert len(Pagination(limit=1, offset=1).apply(bundles)) == 1
