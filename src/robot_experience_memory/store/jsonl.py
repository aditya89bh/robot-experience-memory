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

    def put(
        self,
        bundle: ExperienceBundle,
        *,
        allow_overwrite: bool = False,
    ) -> ExperienceBundle:
        """Append one bundle to the JSONL file."""
        if self.get(bundle.experience_id) is not None and not allow_overwrite:
            raise DuplicateExperienceError(bundle.experience_id)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(bundle.to_json().replace("\n", "") + "\n")
        return bundle

    def get(self, experience_id: str) -> ExperienceBundle | None:
        """Return the latest bundle for an experience ID."""
        found: ExperienceBundle | None = None
        for bundle in self._read_all_raw():
            if bundle.experience_id == experience_id:
                found = bundle
        return found

    def list(
        self,
        filters: ExperienceFilter | None = None,
        pagination: Pagination | None = None,
    ) -> builtin_list[ExperienceBundle]:
        """Return latest bundles in first-inserted stable order."""
        latest: dict[str, ExperienceBundle] = {}
        order: builtin_list[str] = []
        for bundle in self._read_all_raw():
            if bundle.experience_id not in latest:
                order.append(bundle.experience_id)
            latest[bundle.experience_id] = bundle
        selected = [latest[experience_id] for experience_id in order]
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
