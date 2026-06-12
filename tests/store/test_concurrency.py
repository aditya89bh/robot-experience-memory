from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery
from robot_experience_memory.store import InMemoryStore, SQLiteMemoryStore
from tests.store.factories import make_bundle


def test_in_memory_store_handles_parallel_distinct_writes() -> None:
    store = InMemoryStore()

    def write(index: int) -> str:
        bundle = make_bundle(f"exp-{index}", robot_id=f"robot-{index % 3}")
        store.put(bundle)
        return bundle.experience_id

    with ThreadPoolExecutor(max_workers=4) as executor:
        ids = list(executor.map(write, range(24)))

    assert sorted(ids) == sorted(bundle.experience_id for bundle in store.list())


def test_retrieval_can_run_while_memory_is_read_many_times() -> None:
    store = InMemoryStore()
    store.put_many([make_bundle(f"exp-{index}") for index in range(20)])
    engine = RetrievalEngine(store, cache_enabled=False)

    def retrieve(_: int) -> int:
        result = engine.retrieve(RetrievalQuery(robot_id="robot-a", top_k=5))
        return len(result.matches)

    with ThreadPoolExecutor(max_workers=4) as executor:
        counts = list(executor.map(retrieve, range(16)))

    assert counts == [5] * 16


def test_sqlite_store_allows_parallel_readers(tmp_path: Path) -> None:
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite")
    store.put_many([make_bundle(f"exp-{index}") for index in range(12)])

    def read_count(_: int) -> int:
        return len(SQLiteMemoryStore(tmp_path / "memory.sqlite").list())

    with ThreadPoolExecutor(max_workers=4) as executor:
        counts = list(executor.map(read_count, range(8)))

    assert counts == [12] * 8
