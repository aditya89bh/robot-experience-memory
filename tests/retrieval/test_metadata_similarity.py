from robot_experience_memory.retrieval import RetrievalQuery, metadata_similarity_score
from tests.store.factories import make_bundle


def test_metadata_similarity_scores_robot_environment_operator() -> None:
    bundle = make_bundle("exp-1", robot_id="robot-a", environment="lab", operator="ada")
    query = RetrievalQuery(robot_id="robot-a", environment="lab", operator="ada")

    assert metadata_similarity_score(query, bundle) == 1.0


def test_metadata_similarity_is_partial_and_deterministic() -> None:
    bundle = make_bundle("exp-1", robot_id="robot-a", environment="lab", operator="ada")
    query = RetrievalQuery(robot_id="robot-a", environment="field", operator="ada")

    assert metadata_similarity_score(query, bundle) == 2 / 3


def test_metadata_similarity_without_metadata_query_is_zero() -> None:
    assert metadata_similarity_score(RetrievalQuery(), make_bundle("exp-1")) == 0.0
