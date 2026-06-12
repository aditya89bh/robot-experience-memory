"""Similar experience retrieval APIs."""

from robot_experience_memory.retrieval.cache import RetrievalCache
from robot_experience_memory.retrieval.engine import RetrievalEngine
from robot_experience_memory.retrieval.errors import RetrievalError
from robot_experience_memory.retrieval.explanations import (
    RetrievalExplanation,
    explain_match,
)
from robot_experience_memory.retrieval.interface import RetrievalInterface
from robot_experience_memory.retrieval.planner import (
    RetrievalQueryPlan,
    plan_retrieval_query,
)
from robot_experience_memory.retrieval.query import (
    RetrievalMatch,
    RetrievalQuery,
    RetrievalResult,
)
from robot_experience_memory.retrieval.ranking import (
    RetrievalWeights,
    rank_matches,
    score_bundles,
    weighted_similarity_score,
)
from robot_experience_memory.retrieval.scoring import (
    exact_match_score,
    metadata_similarity_score,
    tag_similarity_score,
    temporal_recency_scores,
)

__all__ = [
    "RetrievalCache",
    "RetrievalEngine",
    "RetrievalError",
    "RetrievalExplanation",
    "RetrievalInterface",
    "RetrievalQueryPlan",
    "plan_retrieval_query",
    "RetrievalMatch",
    "RetrievalQuery",
    "RetrievalResult",
    "RetrievalWeights",
    "rank_matches",
    "exact_match_score",
    "metadata_similarity_score",
    "tag_similarity_score",
    "temporal_recency_scores",
    "score_bundles",
    "weighted_similarity_score",
    "explain_match",
]
