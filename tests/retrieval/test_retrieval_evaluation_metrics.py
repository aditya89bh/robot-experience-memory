from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalQuery,
    evaluate_retrieval_result,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_retrieval_evaluation_metrics_report_precision_and_recall() -> None:
    store = InMemoryStore()
    store.put_many(
        [
            make_bundle("exp-1", action_type="pick", tag="cnc"),
            make_bundle("exp-2", action_type="pick", tag="cnc"),
            make_bundle("exp-3", action_type="place", tag="cnc"),
        ]
    )
    result = RetrievalEngine(store).retrieve(
        RetrievalQuery(action_type="pick", top_k=2)
    )

    metrics = evaluate_retrieval_result(result, ["exp-1", "exp-2", "exp-99"])

    assert metrics.true_positives == 2
    assert metrics.precision_at_k == 1.0
    assert metrics.recall_at_k == 0.6667
