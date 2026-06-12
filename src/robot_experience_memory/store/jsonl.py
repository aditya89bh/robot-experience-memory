"""JSON Lines backend for robot experience memory."""

from __future__ import annotations

from builtins import list as builtin_list
from pathlib import Path

from robot_experience_memory.store.base import MemoryStore
from robot_experience_memory.store.bundle import ExperienceBundle
from robot_experience_memory.store.errors import DuplicateExperienceError
from robot_experience_memory.store.filters import ExperienceFilter, Pagination


class JSONLMemoryStore(MemoryStore):
    """Append-oriented JSONL store for portable local persistence."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        self._bundles: dict[str, ExperienceBundle] = {}
        self._order: builtin_list[str] = []
        self._load_index()

    def put(
        self,
        bundle: ExperienceBundle,
        *,
        allow_overwrite: bool = False,
    ) -> ExperienceBundle:
        """Append one bundle to the JSONL file."""
        _ = allow_overwrite
        if self.get(bundle.experience_id) is not None:
            raise DuplicateExperienceError(bundle.experience_id)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(bundle.to_json().replace("\n", "") + "\n")
        self._index_bundle(bundle)
        return bundle

    def get(self, experience_id: str) -> ExperienceBundle | None:
        """Return the latest bundle for an experience ID."""
        return self._bundles.get(experience_id)

    def list(
        self,
        filters: ExperienceFilter | None = None,
        pagination: Pagination | None = None,
    ) -> builtin_list[ExperienceBundle]:
        """Return latest bundles in first-inserted stable order."""
        selected = [self._bundles[experience_id] for experience_id in self._order]
        if filters is not None:
            selected = [bundle for bundle in selected if filters.matches(bundle)]
        if pagination is not None:
            selected = pagination.apply(selected)
        return selected

    def _read_all_raw(self) -> builtin_list[ExperienceBundle]:
        bundles: builtin_list[ExperienceBundle] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                bundles.append(ExperienceBundle.from_json(line))
        return bundles

    def indexed_fields(self) -> tuple[str, ...]:
        """Return fields indexed from the JSONL file on load."""
        return (
            "experience_id",
            "robot_id",
            "environment",
            "operator",
            "success",
            "action_type",
            "tag",
        )

    def _load_index(self) -> None:
        for bundle in self._read_all_raw():
            self._index_bundle(bundle)

    def _index_bundle(self, bundle: ExperienceBundle) -> None:
        if bundle.experience_id not in self._bundles:
            self._order.append(bundle.experience_id)
        self._bundles[bundle.experience_id] = bundle
