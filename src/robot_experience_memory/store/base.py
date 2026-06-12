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
    def put(
        self,
        bundle: ExperienceBundle,
        *,
        allow_overwrite: bool = False,
    ) -> ExperienceBundle:
        """Persist one complete experience bundle and return the stored value."""

    @abstractmethod
    def get(self, experience_id: str) -> ExperienceBundle | None:
        """Return one complete experience bundle by ID, or ``None`` if missing."""

    def put_many(
        self,
        bundles: list[ExperienceBundle],
        *,
        allow_overwrite: bool = False,
    ) -> list[ExperienceBundle]:
        """Persist multiple complete experience bundles in input order."""
        return [self.put(bundle, allow_overwrite=allow_overwrite) for bundle in bundles]

    def get_many(self, experience_ids: list[str]) -> list[ExperienceBundle | None]:
        """Retrieve multiple experience bundles in input ID order."""
        return [self.get(experience_id) for experience_id in experience_ids]

    @abstractmethod
    def list(
        self,
        filters: "ExperienceFilter | None" = None,
        pagination: "Pagination | None" = None,
    ) -> list[ExperienceBundle]:
        """Return stored experience bundles in stable backend order."""
