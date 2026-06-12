"""Deterministic outcome clustering utilities."""

from collections.abc import Iterable

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store import ExperienceBundle


class OutcomeCluster(MemoryModel):
    """Group of outcomes sharing deterministic recovery-relevant attributes."""

    success: bool
    error_code: str | None
    action_type: str
    environment: str
    count: int
    experience_ids: tuple[str, ...]


def cluster_outcomes(experiences: Iterable[ExperienceBundle]) -> list[OutcomeCluster]:
    """Group outcomes by success, error code, action type, and environment."""
    buckets: dict[tuple[bool, str | None, str, str], list[str]] = {}
    for bundle in experiences:
        key = (
            bundle.outcome.success,
            bundle.outcome.error_code,
            bundle.action.action_type,
            bundle.metadata.environment,
        )
        buckets.setdefault(key, []).append(bundle.experience.experience_id)
    clusters = [
        OutcomeCluster(
            success=success,
            error_code=error_code,
            action_type=action_type,
            environment=environment,
            count=len(ids),
            experience_ids=tuple(ids),
        )
        for (success, error_code, action_type, environment), ids in buckets.items()
    ]
    return sorted(
        clusters,
        key=lambda cluster: (
            cluster.success,
            cluster.error_code or "",
            cluster.action_type,
            cluster.environment,
        ),
    )
