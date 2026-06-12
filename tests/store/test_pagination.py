from robot_experience_memory.store import InMemoryStore
from robot_experience_memory.store.filters import Pagination
from tests.store.factories import make_bundle


def test_store_pagination_uses_stable_insertion_order() -> None:
    store = InMemoryStore()
    bundles = [make_bundle(f"exp-{index}") for index in range(5)]
    store.put_many(bundles)

    assert store.list(pagination=Pagination(limit=2)) == bundles[:2]
    assert store.list(pagination=Pagination(limit=2, offset=2)) == bundles[2:4]
    assert store.list(pagination=Pagination(offset=4)) == bundles[4:]
