from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.recovery import (
    FallbackAction,
    RecoveryEngine,
    find_fallback_action,
)
from robot_experience_memory.store import ExperienceBundle, InMemoryStore
from tests.store.factories import make_bundle


def failed_blocked(experience_id: str) -> ExperienceBundle:
    bundle = make_bundle(experience_id, success=False, action_type="navigate")
    return bundle.model_copy(
        update={
            "outcome": OutcomeRecord(
                outcome_id=bundle.outcome.outcome_id,
                success=False,
                summary="blocked",
                error_code="blocked",
            )
        }
    )


def test_find_fallback_action_from_successful_alternate_action() -> None:
    failure = failed_blocked("exp-1")
    fallback_success = make_bundle("exp-2", success=True, action_type="reroute")

    fallback = find_fallback_action(failure, [failure, fallback_success])

    assert fallback == FallbackAction(
        action_type="reroute",
        success_count=1,
        experience_ids=("exp-2",),
        causal_error_code="blocked",
    )


def test_recovery_engine_suggests_fallback_when_alternate_action_worked() -> None:
    store = InMemoryStore()
    failure = failed_blocked("exp-1")
    store.put(failure)
    store.put(failed_blocked("exp-2"))
    store.put(make_bundle("exp-3", success=True, action_type="reroute"))

    suggestion = RecoveryEngine(store, max_retries=1).suggest_recovery(failure)

    assert suggestion.suggestion_type == "fallback"
    assert "reroute" in suggestion.rationale
    assert "exp-3" in suggestion.related_experience_ids
