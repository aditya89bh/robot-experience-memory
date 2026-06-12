from robot_experience_memory.replay import ReplayEngine, ReplayReport
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


def test_replay_returns_report_shape() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))

    report = ReplayEngine(store).replay()

    assert isinstance(report, ReplayReport)
    assert report.total_experiences == 1
    assert report.success_count == 1
    assert report.failure_count == 0
    assert report.total_events == len(report.events)
    assert report.duration_seconds >= 0.0
    assert report.interrupted is False
    assert report.interruption_reason is None


def test_replay_report_serializes_to_json_safe_dict() -> None:
    report = ReplayEngine(InMemoryStore()).replay()

    data = report.to_dict()

    assert data["total_events"] == 2
    assert data["interrupted"] is False
    assert "started_at" in data
    assert "completed_at" in data
