import pytest
from pydantic import ValidationError

from robot_experience_memory.store import (
    InMemoryStore,
    JSONLMemoryStore,
    SQLiteMemoryStore,
    StoreConfig,
    create_memory_store,
)


def test_create_memory_store_selects_memory_backend() -> None:
    assert isinstance(create_memory_store(StoreConfig()), InMemoryStore)


def test_create_memory_store_selects_jsonl_backend(tmp_path) -> None:  # type: ignore[no-untyped-def]
    config = StoreConfig(backend="jsonl", path=tmp_path / "m.jsonl")
    store = create_memory_store(config)

    assert isinstance(store, JSONLMemoryStore)


def test_create_memory_store_selects_sqlite_backend(tmp_path) -> None:  # type: ignore[no-untyped-def]
    config = StoreConfig(backend="sqlite", path=tmp_path / "m.sqlite3")
    store = create_memory_store(config)

    assert isinstance(store, SQLiteMemoryStore)


def test_durable_backends_require_path() -> None:
    with pytest.raises(ValidationError, match="path is required"):
        StoreConfig(backend="jsonl")
