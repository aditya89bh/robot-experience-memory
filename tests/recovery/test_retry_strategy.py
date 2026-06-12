from robot_experience_memory.recovery import RecoveryEngine
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_retry_suggested_when_failure_is_within_retry_policy() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)

    suggestion = RecoveryEngine(store, max_retries=2).suggest_recovery(failure)

    assert suggestion.suggestion_type == "retry"
    assert "rare" in suggestion.rationale


def test_retry_suggested_when_same_action_succeeded_before() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(make_bundle("exp-0", success=True))
    store.put(failure)
    store.put(make_bundle("exp-2", success=False))

    suggestion = RecoveryEngine(store, max_retries=1).suggest_recovery(failure)

    assert suggestion.suggestion_type == "retry"
    assert suggestion.related_experience_ids == ("exp-1", "exp-2")


def test_retry_budget_exhaustion_escalates() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)

    suggestion = RecoveryEngine(store, max_retries=1).suggest_recovery(
        failure, retry_count=1
    )

    assert suggestion.suggestion_type == "escalate"
    assert suggestion.rationale == "retry budget is exhausted"
