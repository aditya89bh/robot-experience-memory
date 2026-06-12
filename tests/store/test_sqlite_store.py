from robot_experience_memory.store import SQLiteMemoryStore
from tests.store.factories import make_bundle


def test_sqlite_store_persists_bundle(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "memory.sqlite3"
    bundle = make_bundle("exp-1")

    SQLiteMemoryStore(path).put(bundle)

    restored = SQLiteMemoryStore(path)
    assert restored.get("exp-1") == bundle
    assert restored.list() == [bundle]
