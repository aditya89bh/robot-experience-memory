import pytest

from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.recovery import (
    RecoveryEvaluationCase,
    evaluate_recovery_cases,
)
from robot_experience_memory.store import ExperienceBundle
from tests.store.factories import make_bundle


def with_error(bundle: ExperienceBundle, error_code: str) -> ExperienceBundle:
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


def test_recovery_evaluation_metrics() -> None:
    retry_failure = with_error(make_bundle("exp-1", success=False), "blocked")
    fallback_failure = with_error(make_bundle("exp-2", success=False), "blocked")
    escalation_failure = with_error(make_bundle("exp-5", success=False), "blocked")
    cases = [
        RecoveryEvaluationCase(
            name="retry",
            experiences=(retry_failure,),
            failed_experience_id="exp-1",
            expected_suggestion_type="retry",
        ),
        RecoveryEvaluationCase(
            name="fallback",
            experiences=(
                fallback_failure,
                with_error(make_bundle("exp-3", success=False), "blocked"),
                make_bundle("exp-4", success=True, action_type="reroute"),
            ),
            failed_experience_id="exp-2",
            expected_suggestion_type="fallback",
        ),
        RecoveryEvaluationCase(
            name="escalate",
            experiences=(
                escalation_failure,
                with_error(make_bundle("exp-6", success=False), "blocked"),
                with_error(make_bundle("exp-7", success=False), "blocked"),
            ),
            failed_experience_id="exp-5",
            expected_suggestion_type="escalate",
        ),
    ]

    metrics = evaluate_recovery_cases(cases)

    assert metrics.total_cases == 3
    assert metrics.suggested_retry == 1
    assert metrics.suggested_fallback == 1
    assert metrics.suggested_escalation == 1
    assert 0.0 <= metrics.average_confidence <= 1.0
    assert metrics.correct_expected_suggestion_rate == 1.0


def test_recovery_evaluation_requires_failed_experience() -> None:
    case = RecoveryEvaluationCase(
        name="missing",
        experiences=(make_bundle("exp-1", success=False),),
        failed_experience_id="missing",
        expected_suggestion_type="retry",
    )

    with pytest.raises(ValueError, match="failed experience not found"):
        evaluate_recovery_cases([case])
