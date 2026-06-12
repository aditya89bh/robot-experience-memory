"""Rule-based recovery intelligence engine."""

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store import ExperienceBundle, MemoryStore


class RecoveryResult(MemoryModel):
    """Typed result returned by the initial recovery engine."""

    failed_experience_id: str
    failure_summary: str
    similar_failure_count: int
    suggestion_type: str
    rationale: str


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
        suggestion_type = "retry" if len(similar_failures) <= 1 else "escalate"
        rationale = (
            "failure is rare for this robot/action pair"
            if suggestion_type == "retry"
            else "similar failures have repeated for this robot/action pair"
        )
        return RecoveryResult(
            failed_experience_id=failed_experience.experience.experience_id,
            failure_summary=failed_experience.outcome.summary,
            similar_failure_count=len(similar_failures),
            suggestion_type=suggestion_type,
            rationale=rationale,
        )

    analyze_failure = suggest_recovery
