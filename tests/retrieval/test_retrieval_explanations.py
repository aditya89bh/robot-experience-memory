from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalExplanation,
    RetrievalQuery,
    explain_match,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_explain_match_includes_components_and_reasons() -> None:
    bundle = make_bundle("exp-1", action_type="navigate", robot_id="robot-a")

    explanation = explain_match(
        RetrievalQuery(action_type="navigate", robot_id="robot-a", tags=("nav",)),
        bundle,
    )

    assert isinstance(explanation, RetrievalExplanation)
    assert explanation.components["exact"] > 0
    assert "action_type matched: navigate" in explanation.reasons
    assert "tags overlapped" in explanation.reasons


def test_engine_attaches_explanations_to_matches() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    result = RetrievalEngine(store).retrieve(RetrievalQuery(action_type="navigate"))
    match = result.matches[0]

    assert isinstance(match.explanation, RetrievalExplanation)
