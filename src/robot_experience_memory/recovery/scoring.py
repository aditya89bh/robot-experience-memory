"""Deterministic recovery-sequence scoring."""

from __future__ import annotations

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.recovery.chains import RecoveryChain


class RecoverySequenceScore(MemoryModel):
    """Explainable score for an ordered recovery sequence."""

    score: float = Field(ge=0.0, le=1.0)
    resolved: bool
    steps: int = Field(ge=0)
    successful_step_index: int | None = None
    rationale: str


def score_recovery_sequence(chain: RecoveryChain) -> RecoverySequenceScore:
    """Score chains higher when they resolve quickly after the initial failure."""
    if not chain.steps:
        return RecoverySequenceScore(
            score=0.0,
            resolved=False,
            steps=0,
            rationale="empty chain has no recovery evidence",
        )
    for index, step in enumerate(chain.steps[1:], start=1):
        if step.success:
            penalty = min(index - 1, 4) * 0.15
            score = round(max(0.2, 1.0 - penalty), 4)
            return RecoverySequenceScore(
                score=score,
                resolved=True,
                steps=len(chain.steps),
                successful_step_index=index,
                rationale=f"resolved after {index} recovery step(s)",
            )
    return RecoverySequenceScore(
        score=0.1,
        resolved=False,
        steps=len(chain.steps),
        rationale="chain did not reach a successful outcome",
    )
