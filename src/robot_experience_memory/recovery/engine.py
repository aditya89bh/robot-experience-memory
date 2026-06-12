"""Rule-based recovery intelligence engine."""

from robot_experience_memory.recovery.strategies import find_fallback_action
from robot_experience_memory.recovery.suggestions import (
    RecoverySuggestion,
    SuggestionType,
)
from robot_experience_memory.store import ExperienceBundle, MemoryStore

RecoveryResult = RecoverySuggestion


class RecoveryEngine:
    """Analyze stored experiences and suggest deterministic recovery actions."""

    def __init__(self, store: MemoryStore, *, max_retries: int = 1) -> None:
        self.store = store
        self.max_retries = max_retries

    def suggest_recovery(
        self, failed_experience: ExperienceBundle, *, retry_count: int = 0
    ) -> RecoveryResult:
        """Suggest a recovery action for a failed experience bundle."""
        experiences = self.store.list()
        similar_failures = [
            bundle
            for bundle in experiences
            if not bundle.outcome.success
            and bundle.action.action_type == failed_experience.action.action_type
            and bundle.metadata.robot_id == failed_experience.metadata.robot_id
        ]
        suggestion_type: SuggestionType
        related_successes = [
            bundle
            for bundle in experiences
            if bundle.outcome.success
            and bundle.action.action_type == failed_experience.action.action_type
            and bundle.metadata.robot_id == failed_experience.metadata.robot_id
        ]
        fallback = find_fallback_action(failed_experience, experiences)
        if retry_count >= self.max_retries:
            suggestion_type = "escalate"
            rationale = "retry budget is exhausted"
        elif fallback is not None and len(similar_failures) > self.max_retries:
            suggestion_type = "fallback"
            rationale = f"alternate action succeeded before: {fallback.action_type}"
        elif len(similar_failures) <= self.max_retries or related_successes:
            suggestion_type = "retry"
            rationale = "failure is rare or this action has succeeded before"
        else:
            suggestion_type = "escalate"
            rationale = "similar failures have repeated for this robot/action pair"
        return RecoverySuggestion(
            suggestion_type=suggestion_type,
            rationale=rationale,
            confidence=0.5,
            related_experience_ids=tuple(
                bundle.experience.experience_id for bundle in similar_failures
            )
            + (() if fallback is None else fallback.experience_ids),
        )

    analyze_failure = suggest_recovery
