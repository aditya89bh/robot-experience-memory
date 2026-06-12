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
        self._by_robot_id: dict[str, set[str]] = {}
        self._by_environment: dict[str, set[str]] = {}
        self._by_operator: dict[str, set[str]] = {}
        self._by_success: dict[bool, set[str]] = {}
        self._by_action_type: dict[str, set[str]] = {}
        self._by_tag: dict[str, set[str]] = {}

    def put(
        self,
        bundle: ExperienceBundle,
        *,
        allow_overwrite: bool = False,
    ) -> ExperienceBundle:
        """Persist one bundle, rejecting duplicate experience IDs."""
        experience_id = bundle.experience_id
        _ = allow_overwrite
        if experience_id in self._bundles:
            raise DuplicateExperienceError(experience_id)
        self._order.append(experience_id)
        self._bundles[experience_id] = bundle
        self._index_bundle(bundle)
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

    def indexed_fields(self) -> tuple[str, ...]:
        """Return fields maintained as in-memory indexes."""
        return (
            "experience_id",
            "robot_id",
            "environment",
            "operator",
            "success",
            "action_type",
            "tag",
        )

    def _index_bundle(self, bundle: ExperienceBundle) -> None:
        experience_id = bundle.experience_id
        self._by_robot_id.setdefault(bundle.metadata.robot_id, set()).add(experience_id)
        self._by_environment.setdefault(bundle.metadata.environment, set()).add(
            experience_id
        )
        if bundle.metadata.operator is not None:
            self._by_operator.setdefault(bundle.metadata.operator, set()).add(
                experience_id
            )
        self._by_success.setdefault(bundle.outcome.success, set()).add(experience_id)
        self._by_action_type.setdefault(bundle.action.action_type, set()).add(
            experience_id
        )
        for tag in bundle.metadata.tags:
            self._by_tag.setdefault(tag, set()).add(experience_id)
