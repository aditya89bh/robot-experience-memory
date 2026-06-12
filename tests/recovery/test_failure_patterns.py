from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.recovery import FailurePattern, detect_failure_patterns
from robot_experience_memory.store import ExperienceBundle
from tests.store.factories import make_bundle


def with_error(experience_id: str, error_code: str) -> ExperienceBundle:
    bundle = make_bundle(experience_id, success=False)
    return bundle.model_copy(
        update={
            "outcome": OutcomeRecord(
                outcome_id=bundle.outcome.outcome_id,
                success=False,
                summary="failed",
                error_code=error_code,
            )
        }
    )


def test_detect_failure_patterns_by_core_fields() -> None:
    patterns = detect_failure_patterns(
        [with_error("exp-1", "blocked"), with_error("exp-2", "blocked")]
    )

    assert any(
        pattern == FailurePattern(
            field="error_code",
            value="blocked",
            count=2,
            experience_ids=("exp-1", "exp-2"),
        )
        for pattern in patterns
    )
    assert any(
        pattern.field == "action_type" and pattern.value == "navigate"
        for pattern in patterns
    )
    assert any(
        pattern.field == "robot_id" and pattern.value == "robot-a"
        for pattern in patterns
    )


def test_detect_failure_patterns_by_tag_and_ignores_success() -> None:
    patterns = detect_failure_patterns(
        [
            make_bundle("exp-1", success=False, tag="dock"),
            make_bundle("exp-2", success=False, tag="dock"),
            make_bundle("exp-3", success=True, tag="dock"),
        ]
    )

    tag_pattern = next(pattern for pattern in patterns if pattern.field == "tag")
    assert tag_pattern.value == "dock"
    assert tag_pattern.count == 2
