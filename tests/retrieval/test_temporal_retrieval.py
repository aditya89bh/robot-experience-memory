from datetime import UTC, datetime

from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalQuery,
    RetrievalWeights,
    temporal_recency_scores,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_temporal_recency_scores_prefer_recent_bundles() -> None:
    older = make_bundle("exp-1", stored_at=datetime(2026, 1, 1, tzinfo=UTC))
    newer = make_bundle("exp-2", stored_at=datetime(2026, 1, 2, tzinfo=UTC))

    scores = temporal_recency_scores([newer, older])

    assert scores["exp-2"] > scores["exp-1"]
    assert scores["exp-2"] == 1.0


def test_temporal_weight_influences_engine_scores() -> None:
    store = InMemoryStore()
    older = make_bundle("exp-1", stored_at=datetime(2026, 1, 1, tzinfo=UTC))
    newer = make_bundle("exp-2", stored_at=datetime(2026, 1, 2, tzinfo=UTC))
    store.put(older)
    store.put(newer)
    engine = RetrievalEngine(
        store,
        weights=RetrievalWeights(action=0, metadata=0, tags=0, outcome=0, temporal=1),
    )

    result = engine.retrieve(RetrievalQuery())
    scores = {
        match.experience.experience.experience_id: match.score
        for match in result.matches
    }

    assert scores["exp-2"] > scores["exp-1"]
