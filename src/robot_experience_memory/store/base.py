"""Abstract storage interface for robot experience memory."""

from abc import ABC, abstractmethod

from robot_experience_memory.store.bundle import ExperienceBundle
from robot_experience_memory.store.filters import ExperienceFilter, Pagination


class MemoryStore(ABC):
    """Abstract API for persisting complete robot experience bundles.

    Stores are append-oriented by default: inserting an existing experience ID
    should fail unless a backend explicitly receives an overwrite instruction in
    a later API extension.
    """

    @abstractmethod
    def put(self, bundle: ExperienceBundle) -> ExperienceBundle:
        """Persist one complete experience bundle and return the stored value."""

    @abstractmethod
    def get(self, experience_id: str) -> ExperienceBundle | None:
        """Return one complete experience bundle by ID, or ``None`` if missing."""

    @abstractmethod
    def list(
        self,
        filters: "ExperienceFilter | None" = None,
        pagination: "Pagination | None" = None,
    ) -> list[ExperienceBundle]:
        """Return stored experience bundles in stable backend order."""
