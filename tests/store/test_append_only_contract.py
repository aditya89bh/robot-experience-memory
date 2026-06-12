from collections.abc import Callable

import pytest

from robot_experience_memory.store import (
    DuplicateExperienceError,
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


def test_all_backends_reject_duplicate_ids(
    store_factory: Callable[[], MemoryStore],
) -> None:
    store = store_factory()
    first = make_bundle("exp-1", success=False)
    second = make_bundle("exp-1", success=True)

    store.put(first)

    with pytest.raises(DuplicateExperienceError):
        store.put(second)

    assert store.get("exp-1") == first


def test_all_backends_reject_duplicates_even_with_legacy_overwrite_flag(
    store_factory: Callable[[], MemoryStore],
) -> None:
    store = store_factory()
    first = make_bundle("exp-1", success=False)
    second = make_bundle("exp-1", success=True)

    store.put(first)

    with pytest.raises(DuplicateExperienceError):
        store.put(second, allow_overwrite=True)

    assert store.get("exp-1") == first
