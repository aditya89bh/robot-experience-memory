import pytest

from robot_experience_memory.store import DuplicateExperienceError, InMemoryStore
from tests.store.factories import make_bundle


def test_store_rejects_duplicate_experience_ids_by_default() -> None:
    store = InMemoryStore()
    bundle = make_bundle("exp-1")
    store.put(bundle)

    with pytest.raises(DuplicateExperienceError, match="exp-1"):
        store.put(bundle)


def test_store_allows_explicit_overwrite_without_reordering() -> None:
    store = InMemoryStore()
    first = make_bundle("exp-1", success=False)
    second = make_bundle("exp-1", success=True)

    store.put(first)
    store.put(second, allow_overwrite=True)

    assert store.get("exp-1") == second
    assert store.list() == [second]
