from collections.abc import Callable

import pytest

from robot_experience_memory.store import (
    JSONLMemoryStore,
    MemoryStore,
    SQLiteMemoryStore,
)
from robot_experience_memory.store.filters import ExperienceFilter
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


def test_metadata_query_helpers_work_across_backends(
    store_factory: Callable[[], MemoryStore],
) -> None:
    store = store_factory()
    first = make_bundle("exp-1", robot_id="r1", environment="lab", tag="nav")
    second = make_bundle("exp-2", robot_id="r2", environment="field", tag="recover")
    store.put_many([first, second])

    assert store.query_by_robot_id("r1") == [first]
    assert store.query_by_environment("field") == [second]
    assert store.query_by_tag("recover") == [second]


def test_operator_filter_uses_metadata_operator() -> None:
    bundle = make_bundle("exp-1")
    assert ExperienceFilter(operator="aditya").matches(bundle)
    assert not ExperienceFilter(operator="someone-else").matches(bundle)


def test_memory_and_jsonl_expose_indexed_fields(tmp_path) -> None:  # type: ignore[no-untyped-def]
    memory = InMemoryStore()
    jsonl = JSONLMemoryStore(tmp_path / "memory.jsonl")

    assert "robot_id" in memory.indexed_fields()
    assert "action_type" in jsonl.indexed_fields()
