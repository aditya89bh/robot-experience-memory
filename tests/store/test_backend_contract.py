from collections.abc import Callable

import pytest

from robot_experience_memory.store import (
    JSONLMemoryStore,
    MemoryStore,
    SQLiteMemoryStore,
)
from robot_experience_memory.store.memory import InMemoryStore
from tests.store.factories import make_bundle


@pytest.fixture(params=["memory", "jsonl", "sqlite"])
def store_factory(tmp_path, request) -> Callable[[], MemoryStore]:  # type: ignore[no-untyped-def]
    backend = str(request.param)
    if backend == "memory":
        return InMemoryStore
    if backend == "jsonl":
        return lambda: JSONLMemoryStore(tmp_path / "memory.jsonl")
    return lambda: SQLiteMemoryStore(tmp_path / "memory.sqlite3")


def test_backend_contract_put_get_list(
    store_factory: Callable[[], MemoryStore],
) -> None:
    store = store_factory()
    first = make_bundle("exp-1")
    second = make_bundle("exp-2")

    store.put(first)
    store.put(second)

    assert store.get("exp-1") == first
    assert store.get("missing") is None
    assert store.list() == [first, second]
