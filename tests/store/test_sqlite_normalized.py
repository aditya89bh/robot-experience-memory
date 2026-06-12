from pathlib import Path

from robot_experience_memory.store import SQLiteMemoryStore
from tests.store.factories import make_bundle


def test_sqlite_store_uses_normalized_tables(tmp_path: Path) -> None:
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    store.put(make_bundle("exp-1"))

    assert store.table_counts() == {
        "experiences": 1,
        "states": 1,
        "actions": 1,
        "outcomes": 1,
        "metadata_records": 1,
    }


def test_sqlite_store_creates_common_query_indexes(tmp_path: Path) -> None:
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")

    indexes = store.indexed_columns()

    assert "idx_actions_action_type" in indexes["actions"]
    assert "idx_outcomes_success" in indexes["outcomes"]
    assert "idx_metadata_robot_id" in indexes["metadata_records"]
    assert "idx_metadata_environment" in indexes["metadata_records"]
