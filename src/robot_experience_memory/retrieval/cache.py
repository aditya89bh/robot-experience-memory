"""Simple deterministic in-memory retrieval cache."""

from robot_experience_memory.retrieval.query import RetrievalQuery, RetrievalResult


class RetrievalCache:
    """Small in-memory cache keyed by normalized query JSON."""

    def __init__(self) -> None:
        self._entries: dict[str, RetrievalResult] = {}

    def key_for(self, query: RetrievalQuery) -> str:
        """Return a deterministic cache key for a query."""
        return query.model_dump_json(exclude_none=True, exclude_defaults=True)

    def get(self, query: RetrievalQuery) -> RetrievalResult | None:
        """Return a cached result, if present."""
        return self._entries.get(self.key_for(query))

    def set(self, query: RetrievalQuery, result: RetrievalResult) -> None:
        """Cache a query result."""
        self._entries[self.key_for(query)] = result

    def clear(self) -> None:
        """Clear all cached retrieval results."""
        self._entries.clear()
