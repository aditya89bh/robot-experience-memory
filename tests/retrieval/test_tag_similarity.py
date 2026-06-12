from robot_experience_memory.retrieval import RetrievalQuery, tag_similarity_score
from tests.store.factories import make_bundle


def test_tag_similarity_uses_jaccard_overlap() -> None:
    bundle = make_bundle("exp-1", tag="nav")
    query = RetrievalQuery(tags=("nav", "blocked"))

    assert tag_similarity_score(query, bundle) == 0.5


def test_tag_similarity_empty_query_is_zero() -> None:
    assert tag_similarity_score(RetrievalQuery(), make_bundle("exp-1")) == 0.0


def test_tag_similarity_no_overlap_is_zero() -> None:
    bundle = make_bundle("exp-1", tag="nav")

    assert tag_similarity_score(RetrievalQuery(tags=("dock",)), bundle) == 0.0
