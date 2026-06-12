"""Rule-based recovery intelligence engine."""

from robot_experience_memory.recovery.suggestions import (
    RecoverySuggestion,
    SuggestionType,
)
from robot_experience_memory.store import ExperienceBundle, MemoryStore

RecoveryResult = RecoverySuggestion


class RecoveryEngine:
    """Analyze stored experiences and suggest deterministic recovery actions."""

    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def suggest_recovery(self, failed_experience: ExperienceBundle) -> RecoveryResult:
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
        if len(similar_failures) <= 1:
            suggestion_type = "retry"
            rationale = "failure is rare for this robot/action pair"
        else:
            suggestion_type = "escalate"
            rationale = "similar failures have repeated for this robot/action pair"
        return RecoverySuggestion(
            suggestion_type=suggestion_type,
            rationale=rationale,
            confidence=0.5,
            related_experience_ids=tuple(
                bundle.experience.experience_id for bundle in similar_failures
            ),
        )

    analyze_failure = suggest_recovery
