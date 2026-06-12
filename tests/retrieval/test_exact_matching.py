from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalQuery,
    exact_match_score,
)
from robot_experience_memory.store import ExperienceBundle, InMemoryStore
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


def test_exact_match_scores_selected_fields() -> None:
    bundle = with_error(make_bundle("exp-1", success=False), "blocked")
    query = RetrievalQuery(
        action_type="navigate",
        robot_id="robot-a",
        environment="lab",
        success=False,
        error_code="blocked",
    )

    assert exact_match_score(query, bundle) == 1.0


def test_exact_match_scores_partial_mismatch() -> None:
    bundle = make_bundle("exp-1", success=True, action_type="navigate")
    query = RetrievalQuery(action_type="navigate", success=False)

    assert exact_match_score(query, bundle) == 0.5


def test_engine_uses_exact_match_scores() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", success=True, action_type="navigate"))

    result = RetrievalEngine(store).retrieve(RetrievalQuery(action_type="navigate"))

    assert result.matches[0].score == 1.0
