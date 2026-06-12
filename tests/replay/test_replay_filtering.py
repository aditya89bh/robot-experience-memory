from collections.abc import Sequence

from robot_experience_memory.replay import ReplayEngine, ReplayEvent
from robot_experience_memory.store import ExperienceFilter, InMemoryStore, Pagination
from tests.store.factories import make_bundle


def replayed_ids(events: Sequence[ReplayEvent]) -> list[str | None]:
    return [
        event.experience_id
        for event in events
        if event.event_type == "experience_started"
    ]


def test_replay_filters_by_success() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", success=True))
    store.put(make_bundle("exp-2", success=False))

    events = ReplayEngine(store).replay(filters=ExperienceFilter(success=False)).events

    assert replayed_ids(events) == ["exp-2"]


def test_replay_filters_by_robot_id() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", robot_id="robot-a"))
    store.put(make_bundle("exp-2", robot_id="robot-b"))

    events = ReplayEngine(store).replay(
        filters=ExperienceFilter(robot_id="robot-b")
    ).events

    assert replayed_ids(events) == ["exp-2"]


def test_replay_filters_by_action_type() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1", action_type="navigate"))
    store.put(make_bundle("exp-2", action_type="grasp"))

    events = ReplayEngine(store).replay(
        filters=ExperienceFilter(action_type="grasp")
    ).events

    assert replayed_ids(events) == ["exp-2"]


def test_replay_applies_pagination() -> None:
    store = InMemoryStore()
    store.put(make_bundle("exp-1"))
    store.put(make_bundle("exp-2"))

    events = ReplayEngine(store).replay(pagination=Pagination(offset=1, limit=1)).events

    assert replayed_ids(events) == ["exp-2"]
