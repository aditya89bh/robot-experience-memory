from robot_experience_memory.recovery import RecoveryEngine
from robot_experience_memory.retrieval import RetrievalEngine
from robot_experience_memory.ros2 import (
    handle_recovery_request,
    handle_retrieval_request,
)
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_handle_retrieval_request_uses_duck_typed_callbacks() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", action_type="dock"))
    engine = RetrievalEngine(store)

    response = handle_retrieval_request(
        {"query": {"action_type": "dock"}},
        engine=engine,
        parse_request=lambda request: request,
        build_response=lambda payload: payload,
    )

    assert response["matches"][0]["experience_id"] == "exp-1"


def test_handle_recovery_request_uses_duck_typed_callbacks() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", success=False))
    engine = RecoveryEngine(store)

    response = handle_recovery_request(
        {"experience_id": "exp-1"},
        engine=engine,
        parse_request=lambda request: request,
        build_response=lambda payload: payload,
    )

    assert "suggestion_type" in response
    assert "confidence" in response
