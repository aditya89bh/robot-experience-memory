"""Deterministic similar-experience retrieval engine."""

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
from robot_experience_memory.store import MemoryStore


class RetrievalEngine(RetrievalInterface):
    """Retrieve relevant past experiences from a memory store."""

    def __init__(
        self, store: MemoryStore, *, weights: RetrievalWeights | None = None
    ) -> None:
        self.store = store
        self.weights = weights or RetrievalWeights()

    def retrieve(self, query: RetrievalQuery) -> RetrievalResult:
        """Return stored experiences for a query."""
        matches = tuple(
            RetrievalMatch(
                experience=bundle,
                score=weighted_similarity_score(query, bundle, self.weights),
            )
            for bundle in self.store.list()
        )
        return RetrievalResult(query=query, matches=matches)
