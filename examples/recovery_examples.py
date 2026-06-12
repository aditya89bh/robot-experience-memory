"""Runnable recovery intelligence examples.

Run with:
    python examples/recovery_examples.py
"""

from __future__ import annotations

from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.recovery import RecoveryEngine, RecoveryPolicy
from robot_experience_memory.store import ExperienceBundle, InMemoryStore


def make_bundle(
    experience_id: str,
    *,
    success: bool,
    action_type: str = "navigate",
    error_code: str | None = None,
) -> ExperienceBundle:
    """Build a small example bundle without test fixtures."""
    from robot_experience_memory.models import (  # noqa: PLC0415
        ActionRecord,
        ExperienceRecord,
        Metadata,
        StateSnapshot,
    )
    from robot_experience_memory.timestamps import utc_now  # noqa: PLC0415

    suffix = experience_id.removeprefix("exp-")
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id=experience_id,
            state_id=f"state-{suffix}",
            action_id=f"action-{suffix}",
            outcome_id=f"outcome-{suffix}",
            metadata_id=f"metadata-{suffix}",
        ),
        state=StateSnapshot(state_id=f"state-{suffix}"),
        action=ActionRecord(
            action_id=f"action-{suffix}",
            action_type=action_type,
            command=action_type,
        ),
        outcome=OutcomeRecord(
            outcome_id=f"outcome-{suffix}",
            success=success,
            summary="ok" if success else "failed",
            error_code=error_code,
        ),
        metadata=Metadata(
            metadata_id=f"metadata-{suffix}",
            robot_id="robot-a",
            environment="lab",
            tags=("nav",),
        ),
        stored_at=utc_now(),
    )


def print_suggestion(label: str, suggestion: object) -> None:
    """Print a compact example result."""
    print(f"\n{label}")
    print(suggestion)


def main() -> None:
    """Run retry, fallback, escalation, confidence, and trace examples."""
    retry_store = InMemoryStore()
    retry_failure = make_bundle("exp-1", success=False, error_code="blocked")
    retry_store.put(retry_failure)
    retry_suggestion = RecoveryEngine(retry_store).suggest_recovery(retry_failure)
    print_suggestion("retry suggestion", retry_suggestion)

    fallback_store = InMemoryStore()
    fallback_failure = make_bundle("exp-2", success=False, error_code="blocked")
    fallback_store.put(fallback_failure)
    fallback_store.put(make_bundle("exp-3", success=False, error_code="blocked"))
    fallback_store.put(make_bundle("exp-4", success=True, action_type="reroute"))
    fallback_suggestion = RecoveryEngine(fallback_store).suggest_recovery(
        fallback_failure
    )
    print_suggestion("fallback suggestion", fallback_suggestion)

    escalation_store = InMemoryStore()
    escalation_failure = make_bundle("exp-5", success=False, error_code="blocked")
    escalation_store.put(escalation_failure)
    escalation_store.put(make_bundle("exp-6", success=False, error_code="blocked"))
    escalation_store.put(make_bundle("exp-7", success=False, error_code="blocked"))
    escalation_suggestion = RecoveryEngine(escalation_store).suggest_recovery(
        escalation_failure
    )
    print_suggestion("escalation suggestion", escalation_suggestion)

    strict_policy = RecoveryPolicy(minimum_confidence=0.8)
    confidence_suggestion = RecoveryEngine(
        retry_store, policy=strict_policy
    ).suggest_recovery(retry_failure)
    print_suggestion("confidence threshold suggestion", confidence_suggestion)

    print_suggestion("trace output", retry_suggestion.trace)


if __name__ == "__main__":
    main()
