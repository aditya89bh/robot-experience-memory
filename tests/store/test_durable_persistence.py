import pytest

from robot_experience_memory.store import JSONLMemoryStore, SQLiteMemoryStore
from tests.store.factories import make_bundle


@pytest.mark.parametrize("store_type", ["jsonl", "sqlite"])
def test_durable_stores_survive_reopen(tmp_path, store_type: str) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / f"memory.{store_type}"
    store = JSONLMemoryStore(path) if store_type == "jsonl" else SQLiteMemoryStore(path)
    bundles = [make_bundle("exp-1"), make_bundle("exp-2")]
    store.put_many(bundles)

    reopened = (
        JSONLMemoryStore(path)
        if store_type == "jsonl"
        else SQLiteMemoryStore(path)
    )

    assert reopened.get("exp-1") == bundles[0]
    assert reopened.list() == bundles
