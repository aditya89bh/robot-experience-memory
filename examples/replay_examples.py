"""Runnable examples for replay APIs."""

from robot_experience_memory.replay import ReplayConfig, ReplayEngine, ReplayEvent
from robot_experience_memory.store import ExperienceFilter, InMemoryStore
from tests.store.factories import make_bundle


def build_store() -> InMemoryStore:
    """Build a small in-memory store for examples."""
    store = InMemoryStore()
    store.put(make_bundle("exp-1", robot_id="robot-a", action_type="navigate"))
    store.put(
        make_bundle("exp-2", robot_id="robot-b", action_type="grasp", success=False)
    )
    return store


def main() -> None:
    """Run basic, filtered, callback, failure-only, and deterministic replays."""
    store = build_store()

    basic = ReplayEngine(store, ReplayConfig(speed_multiplier=0.0)).replay()
    print(f"basic replay: {basic.total_experiences} experiences")

    filtered = ReplayEngine(store, ReplayConfig(speed_multiplier=0.0)).replay(
        filters=ExperienceFilter(robot_id="robot-a")
    )
    print(f"filtered replay: {filtered.total_experiences} experiences")

    def callback(event: ReplayEvent) -> None:
        if event.event_type == "experience_started":
            print(f"callback saw {event.experience_id}")

    ReplayEngine(
        store, ReplayConfig(speed_multiplier=0.0), callbacks=[callback]
    ).replay()

    failures = ReplayEngine(store, ReplayConfig(speed_multiplier=0.0)).replay(
        filters=ExperienceFilter(success=False)
    )
    print(f"failure-only replay: {failures.failure_count} failures")

    deterministic = ReplayEngine(store, ReplayConfig(deterministic=True)).replay()
    print(f"deterministic timestamp: {deterministic.events[0].timestamp.isoformat()}")


if __name__ == "__main__":
    main()
