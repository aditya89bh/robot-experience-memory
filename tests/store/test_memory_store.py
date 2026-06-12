from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_in_memory_store_put_get_and_list() -> None:
    store = InMemoryStore()
    bundle = make_bundle("exp-1")

    assert store.put(bundle) == bundle
    assert store.get("exp-1") == bundle
    assert store.list() == [bundle]
    assert store.get("missing") is None
