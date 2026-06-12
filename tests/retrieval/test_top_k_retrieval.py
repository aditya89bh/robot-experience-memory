import pytest
from pydantic import ValidationError

from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_retrieval_query_validates_top_k_positive() -> None:
    with pytest.raises(ValidationError):
        RetrievalQuery(top_k=0)


def test_engine_returns_at_most_top_k_matches() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))
    store.put(make_bundle("exp-2"))

    result = RetrievalEngine(store).retrieve(RetrievalQuery(top_k=1))

    assert len(result.matches) == 1
