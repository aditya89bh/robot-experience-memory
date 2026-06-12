"""Replay statistics helpers."""

from collections import Counter
from dataclasses import dataclass, field

from robot_experience_memory.store import ExperienceBundle


@dataclass(frozen=True)
class ReplayStatistics:
    """Aggregate statistics for one replay run."""

    total_experiences: int = 0
    success_count: int = 0
    failure_count: int = 0
    action_type_counts: dict[str, int] = field(default_factory=dict)
    robot_id_counts: dict[str, int] = field(default_factory=dict)
    replay_duration_seconds: float = 0.0


def build_statistics(
    bundles: list[ExperienceBundle], *, replay_duration_seconds: float
) -> ReplayStatistics:
    """Build aggregate replay statistics from replayed bundles."""
    action_counts: Counter[str] = Counter()
    robot_counts: Counter[str] = Counter()
    success_count = 0
    for bundle in bundles:
        action_counts[bundle.action.action_type] += 1
        robot_counts[bundle.metadata.robot_id] += 1
        if bundle.outcome.success:
            success_count += 1
    total = len(bundles)
    return ReplayStatistics(
        total_experiences=total,
        success_count=success_count,
        failure_count=total - success_count,
        action_type_counts=dict(action_counts),
        robot_id_counts=dict(robot_counts),
        replay_duration_seconds=replay_duration_seconds,
    )
