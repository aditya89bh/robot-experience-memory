"""Weighted retrieval scoring and ranking helpers."""

from pydantic import Field, model_validator

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.retrieval.query import RetrievalQuery
from robot_experience_memory.retrieval.scoring import (
    exact_match_score,
    metadata_similarity_score,
    tag_similarity_score,
)
from robot_experience_memory.store import ExperienceBundle


class RetrievalWeights(MemoryModel):
    """Configurable non-negative weights for retrieval scoring."""

    action: float = Field(default=1.0, ge=0.0)
    metadata: float = Field(default=1.0, ge=0.0)
    tags: float = Field(default=1.0, ge=0.0)
    outcome: float = Field(default=1.0, ge=0.0)
    temporal: float = Field(default=0.0, ge=0.0)

    @model_validator(mode="after")
    def require_positive_total(self) -> "RetrievalWeights":
        if self.total == 0.0:
            msg = "at least one retrieval weight must be positive"
            raise ValueError(msg)
        return self

    @property
    def total(self) -> float:
        """Return the total configured weight."""
        return self.action + self.metadata + self.tags + self.outcome + self.temporal


def _active_weight_total(query: RetrievalQuery, weights: RetrievalWeights) -> float:
    total = 0.0
    if query.action_type is not None:
        total += weights.action
    metadata_values = (query.robot_id, query.environment, query.operator)
    if any(value is not None for value in metadata_values):
        total += weights.metadata
    if query.tags:
        total += weights.tags
    if query.success is not None or query.error_code is not None:
        total += weights.outcome
    total += weights.temporal
    return total


def weighted_similarity_score(
    query: RetrievalQuery,
    bundle: ExperienceBundle,
    weights: RetrievalWeights,
) -> float:
    """Compute a deterministic weighted similarity score."""
    action_score = (
        1.0
        if (
            query.action_type is not None
            and bundle.action.action_type == query.action_type
        )
        else 0.0
    )
    outcome_score = exact_match_score(
        RetrievalQuery(success=query.success, error_code=query.error_code), bundle
    )
    active_total = _active_weight_total(query, weights)
    if active_total == 0.0:
        return 0.0
    score = (
        (weights.action * action_score)
        + (weights.metadata * metadata_similarity_score(query, bundle))
        + (weights.tags * tag_similarity_score(query, bundle))
        + (weights.outcome * outcome_score)
    ) / active_total
    return round(max(0.0, min(1.0, score)), 6)
