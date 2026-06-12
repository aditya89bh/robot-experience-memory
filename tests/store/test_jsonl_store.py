from pathlib import Path

from robot_experience_memory.store import JSONLMemoryStore
from tests.store.factories import make_bundle


def test_jsonl_store_persists_bundle(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    bundle = make_bundle("exp-1")

    JSONLMemoryStore(path).put(bundle)

    restored = JSONLMemoryStore(path)
    assert restored.get("exp-1") == bundle
    assert restored.list() == [bundle]
