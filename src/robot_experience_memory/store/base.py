"""Abstract storage interface for robot experience memory."""

from abc import ABC, abstractmethod

from robot_experience_memory.store.bundle import ExperienceBundle
from robot_experience_memory.store.filters import ExperienceFilter, Pagination


class MemoryStore(ABC):
    """Abstract API for persisting complete robot experience bundles.

    Stores are append-only: inserting an existing experience ID must raise
    ``DuplicateExperienceError``. The ``allow_overwrite`` parameter is kept for
    backwards-compatible callers but backends should not overwrite records.
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
        """Persist multiple complete experience bundles in input order.

        ``allow_overwrite`` is accepted for compatibility and does not permit
        duplicate IDs in append-only stores.
        """
        return [self.put(bundle, allow_overwrite=allow_overwrite) for bundle in bundles]

    def get_many(self, experience_ids: list[str]) -> list[ExperienceBundle | None]:
        """Retrieve multiple experience bundles in input ID order."""
        return [self.get(experience_id) for experience_id in experience_ids]


    def query_by_robot_id(self, robot_id: str) -> list[ExperienceBundle]:
        """Return experiences recorded for a robot."""
        return self.list(filters=ExperienceFilter(robot_id=robot_id))

    def query_by_environment(self, environment: str) -> list[ExperienceBundle]:
        """Return experiences recorded in an environment."""
        return self.list(filters=ExperienceFilter(environment=environment))

    def query_by_tag(self, tag: str) -> list[ExperienceBundle]:
        """Return experiences carrying a metadata tag."""
        return self.list(filters=ExperienceFilter(tag=tag))

    def query_by_operator(self, operator: str) -> list[ExperienceBundle]:
        """Return experiences associated with an operator."""
        return self.list(filters=ExperienceFilter(operator=operator))

    @abstractmethod
    def list(
        self,
        filters: "ExperienceFilter | None" = None,
        pagination: "Pagination | None" = None,
    ) -> list[ExperienceBundle]:
        """Return stored experience bundles in stable backend order."""
