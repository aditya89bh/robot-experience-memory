from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_store_put_many_and_get_many_preserve_order() -> None:
    store = InMemoryStore()
    bundles = [make_bundle("exp-1"), make_bundle("exp-2")]

    assert store.put_many(bundles) == bundles
    assert store.get_many(["exp-2", "missing", "exp-1"]) == [
        bundles[1],
        None,
        bundles[0],
    ]
