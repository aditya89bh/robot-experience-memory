from robot_experience_memory.recovery import RecoveryEngine
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_repeated_failures_exceeding_threshold_escalate() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)
    store.put(make_bundle("exp-2", success=False))
    store.put(make_bundle("exp-3", success=False))

    suggestion = RecoveryEngine(store, escalation_threshold=3).suggest_recovery(failure)

    assert suggestion.suggestion_type == "escalate"
    assert suggestion.rationale == "repeated failures exceed escalation threshold"


def test_threshold_can_be_tuned_to_allow_retry() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)
    store.put(make_bundle("exp-2", success=False))

    suggestion = RecoveryEngine(
        store, max_retries=2, escalation_threshold=3
    ).suggest_recovery(failure)

    assert suggestion.suggestion_type == "retry"
