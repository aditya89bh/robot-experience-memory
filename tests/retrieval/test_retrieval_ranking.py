from datetime import UTC, datetime

from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_retrieval_ranking_sorts_by_score_descending() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", action_type="dock"))
    store.put(make_bundle("exp-2", action_type="navigate"))

    result = RetrievalEngine(store).retrieve(RetrievalQuery(action_type="navigate"))

    assert result.matches[0].experience.experience.experience_id == "exp-2"


def test_retrieval_ranking_tiebreaks_by_recent_then_id() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-b", stored_at=datetime(2026, 1, 1, tzinfo=UTC)))
    store.put(make_bundle("exp-a", stored_at=datetime(2026, 1, 1, tzinfo=UTC)))
    store.put(make_bundle("exp-c", stored_at=datetime(2026, 1, 2, tzinfo=UTC)))

    result = RetrievalEngine(store).retrieve(RetrievalQuery())

    assert [match.experience.experience.experience_id for match in result.matches] == [
        "exp-c",
        "exp-a",
        "exp-b",
    ]
