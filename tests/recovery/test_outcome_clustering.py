from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.recovery import OutcomeCluster, cluster_outcomes
from robot_experience_memory.store import ExperienceBundle
from tests.store.factories import make_bundle


def with_outcome(
    experience_id: str, *, success: bool, error_code: str | None = None
) -> ExperienceBundle:
    bundle = make_bundle(experience_id, success=success)
    return bundle.model_copy(
        update={
            "outcome": OutcomeRecord(
                outcome_id=bundle.outcome.outcome_id,
                success=success,
                summary="ok" if success else "failed",
                error_code=error_code,
            )
        }
    )


def test_cluster_outcomes_by_recovery_relevant_fields() -> None:
    clusters = cluster_outcomes(
        [
            with_outcome("exp-1", success=False, error_code="blocked"),
            with_outcome("exp-2", success=False, error_code="blocked"),
            with_outcome("exp-3", success=True),
        ]
    )

    failed = next(cluster for cluster in clusters if not cluster.success)
    assert failed == OutcomeCluster(
        success=False,
        error_code="blocked",
        action_type="navigate",
        environment="lab",
        count=2,
        experience_ids=("exp-1", "exp-2"),
    )
    assert any(cluster.success for cluster in clusters)
