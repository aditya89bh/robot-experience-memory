"""Rule-based recovery intelligence engine."""

from robot_experience_memory.recovery.policies import RecoveryPolicy
from robot_experience_memory.recovery.strategies import (
    find_fallback_action,
    score_confidence,
)
from robot_experience_memory.recovery.suggestions import (
    RecoverySuggestion,
    SuggestionType,
)
from robot_experience_memory.recovery.traces import RecoveryTrace
from robot_experience_memory.store import ExperienceBundle, MemoryStore

RecoveryResult = RecoverySuggestion


class RecoveryEngine:
    """Analyze stored experiences and suggest deterministic recovery actions."""

    def __init__(
        self,
        store: MemoryStore,
        *,
        policy: RecoveryPolicy | None = None,
        max_retries: int | None = None,
        escalation_threshold: int | None = None,
    ) -> None:
        self.store = store
        base_policy = policy or RecoveryPolicy()
        self.policy = base_policy.model_copy(
            update={
                key: value
                for key, value in {
                    "max_retries": max_retries,
                    "escalation_threshold": escalation_threshold,
                }.items()
                if value is not None
            }
        )
        self.max_retries = self.policy.max_retries
        self.escalation_threshold = self.policy.escalation_threshold

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
        rules_fired: list[str] = []
        if len(similar_failures) >= self.escalation_threshold:
            suggestion_type = "escalate"
            rationale = "repeated failures exceed escalation threshold"
            rules_fired.append("escalation_threshold")
        elif retry_count >= self.max_retries:
            suggestion_type = "escalate"
            rationale = "retry budget is exhausted"
            rules_fired.append("retry_budget_exhausted")
        elif fallback is not None and len(similar_failures) > self.max_retries:
            suggestion_type = "fallback"
            rationale = f"alternate action succeeded before: {fallback.action_type}"
            rules_fired.append("fallback_success")
        elif len(similar_failures) <= self.max_retries or related_successes:
            suggestion_type = "retry"
            rationale = "failure is rare or this action has succeeded before"
            rules_fired.append("retry_candidate")
        else:
            suggestion_type = "escalate"
            rationale = "similar failures have repeated for this robot/action pair"
            rules_fired.append("repeated_failure")
        confidence = score_confidence(
            sample_size=len(similar_failures) + len(related_successes),
            successes=len(related_successes)
            + (0 if fallback is None else fallback.success_count),
            failures=len(similar_failures),
            similarity=1.0,
        )
        if confidence < self.policy.minimum_confidence:
            suggestion_type = "escalate"
            rationale = "confidence is below recovery policy threshold"
            rules_fired.append("minimum_confidence")
        related_ids = tuple(
            bundle.experience.experience_id for bundle in similar_failures
        ) + (() if fallback is None else fallback.experience_ids)
        trace = RecoveryTrace(
            matched_experience_ids=related_ids,
            rules_fired=tuple(rules_fired),
            final_rationale=rationale,
            evidence={
                "similar_failures": len(similar_failures),
                "related_successes": len(related_successes),
                "retry_count": retry_count,
                "max_retries": self.max_retries,
                "escalation_threshold": self.escalation_threshold,
            },
        )
        return RecoverySuggestion(
            suggestion_type=suggestion_type,
            rationale=rationale,
            confidence=confidence,
            related_experience_ids=related_ids,
            trace=trace,
        )

    analyze_failure = suggest_recovery
