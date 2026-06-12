import pytest
from pydantic import ValidationError

from robot_experience_memory.recovery import RecoveryEngine, RecoverySuggestion
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_recovery_suggestion_model_serializes() -> None:
    suggestion = RecoverySuggestion(
        suggestion_type="retry",
        rationale="rare failure",
        confidence=0.75,
        related_experience_ids=("exp-1",),
    )

    assert suggestion.to_dict()["suggestion_type"] == "retry"
    assert suggestion.related_experience_ids == ("exp-1",)


def test_recovery_suggestion_validates_confidence() -> None:
    with pytest.raises(ValidationError):
        RecoverySuggestion(
            suggestion_type="retry",
            rationale="bad confidence",
            confidence=1.1,
        )


def test_recovery_engine_returns_recovery_suggestion() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)

    suggestion = RecoveryEngine(store).suggest_recovery(failure)

    assert isinstance(suggestion, RecoverySuggestion)
    assert suggestion.suggestion_type == "retry"
    assert suggestion.related_experience_ids == ("exp-1",)
