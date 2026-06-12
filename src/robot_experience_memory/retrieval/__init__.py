"""Similar experience retrieval APIs."""

from robot_experience_memory.retrieval.engine import RetrievalEngine
from robot_experience_memory.retrieval.errors import RetrievalError
from robot_experience_memory.retrieval.interface import RetrievalInterface
from robot_experience_memory.retrieval.query import (
    RetrievalMatch,
    RetrievalQuery,
    RetrievalResult,
)
from robot_experience_memory.retrieval.ranking import (
    RetrievalWeights,
    weighted_similarity_score,
)
from robot_experience_memory.retrieval.scoring import (
    exact_match_score,
    metadata_similarity_score,
    tag_similarity_score,
)

__all__ = [
    "RetrievalEngine",
    "RetrievalError",
    "RetrievalInterface",
    "RetrievalMatch",
    "RetrievalQuery",
    "RetrievalResult",
    "RetrievalWeights",
    "exact_match_score",
    "metadata_similarity_score",
    "tag_similarity_score",
    "weighted_similarity_score",
]
