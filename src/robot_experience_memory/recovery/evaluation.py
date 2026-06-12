"""Deterministic recovery evaluation scenarios and metrics."""

from collections.abc import Iterable

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.recovery.engine import RecoveryEngine
from robot_experience_memory.recovery.suggestions import SuggestionType
from robot_experience_memory.store import ExperienceBundle, InMemoryStore


class RecoveryEvaluationCase(MemoryModel):
    """A deterministic recovery evaluation case."""

    name: str = Field(min_length=1)
    experiences: tuple[ExperienceBundle, ...]
    failed_experience_id: str = Field(min_length=1)
    expected_suggestion_type: SuggestionType


class RecoveryEvaluationMetrics(MemoryModel):
    """Aggregate deterministic recovery evaluation metrics."""

    total_cases: int = Field(ge=0)
    suggested_retry: int = Field(ge=0)
    suggested_fallback: int = Field(ge=0)
    suggested_escalation: int = Field(ge=0)
    average_confidence: float = Field(ge=0.0, le=1.0)
    correct_expected_suggestion_rate: float = Field(ge=0.0, le=1.0)


def evaluate_recovery_cases(
    cases: Iterable[RecoveryEvaluationCase],
) -> RecoveryEvaluationMetrics:
    """Evaluate recovery suggestions against expected deterministic outcomes."""
    case_list = list(cases)
    retry = 0
    fallback = 0
    escalation = 0
    confidence_total = 0.0
    correct = 0
    for case in case_list:
        store = InMemoryStore()
        failed: ExperienceBundle | None = None
        for bundle in case.experiences:
            store.put(bundle)
            if bundle.experience.experience_id == case.failed_experience_id:
                failed = bundle
        if failed is None:
            msg = f"failed experience not found: {case.failed_experience_id}"
            raise ValueError(msg)
        suggestion = RecoveryEngine(store).suggest_recovery(failed)
        if suggestion.suggestion_type == "retry":
            retry += 1
        elif suggestion.suggestion_type == "fallback":
            fallback += 1
        elif suggestion.suggestion_type == "escalate":
            escalation += 1
        confidence_total += suggestion.confidence
        if suggestion.suggestion_type == case.expected_suggestion_type:
            correct += 1
    total = len(case_list)
    return RecoveryEvaluationMetrics(
        total_cases=total,
        suggested_retry=retry,
        suggested_fallback=fallback,
        suggested_escalation=escalation,
        average_confidence=round(confidence_total / total, 4) if total else 0.0,
        correct_expected_suggestion_rate=round(correct / total, 4) if total else 0.0,
    )
