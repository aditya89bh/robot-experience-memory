from datetime import timedelta

from robot_experience_memory.recovery import (
    RecoveryEvaluationCase,
    evaluate_recovery_cases,
)
from robot_experience_memory.timestamps import utc_now
from tests.store.factories import make_bundle


def test_recovery_evaluation_reports_sequence_metrics() -> None:
    start = utc_now()
    failed = make_bundle("exp-1", success=False, stored_at=start)
    recovered = make_bundle(
        "exp-2", success=True, stored_at=start + timedelta(seconds=1)
    )
    case = RecoveryEvaluationCase(
        name="fast recovery",
        experiences=(failed, recovered),
        failed_experience_id="exp-1",
        expected_suggestion_type="retry",
    )

    metrics = evaluate_recovery_cases([case])

    assert metrics.resolved_sequence_rate == 1.0
    assert metrics.average_sequence_score == 1.0
