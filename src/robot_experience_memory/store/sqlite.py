"""SQLite backend for robot experience memory."""

import sqlite3
from pathlib import Path

from robot_experience_memory.store.base import MemoryStore
from robot_experience_memory.store.bundle import ExperienceBundle
from robot_experience_memory.store.errors import DuplicateExperienceError
from robot_experience_memory.store.filters import ExperienceFilter, Pagination


class SQLiteMemoryStore(MemoryStore):
    """SQLite-backed store for durable local robot experience persistence."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def put(
        self,
        bundle: ExperienceBundle,
        *,
        allow_overwrite: bool = False,
    ) -> ExperienceBundle:
        """Persist one bundle in SQLite."""
        statement = """
            INSERT INTO experiences (experience_id, bundle_json)
            VALUES (?, ?)
        """
        if allow_overwrite:
            statement = """
                INSERT OR REPLACE INTO experiences (experience_id, bundle_json)
                VALUES (?, ?)
            """
        try:
            with self._connect() as connection:
                connection.execute(statement, (bundle.experience_id, bundle.to_json()))
        except sqlite3.IntegrityError as exc:
            raise DuplicateExperienceError(bundle.experience_id) from exc
        return bundle

    def get(self, experience_id: str) -> ExperienceBundle | None:
        """Return one bundle by experience ID."""
        with self._connect() as connection:
            row = connection.execute(
                "SELECT bundle_json FROM experiences WHERE experience_id = ?",
                (experience_id,),
            ).fetchone()
        if row is None:
            return None
        return ExperienceBundle.from_json(str(row[0]))

    def list(
        self,
        filters: ExperienceFilter | None = None,
        pagination: Pagination | None = None,
    ) -> list[ExperienceBundle]:
        """Return bundles in SQLite insertion order."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT bundle_json FROM experiences ORDER BY rowid ASC"
            ).fetchall()
        selected = [ExperienceBundle.from_json(str(row[0])) for row in rows]
        if filters is not None:
            selected = [bundle for bundle in selected if filters.matches(bundle)]
        if pagination is not None:
            selected = pagination.apply(selected)
        return selected

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS experiences (
                    experience_id TEXT PRIMARY KEY,
                    bundle_json TEXT NOT NULL
                )
                """
            )
