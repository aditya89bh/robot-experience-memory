"""Recovery strategy support models and helpers."""

from collections import Counter
from collections.abc import Iterable

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store import ExperienceBundle


class FallbackAction(MemoryModel):
    """Alternate action that previously succeeded after similar failures."""

    action_type: str = Field(min_length=1)
    success_count: int = Field(ge=1)
    experience_ids: tuple[str, ...]
    causal_error_code: str | None = None


def find_fallback_action(
    failed_experience: ExperienceBundle,
    experiences: Iterable[ExperienceBundle],
) -> FallbackAction | None:
    """Find a deterministic alternate action that succeeded in similar context."""
    failed_error = failed_experience.outcome.error_code
    failed_ids = {
        bundle.experience.experience_id
        for bundle in experiences
        if not bundle.outcome.success
        and bundle.metadata.robot_id == failed_experience.metadata.robot_id
        and bundle.metadata.environment == failed_experience.metadata.environment
        and bundle.outcome.error_code == failed_error
    }
    if not failed_ids:
        return None
    candidates: dict[str, list[str]] = {}
    for bundle in experiences:
        same_cell = (
            bundle.metadata.robot_id == failed_experience.metadata.robot_id
            and bundle.metadata.environment == failed_experience.metadata.environment
        )
        after_failure = bundle.stored_at >= failed_experience.stored_at
        alternate_success = (
            bundle.outcome.success
            and bundle.action.action_type != failed_experience.action.action_type
        )
        if same_cell and after_failure and alternate_success:
            candidates.setdefault(bundle.action.action_type, []).append(
                bundle.experience.experience_id
            )
    if not candidates:
        return None
    counts = Counter({action: len(ids) for action, ids in candidates.items()})
    action_type = sorted(counts, key=lambda action: (-counts[action], action))[0]
    return FallbackAction(
        action_type=action_type,
        success_count=counts[action_type],
        experience_ids=tuple(candidates[action_type]),
        causal_error_code=failed_error,
    )


def score_confidence(
    *, sample_size: int, successes: int, failures: int, similarity: float = 1.0
) -> float:
    """Score deterministic suggestion confidence between 0.0 and 1.0."""
    bounded_similarity = max(0.0, min(1.0, similarity))
    sample_component = min(sample_size, 10) / 10
    total = successes + failures
    evidence_component = 0.25 if total == 0 else max(successes, failures) / total
    confidence = 0.2 + (0.4 * sample_component) + (0.3 * evidence_component)
    confidence += 0.1 * bounded_similarity
    return round(max(0.0, min(1.0, confidence)), 4)
