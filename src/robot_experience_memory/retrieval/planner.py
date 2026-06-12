"""Deterministic query planning for symbolic retrieval."""

from __future__ import annotations

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.retrieval.query import RetrievalQuery
from robot_experience_memory.store import ExperienceFilter


class RetrievalQueryPlan(MemoryModel):
    """Executable plan for narrowing a retrieval query before scoring."""

    query: RetrievalQuery
    filters: ExperienceFilter | None = None
    pushdown_fields: tuple[str, ...] = Field(default_factory=tuple)
    residual_fields: tuple[str, ...] = Field(default_factory=tuple)

    @property
    def has_pushdown(self) -> bool:
        """Return whether the plan can narrow candidates in the store."""
        return self.filters is not None and bool(self.pushdown_fields)


def plan_retrieval_query(query: RetrievalQuery) -> RetrievalQueryPlan:
    """Build a practical retrieval plan from exact-match query fields."""
    pushdown_fields: list[str] = []
    residual_fields: list[str] = []
    filter_kwargs: dict[str, object] = {}

    for field_name in ("action_type", "robot_id", "environment", "operator", "success"):
        value = getattr(query, field_name)
        if value is not None:
            pushdown_fields.append(field_name)
            filter_kwargs[field_name] = value

    if query.tags:
        pushdown_fields.append("tag")
        filter_kwargs["tag"] = query.tags[0]
        if len(query.tags) > 1:
            residual_fields.append("tags")

    if query.error_code is not None:
        residual_fields.append("error_code")

    filters = (
        ExperienceFilter(
            action_type=query.action_type,
            robot_id=query.robot_id,
            environment=query.environment,
            operator=query.operator,
            success=query.success,
            tag=query.tags[0] if query.tags else None,
        )
        if filter_kwargs
        else None
    )
    return RetrievalQueryPlan(
        query=query,
        filters=filters,
        pushdown_fields=tuple(pushdown_fields),
        residual_fields=tuple(residual_fields),
    )
