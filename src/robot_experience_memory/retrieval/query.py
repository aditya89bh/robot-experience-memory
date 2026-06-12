"""Retrieval query and result models."""

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store import ExperienceBundle


class RetrievalQuery(MemoryModel):
    """Criteria describing experiences to retrieve."""

    action_type: str | None = None
    robot_id: str | None = None
    environment: str | None = None
    operator: str | None = None
    success: bool | None = None
    error_code: str | None = None
    tags: tuple[str, ...] = Field(default_factory=tuple)
    top_k: int | None = Field(default=None, gt=0)


class RetrievalMatch(MemoryModel):
    """A matched experience and its deterministic similarity score."""

    experience: ExperienceBundle
    score: float = Field(ge=0.0, le=1.0)
    explanation: object | None = None


class RetrievalResult(MemoryModel):
    """Result set returned by retrieval."""

    query: RetrievalQuery
    matches: tuple[RetrievalMatch, ...] = Field(default_factory=tuple)
