from robot_experience_memory.retrieval import (
    RetrievalCache,
    RetrievalEngine,
    RetrievalQuery,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_retrieval_cache_key_is_deterministic() -> None:
    cache = RetrievalCache()
    query = RetrievalQuery(action_type="navigate", tags=("nav",))

    assert cache.key_for(query) == cache.key_for(query)


def test_engine_reuses_cached_results_when_enabled() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))
    engine = RetrievalEngine(store)
    query = RetrievalQuery(action_type="navigate")

    first = engine.retrieve(query)
    store.put(make_bundle("exp-2"))
    second = engine.retrieve(query)

    assert second == first


def test_engine_can_disable_cache() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))
    engine = RetrievalEngine(store, cache_enabled=False)
    query = RetrievalQuery(action_type="navigate")

    first = engine.retrieve(query)
    store.put(make_bundle("exp-2"))
    second = engine.retrieve(query)

    assert len(first.matches) == 1
    assert len(second.matches) == 2
