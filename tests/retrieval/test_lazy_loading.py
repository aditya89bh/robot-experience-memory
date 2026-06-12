from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery
from robot_experience_memory.store import (
    ExperienceBundle,
    ExperienceFilter,
    InMemoryStore,
)
from tests.store.factories import make_bundle


class RecordingStore(InMemoryStore):
    def __init__(self) -> None:
        super().__init__()
        self.last_filter: ExperienceFilter | None = None

    def list(
        self,
        filters: ExperienceFilter | None = None,
        pagination: object | None = None,
    ) -> list[ExperienceBundle]:
        self.last_filter = filters
        return super().list(filters=filters, pagination=pagination)  # type: ignore[arg-type]


def test_retrieval_engine_uses_planned_filter_for_candidate_loading() -> None:
    store = RecordingStore()
    store.put_many(
        [
            make_bundle("exp-1", robot_id="robot-a", action_type="pick"),
            make_bundle("exp-2", robot_id="robot-b", action_type="place"),
        ]
    )

    result = RetrievalEngine(store, cache_enabled=False).retrieve(
        RetrievalQuery(robot_id="robot-a", action_type="pick")
    )

    assert [match.experience.experience_id for match in result.matches] == ["exp-1"]
    assert store.last_filter is not None
    assert store.last_filter.robot_id == "robot-a"
    assert store.last_filter.action_type == "pick"
