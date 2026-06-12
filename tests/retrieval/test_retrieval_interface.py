from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalMatch,
    RetrievalQuery,
    RetrievalResult,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_retrieval_engine_returns_typed_result() -> None:
    store = InMemoryStore()
    bundle = make_bundle("exp-1")
    store.put(bundle)

    result = RetrievalEngine(store).retrieve(RetrievalQuery(action_type="navigate"))

    assert isinstance(result, RetrievalResult)
    assert result.query.action_type == "navigate"
    assert result.matches == (RetrievalMatch(experience=bundle, score=1.0),)
