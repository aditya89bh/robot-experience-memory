"""Deterministic similar-experience retrieval engine."""

from robot_experience_memory.retrieval.cache import RetrievalCache
from robot_experience_memory.retrieval.explanations import explain_match
from robot_experience_memory.retrieval.interface import RetrievalInterface
from robot_experience_memory.retrieval.planner import plan_retrieval_query
from robot_experience_memory.retrieval.query import (
    RetrievalMatch,
    RetrievalQuery,
    RetrievalResult,
)
from robot_experience_memory.retrieval.ranking import (
    RetrievalWeights,
    rank_matches,
    score_bundles,
)
from robot_experience_memory.retrieval.scoring import temporal_recency_scores
from robot_experience_memory.store import MemoryStore


class RetrievalEngine(RetrievalInterface):
    """Retrieve relevant past experiences from a memory store."""

    def __init__(
        self,
        store: MemoryStore,
        *,
        weights: RetrievalWeights | None = None,
        cache_enabled: bool = True,
    ) -> None:
        self.store = store
        self.weights = weights or RetrievalWeights()
        self.cache_enabled = cache_enabled
        self.cache = RetrievalCache()

    def retrieve(self, query: RetrievalQuery) -> RetrievalResult:
        """Return stored experiences for a query."""
        if self.cache_enabled:
            cached = self.cache.get(query)
            if cached is not None:
                return cached
        plan = plan_retrieval_query(query)
        bundles = (
            self.store.list(filters=plan.filters)
            if plan.has_pushdown
            else self.store.list()
        )
        scores = score_bundles(query, bundles, self.weights)
        temporal_scores = temporal_recency_scores(bundles)
        matches = tuple(
            RetrievalMatch(
                experience=bundle,
                score=scores[bundle.experience.experience_id],
                explanation=explain_match(
                    query,
                    bundle,
                    temporal_score=temporal_scores.get(
                        bundle.experience.experience_id, 0.0
                    ),
                ),
            )
            for bundle in bundles
        )
        matches = rank_matches(matches)
        if query.top_k is not None:
            matches = matches[: query.top_k]
        result = RetrievalResult(query=query, matches=matches)
        if self.cache_enabled:
            self.cache.set(query, result)
        return result
