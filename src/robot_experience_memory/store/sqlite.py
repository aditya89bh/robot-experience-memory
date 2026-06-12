"""SQLite backend for robot experience memory."""

from __future__ import annotations

import json
import sqlite3
from builtins import list as builtin_list
from pathlib import Path
from typing import Any

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
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
        """Persist one bundle in normalized SQLite tables."""
        try:
            with self._connect() as connection:
                self._insert_bundle(connection, bundle, allow_overwrite=allow_overwrite)
        except sqlite3.IntegrityError as exc:
            raise DuplicateExperienceError(bundle.experience_id) from exc
        return bundle

    def put_many(
        self,
        bundles: builtin_list[ExperienceBundle],
        *,
        allow_overwrite: bool = False,
    ) -> builtin_list[ExperienceBundle]:
        """Persist a batch atomically in input order."""
        try:
            with self._connect() as connection:
                for bundle in bundles:
                    self._insert_bundle(
                        connection,
                        bundle,
                        allow_overwrite=allow_overwrite,
                    )
        except sqlite3.IntegrityError as exc:
            experience_id = self._first_duplicate_id(bundles)
            raise DuplicateExperienceError(experience_id) from exc
        return bundles

    def get(self, experience_id: str) -> ExperienceBundle | None:
        """Return one bundle by experience ID."""
        with self._connect() as connection:
            row = connection.execute(
                self._select_sql() + " WHERE experiences.experience_id = ?",
                (experience_id,),
            ).fetchone()
        if row is None:
            return None
        return self._bundle_from_row(row)

    def list(
        self,
        filters: ExperienceFilter | None = None,
        pagination: Pagination | None = None,
    ) -> builtin_list[ExperienceBundle]:
        """Return bundles in SQLite insertion order."""
        with self._connect() as connection:
            rows = connection.execute(
                self._select_sql() + " ORDER BY experiences.rowid ASC"
            ).fetchall()
        selected = [self._bundle_from_row(row) for row in rows]
        if filters is not None:
            selected = [bundle for bundle in selected if filters.matches(bundle)]
        if pagination is not None:
            selected = pagination.apply(selected)
        return selected

    def _insert_bundle(
        self,
        connection: sqlite3.Connection,
        bundle: ExperienceBundle,
        *,
        allow_overwrite: bool,
    ) -> None:
        _ = allow_overwrite
        connection.execute(
            """
            INSERT INTO states (state_id, payload_json)
            VALUES (?, ?)
            """,
            (bundle.state.state_id, bundle.state.to_json()),
        )
        connection.execute(
            """
            INSERT INTO actions (action_id, action_type, payload_json)
            VALUES (?, ?, ?)
            """,
            (
                bundle.action.action_id,
                bundle.action.action_type,
                bundle.action.to_json(),
            ),
        )
        connection.execute(
            """
            INSERT INTO outcomes (outcome_id, success, payload_json)
            VALUES (?, ?, ?)
            """,
            (
                bundle.outcome.outcome_id,
                int(bundle.outcome.success),
                bundle.outcome.to_json(),
            ),
        )
        connection.execute(
            """
            INSERT INTO metadata_records (
                metadata_id,
                robot_id,
                operator,
                environment,
                tags_json,
                payload_json
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                bundle.metadata.metadata_id,
                bundle.metadata.robot_id,
                bundle.metadata.operator,
                bundle.metadata.environment,
                json.dumps(list(bundle.metadata.tags)),
                bundle.metadata.to_json(),
            ),
        )
        connection.execute(
            """
            INSERT INTO experiences (
                experience_id,
                state_id,
                action_id,
                outcome_id,
                metadata_id,
                stored_at,
                payload_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                bundle.experience.experience_id,
                bundle.experience.state_id,
                bundle.experience.action_id,
                bundle.experience.outcome_id,
                bundle.experience.metadata_id,
                bundle.stored_at.isoformat(),
                bundle.experience.to_json(),
            ),
        )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS states (
                    state_id TEXT PRIMARY KEY,
                    payload_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS actions (
                    action_id TEXT PRIMARY KEY,
                    action_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS outcomes (
                    outcome_id TEXT PRIMARY KEY,
                    success INTEGER NOT NULL,
                    payload_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS metadata_records (
                    metadata_id TEXT PRIMARY KEY,
                    robot_id TEXT NOT NULL,
                    operator TEXT,
                    environment TEXT NOT NULL,
                    tags_json TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS experiences (
                    experience_id TEXT PRIMARY KEY,
                    state_id TEXT NOT NULL REFERENCES states(state_id),
                    action_id TEXT NOT NULL REFERENCES actions(action_id),
                    outcome_id TEXT NOT NULL REFERENCES outcomes(outcome_id),
                    metadata_id TEXT NOT NULL REFERENCES metadata_records(metadata_id),
                    stored_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_experiences_state_id
                    ON experiences(state_id);
                CREATE INDEX IF NOT EXISTS idx_experiences_action_id
                    ON experiences(action_id);
                CREATE INDEX IF NOT EXISTS idx_experiences_outcome_id
                    ON experiences(outcome_id);
                CREATE INDEX IF NOT EXISTS idx_experiences_metadata_id
                    ON experiences(metadata_id);
                CREATE INDEX IF NOT EXISTS idx_actions_action_type
                    ON actions(action_type);
                CREATE INDEX IF NOT EXISTS idx_outcomes_success
                    ON outcomes(success);
                CREATE INDEX IF NOT EXISTS idx_metadata_robot_id
                    ON metadata_records(robot_id);
                CREATE INDEX IF NOT EXISTS idx_metadata_environment
                    ON metadata_records(environment);
                CREATE INDEX IF NOT EXISTS idx_metadata_operator
                    ON metadata_records(operator);
                """
            )

    def _select_sql(self) -> str:
        return """
            SELECT
                experiences.payload_json AS experience_json,
                states.payload_json AS state_json,
                actions.payload_json AS action_json,
                outcomes.payload_json AS outcome_json,
                metadata_records.payload_json AS metadata_json,
                experiences.stored_at AS stored_at
            FROM experiences
            JOIN states ON states.state_id = experiences.state_id
            JOIN actions ON actions.action_id = experiences.action_id
            JOIN outcomes ON outcomes.outcome_id = experiences.outcome_id
            JOIN metadata_records
                ON metadata_records.metadata_id = experiences.metadata_id
        """

    def _bundle_from_row(self, row: sqlite3.Row) -> ExperienceBundle:
        return ExperienceBundle(
            experience=ExperienceRecord.from_json(str(row["experience_json"])),
            state=StateSnapshot.from_json(str(row["state_json"])),
            action=ActionRecord.from_json(str(row["action_json"])),
            outcome=OutcomeRecord.from_json(str(row["outcome_json"])),
            metadata=Metadata.from_json(str(row["metadata_json"])),
            stored_at=ExperienceBundle.model_validate(
                {
                    "experience": json.loads(str(row["experience_json"])),
                    "state": json.loads(str(row["state_json"])),
                    "action": json.loads(str(row["action_json"])),
                    "outcome": json.loads(str(row["outcome_json"])),
                    "metadata": json.loads(str(row["metadata_json"])),
                    "stored_at": row["stored_at"],
                }
            ).stored_at,
        )

    def _first_duplicate_id(self, bundles: builtin_list[ExperienceBundle]) -> str:
        seen: set[str] = set()
        for bundle in bundles:
            if bundle.experience_id in seen:
                return str(bundle.experience_id)
            seen.add(bundle.experience_id)
        return str(bundles[0].experience_id) if bundles else "unknown"

    def indexed_columns(self) -> dict[str, builtin_list[str]]:
        """Return indexed columns for diagnostics and tests."""
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT name, tbl_name
                FROM sqlite_master
                WHERE type = 'index' AND name LIKE 'idx_%'
                ORDER BY name
                """
            ).fetchall()
        indexes: dict[str, builtin_list[str]] = {}
        for row in rows:
            indexes.setdefault(str(row["tbl_name"]), []).append(str(row["name"]))
        return indexes

    def table_counts(self) -> dict[str, int]:
        """Return normalized table row counts for diagnostics and tests."""
        tables: builtin_list[str] = [
            "experiences",
            "states",
            "actions",
            "outcomes",
            "metadata_records",
        ]
        counts: dict[str, int] = {}
        with self._connect() as connection:
            for table in tables:
                row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
                result: Any = row[0]
                counts[table] = int(result)
        return counts
