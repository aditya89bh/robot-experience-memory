"""Failure pattern detection for stored experiences."""

from collections import Counter
from collections.abc import Iterable

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store import ExperienceBundle


class FailurePattern(MemoryModel):
    """Repeated failure evidence for a specific field/value pair."""

    field: str
    value: str
    count: int
    experience_ids: tuple[str, ...]


def detect_failure_patterns(
    experiences: Iterable[ExperienceBundle], *, min_count: int = 2
) -> list[FailurePattern]:
    """Detect repeated failures by action, error, robot, environment, and tag."""
    buckets: dict[tuple[str, str], list[str]] = {}
    for bundle in experiences:
        if bundle.outcome.success:
            continue
        values = {
            "action_type": bundle.action.action_type,
            "robot_id": bundle.metadata.robot_id,
            "environment": bundle.metadata.environment,
        }
        if bundle.outcome.error_code is not None:
            values["error_code"] = bundle.outcome.error_code
        for field, value in values.items():
            buckets.setdefault((field, value), []).append(
                bundle.experience.experience_id
            )
        for tag in bundle.metadata.tags:
            buckets.setdefault(("tag", tag), []).append(bundle.experience.experience_id)

    patterns = [
        FailurePattern(
            field=field, value=value, count=len(ids), experience_ids=tuple(ids)
        )
        for (field, value), ids in buckets.items()
        if len(ids) >= min_count
    ]
    order = Counter(
        {(pattern.field, pattern.value): pattern.count for pattern in patterns}
    )
    return sorted(
        patterns,
        key=lambda pattern: (
            -order[(pattern.field, pattern.value)],
            pattern.field,
            pattern.value,
        ),
    )
