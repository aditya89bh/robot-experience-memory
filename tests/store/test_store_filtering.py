from datetime import UTC, datetime

from robot_experience_memory.store import InMemoryStore
from robot_experience_memory.store.filters import ExperienceFilter
from tests.store.factories import make_bundle


def test_store_filters_by_core_reference_ids() -> None:
    store = InMemoryStore()
    bundle = make_bundle("exp-1")
    store.put(bundle)

    assert store.list(ExperienceFilter(experience_id="exp-1")) == [bundle]
    assert store.list(ExperienceFilter(state_id=bundle.state.state_id)) == [bundle]
    assert store.list(ExperienceFilter(action_id=bundle.action.action_id)) == [bundle]
    assert store.list(ExperienceFilter(outcome_id=bundle.outcome.outcome_id)) == [
        bundle
    ]
    assert store.list(ExperienceFilter(metadata_id=bundle.metadata.metadata_id)) == [
        bundle
    ]


def test_store_filters_by_robot_context_action_and_result() -> None:
    store = InMemoryStore()
    success = make_bundle("exp-1", robot_id="r1", environment="lab", tag="nav")
    failure = make_bundle(
        "exp-2",
        robot_id="r2",
        environment="field",
        tag="recovery",
        success=False,
        action_type="recover",
    )
    store.put_many([success, failure])

    assert store.list(ExperienceFilter(robot_id="r1")) == [success]
    assert store.list(ExperienceFilter(environment="field")) == [failure]
    assert store.list(ExperienceFilter(tag="recovery")) == [failure]
    assert store.list(ExperienceFilter(success=False)) == [failure]
    assert store.list(ExperienceFilter(action_type="recover")) == [failure]


def test_store_filters_by_stored_time_range() -> None:
    store = InMemoryStore()
    old = make_bundle("exp-1", stored_at=datetime(2026, 1, 1, tzinfo=UTC))
    new = make_bundle("exp-2", stored_at=datetime(2026, 1, 2, tzinfo=UTC))
    store.put_many([old, new])

    after = ExperienceFilter(stored_after=datetime(2026, 1, 2, tzinfo=UTC))
    before = ExperienceFilter(stored_before=datetime(2026, 1, 1, tzinfo=UTC))

    assert store.list(after) == [new]
    assert store.list(before) == [old]
