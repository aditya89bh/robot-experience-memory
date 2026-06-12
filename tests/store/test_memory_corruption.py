from pathlib import Path

import pytest
from pydantic import ValidationError

from robot_experience_memory.store import JSONLMemoryStore, SQLiteMemoryStore
from tests.store.factories import make_bundle


def test_jsonl_store_rejects_corrupt_lines_on_load(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    JSONLMemoryStore(path).put(make_bundle("exp-1"))
    with path.open("a", encoding="utf-8") as file:
        file.write("{not-valid-json}\n")

    with pytest.raises(ValueError):
        JSONLMemoryStore(path)


def test_jsonl_store_rejects_schema_corruption_on_load(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    path.write_text('{"experience": {"experience_id": "missing"}}\n', encoding="utf-8")

    with pytest.raises(ValidationError):
        JSONLMemoryStore(path)


def test_sqlite_store_rejects_non_database_file(tmp_path: Path) -> None:
    path = tmp_path / "memory.sqlite"
    path.write_text("this is not sqlite", encoding="utf-8")

    with pytest.raises(Exception, match="file is not a database|malformed"):
        SQLiteMemoryStore(path)
