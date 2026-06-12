"""Temporal recovery-chain analysis."""

from __future__ import annotations

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store import ExperienceBundle


class RecoveryChainStep(MemoryModel):
    """One ordered experience in a recovery chain."""

    experience_id: str
    action_type: str
    success: bool
    summary: str | None = None


class RecoveryChain(MemoryModel):
    """Ordered sequence from an initial failure to later outcomes."""

    root_experience_id: str
    steps: tuple[RecoveryChainStep, ...] = Field(default_factory=tuple)

    @property
    def resolved(self) -> bool:
        """Return whether the chain eventually reaches a success."""
        return any(step.success for step in self.steps[1:])


def build_temporal_recovery_chain(
    failed_experience: ExperienceBundle,
    candidates: list[ExperienceBundle],
    *,
    max_steps: int = 5,
) -> RecoveryChain:
    """Build a same-robot/environment chain after a failure timestamp."""
    related = [
        bundle
        for bundle in candidates
        if bundle.metadata.robot_id == failed_experience.metadata.robot_id
        and bundle.metadata.environment == failed_experience.metadata.environment
        and bundle.stored_at >= failed_experience.stored_at
    ]
    related.sort(key=lambda bundle: bundle.stored_at)
    steps = tuple(
        RecoveryChainStep(
            experience_id=bundle.experience_id,
            action_type=bundle.action.action_type,
            success=bundle.outcome.success,
            summary=bundle.outcome.summary,
        )
        for bundle in related[:max_steps]
    )
    return RecoveryChain(
        root_experience_id=failed_experience.experience_id,
        steps=steps,
    )
