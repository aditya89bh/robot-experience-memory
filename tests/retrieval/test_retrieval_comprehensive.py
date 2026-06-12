from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalExplanation,
    RetrievalQuery,
    RetrievalWeights,
    exact_match_score,
    metadata_similarity_score,
    tag_similarity_score,
    temporal_recency_scores,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_query_validation_rejects_non_positive_top_k() -> None:
    with pytest.raises(ValidationError):
        RetrievalQuery(top_k=0)


def test_engine_answers_action_state_and_outcome_questions() -> None:
    store = InMemoryStore()
    store.put(
        make_bundle(
            "exp-1",
            action_type="navigate",
            robot_id="robot-a",
            environment="lab",
            success=True,
        )
    )
    store.put(
        make_bundle(
            "exp-2",
            action_type="dock",
            robot_id="robot-b",
            environment="field",
            success=False,
        )
    )

    seen_state = RetrievalEngine(store).retrieve(
        RetrievalQuery(robot_id="robot-a", environment="lab")
    )
    tried_action = RetrievalEngine(store).retrieve(
        RetrievalQuery(action_type="dock")
    )
    failed_similar = RetrievalEngine(store).retrieve(RetrievalQuery(success=False))

    assert seen_state.matches[0].experience.experience.experience_id == "exp-1"
    assert tried_action.matches[0].experience.experience.experience_id == "exp-2"
    assert failed_similar.matches[0].experience.outcome.success is False


def test_scoring_helpers_cover_exact_metadata_tags_and_temporal() -> None:
    older = make_bundle(
        "exp-1",
        robot_id="robot-a",
        environment="lab",
        action_type="navigate",
        stored_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    newer = make_bundle(
        "exp-2",
        robot_id="robot-b",
        environment="lab",
        action_type="dock",
        stored_at=datetime(2026, 1, 2, tzinfo=UTC),
    )
    query = RetrievalQuery(
        action_type="navigate",
        robot_id="robot-a",
        environment="lab",
        tags=("nav",),
    )

    assert exact_match_score(query, older) > exact_match_score(query, newer)
    assert metadata_similarity_score(query, older) > metadata_similarity_score(
        query, newer
    )
    assert tag_similarity_score(query, older) == 1.0
    recency = temporal_recency_scores([older, newer])
    assert recency["exp-2"] > recency["exp-1"]


def test_weighted_top_k_ranking_explanations_and_cache_work_together() -> None:
    store = InMemoryStore()
    store.put(
        make_bundle(
            "exp-1",
            action_type="navigate",
            stored_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
    )
    store.put(
        make_bundle(
            "exp-2",
            action_type="navigate",
            stored_at=datetime(2026, 1, 2, tzinfo=UTC),
        )
    )
    engine = RetrievalEngine(
        store,
        weights=RetrievalWeights(action=1, metadata=0, tags=0, outcome=0, temporal=1),
    )
    query = RetrievalQuery(action_type="navigate", top_k=1)

    first = engine.retrieve(query)
    second = engine.retrieve(query)

    assert first is second
    assert len(first.matches) == 1
    assert first.matches[0].experience.experience.experience_id == "exp-2"
    assert isinstance(first.matches[0].explanation, RetrievalExplanation)
    assert first.matches[0].explanation.reasons
