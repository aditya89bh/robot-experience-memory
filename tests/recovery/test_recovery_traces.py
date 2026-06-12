from robot_experience_memory.recovery import RecoveryEngine, RecoveryTrace
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_recovery_trace_records_evidence_and_rules() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)

    suggestion = RecoveryEngine(store).suggest_recovery(failure)

    assert isinstance(suggestion.trace, RecoveryTrace)
    assert suggestion.trace.matched_experience_ids == ("exp-1",)
    assert suggestion.trace.rules_fired == ("retry_candidate",)
    assert suggestion.trace.final_rationale == suggestion.rationale
    assert suggestion.trace.evidence["similar_failures"] == 1
