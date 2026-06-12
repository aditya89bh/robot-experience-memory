"""Retrieval engine interface."""

from abc import ABC, abstractmethod

from robot_experience_memory.retrieval.query import RetrievalQuery, RetrievalResult


class RetrievalInterface(ABC):
    """Abstract retrieval interface."""

    @abstractmethod
    def retrieve(self, query: RetrievalQuery) -> RetrievalResult:
        """Return experiences matching a retrieval query."""
