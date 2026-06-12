from robot_experience_memory.recovery import RecoveryEngine, score_confidence
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_confidence_score_is_bounded() -> None:
    assert score_confidence(sample_size=0, successes=0, failures=0) >= 0.0
    assert score_confidence(sample_size=100, successes=100, failures=0) <= 1.0


def test_confidence_increases_with_sample_size_and_consistency() -> None:
    weak = score_confidence(sample_size=1, successes=1, failures=1, similarity=0.5)
    strong = score_confidence(sample_size=8, successes=8, failures=0, similarity=1.0)

    assert strong > weak


def test_engine_uses_deterministic_confidence() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)

    suggestion = RecoveryEngine(store).suggest_recovery(failure)

    assert 0.0 <= suggestion.confidence <= 1.0
    repeated = RecoveryEngine(store).suggest_recovery(failure)
    assert suggestion.confidence == repeated.confidence
