"""Deterministic similar-experience retrieval engine."""

from robot_experience_memory.retrieval.interface import RetrievalInterface
from robot_experience_memory.retrieval.query import (
    RetrievalMatch,
    RetrievalQuery,
    RetrievalResult,
)
from robot_experience_memory.retrieval.ranking import (
    RetrievalWeights,
    score_bundles,
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
        bundles = self.store.list()
        scores = score_bundles(query, bundles, self.weights)
        matches = tuple(
            RetrievalMatch(
                experience=bundle,
                score=scores[bundle.experience.experience_id],
            )
            for bundle in bundles
        )
        return RetrievalResult(query=query, matches=matches)
