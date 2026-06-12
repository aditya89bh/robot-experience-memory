import pytest
from pydantic import ValidationError

from robot_experience_memory.recovery import RecoveryEngine, RecoveryPolicy
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_recovery_policy_validates_thresholds() -> None:
    with pytest.raises(ValidationError):
        RecoveryPolicy(max_retries=3, escalation_threshold=3)


def test_recovery_policy_controls_engine_thresholds() -> None:
    policy = RecoveryPolicy(max_retries=2, escalation_threshold=4)
    engine = RecoveryEngine(InMemoryStore(), policy=policy)

    assert engine.policy == policy
    assert engine.max_retries == 2


def test_minimum_confidence_can_force_escalation() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)

    suggestion = RecoveryEngine(
        store, policy=RecoveryPolicy(minimum_confidence=0.99)
    ).suggest_recovery(failure)

    assert suggestion.suggestion_type == "escalate"
    assert suggestion.rationale == "confidence is below recovery policy threshold"
