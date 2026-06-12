import pytest

from robot_experience_memory.store import DuplicateExperienceError, InMemoryStore
from tests.store.factories import make_bundle


def test_put_many_rejects_duplicate_ids() -> None:
    store = InMemoryStore()
    bundle = make_bundle("exp-1")

    with pytest.raises(DuplicateExperienceError):
        store.put_many([bundle, bundle])


def test_put_many_rejects_duplicate_ids_even_when_overwrite_requested() -> None:
    store = InMemoryStore()
    first = make_bundle("exp-1", success=False)
    second = make_bundle("exp-1", success=True)

    with pytest.raises(DuplicateExperienceError):
        store.put_many([first, second], allow_overwrite=True)

    assert store.list() == [first]
