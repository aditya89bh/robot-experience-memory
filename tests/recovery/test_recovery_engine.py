from robot_experience_memory.recovery import RecoveryEngine, RecoverySuggestion
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_recovery_engine_suggests_retry_for_rare_failure() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)

    result = RecoveryEngine(store).suggest_recovery(failure)

    assert isinstance(result, RecoverySuggestion)
    assert result.suggestion_type == "retry"
    assert result.related_experience_ids == ("exp-1",)


def test_recovery_engine_escalates_repeated_failure() -> None:
    store = InMemoryStore()
    first = make_bundle("exp-1", success=False)
    second = make_bundle("exp-2", success=False)
    store.put(first)
    store.put(second)

    result = RecoveryEngine(store).analyze_failure(second)

    assert result.suggestion_type == "escalate"
    assert result.related_experience_ids == ("exp-1", "exp-2")
