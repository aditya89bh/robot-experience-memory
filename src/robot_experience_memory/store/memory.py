"""In-memory backend for robot experience memory."""

from robot_experience_memory.store.base import MemoryStore
from robot_experience_memory.store.bundle import ExperienceBundle
from robot_experience_memory.store.errors import DuplicateExperienceError
from robot_experience_memory.store.filters import ExperienceFilter, Pagination


class InMemoryStore(MemoryStore):
    """Process-local store useful for tests, prototypes, and short-lived agents."""

    def __init__(self) -> None:
        self._bundles: dict[str, ExperienceBundle] = {}
        self._order: list[str] = []

    def put(self, bundle: ExperienceBundle) -> ExperienceBundle:
        """Persist one bundle, rejecting duplicate experience IDs."""
        experience_id = bundle.experience_id
        if experience_id in self._bundles:
            raise DuplicateExperienceError(experience_id)
        self._bundles[experience_id] = bundle
        self._order.append(experience_id)
        return bundle

    def get(self, experience_id: str) -> ExperienceBundle | None:
        """Return a bundle by experience ID, if present."""
        return self._bundles.get(experience_id)

    def list(
        self,
        filters: ExperienceFilter | None = None,
        pagination: Pagination | None = None,
    ) -> list[ExperienceBundle]:
        """Return bundles in stable insertion order."""
        selected = [self._bundles[experience_id] for experience_id in self._order]
        if filters is not None:
            selected = [bundle for bundle in selected if filters.matches(bundle)]
        if pagination is not None:
            selected = pagination.apply(selected)
        return selected
