"""Human-readable retrieval explanations."""

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.retrieval.query import RetrievalQuery
from robot_experience_memory.retrieval.scoring import (
    exact_match_score,
    metadata_similarity_score,
    tag_similarity_score,
)
from robot_experience_memory.store import ExperienceBundle


class RetrievalExplanation(MemoryModel):
    """Score component details for a retrieval match."""

    components: dict[str, float] = Field(default_factory=dict)
    reasons: tuple[str, ...] = Field(default_factory=tuple)


def explain_match(
    query: RetrievalQuery,
    bundle: ExperienceBundle,
    *,
    temporal_score: float = 0.0,
) -> RetrievalExplanation:
    """Explain why a bundle was returned for a query."""
    components = {
        "exact": exact_match_score(query, bundle),
        "metadata": metadata_similarity_score(query, bundle),
        "tags": tag_similarity_score(query, bundle),
        "temporal": temporal_score,
    }
    reasons: list[str] = []
    if query.action_type is not None and bundle.action.action_type == query.action_type:
        reasons.append(f"action_type matched: {query.action_type}")
    if query.robot_id is not None and bundle.metadata.robot_id == query.robot_id:
        reasons.append(f"robot_id matched: {query.robot_id}")
    if (
        query.environment is not None
        and bundle.metadata.environment == query.environment
    ):
        reasons.append(f"environment matched: {query.environment}")
    if query.tags and set(query.tags) & set(bundle.metadata.tags):
        reasons.append("tags overlapped")
    if temporal_score > 0:
        reasons.append("temporal recency contributed")
    if not reasons:
        reasons.append("returned by deterministic ranking")
    return RetrievalExplanation(components=components, reasons=tuple(reasons))
