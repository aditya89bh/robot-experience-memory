import pytest
from pydantic import ValidationError

from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalQuery,
    RetrievalWeights,
    weighted_similarity_score,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_retrieval_weights_validate_non_negative() -> None:
    with pytest.raises(ValidationError):
        RetrievalWeights(action=-1)


def test_retrieval_weights_require_positive_total() -> None:
    with pytest.raises(ValidationError):
        RetrievalWeights(action=0, metadata=0, tags=0, outcome=0, temporal=0)


def test_weighted_similarity_can_prioritize_action() -> None:
    bundle = make_bundle("exp-1", action_type="navigate")
    weights = RetrievalWeights(action=2, metadata=0, tags=0, outcome=0, temporal=0)

    score = weighted_similarity_score(
        RetrievalQuery(action_type="navigate"), bundle, weights
    )

    assert score == 1.0


def test_engine_uses_configured_weights() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", action_type="navigate"))
    engine = RetrievalEngine(
        store,
        weights=RetrievalWeights(action=1, metadata=0, tags=0, outcome=0, temporal=0),
    )

    result = engine.retrieve(RetrievalQuery(action_type="navigate"))

    assert result.matches[0].score == 1.0
