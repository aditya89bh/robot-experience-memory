"""Lightweight benchmark for recovery suggestion latency."""

from __future__ import annotations

import argparse
import json
from time import perf_counter

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.recovery import RecoveryEngine
from robot_experience_memory.store import ExperienceBundle, InMemoryStore
from robot_experience_memory.timestamps import utc_now


def make_synthetic_bundle(index: int, *, success: bool) -> ExperienceBundle:
    """Create a deterministic synthetic bundle for benchmark stores."""
    experience_id = f"bench-{index}"
    action_type = "navigate" if index % 3 else "reroute"
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id=experience_id,
            state_id=f"state-{index}",
            action_id=f"action-{index}",
            outcome_id=f"outcome-{index}",
            metadata_id=f"metadata-{index}",
        ),
        state=StateSnapshot(state_id=f"state-{index}"),
        action=ActionRecord(
            action_id=f"action-{index}",
            action_type=action_type,
            command=action_type,
        ),
        outcome=OutcomeRecord(
            outcome_id=f"outcome-{index}",
            success=success,
            summary="ok" if success else "blocked",
            error_code=None if success else "blocked",
        ),
        metadata=Metadata(
            metadata_id=f"metadata-{index}",
            robot_id="robot-a",
            environment="lab",
            tags=("benchmark",),
        ),
        stored_at=utc_now(),
    )


def build_store(size: int) -> tuple[InMemoryStore, ExperienceBundle]:
    """Build a synthetic store and return a target failed experience."""
    store = InMemoryStore()
    target = make_synthetic_bundle(0, success=False)
    store.put(target)
    for index in range(1, size):
        store.put(make_synthetic_bundle(index, success=index % 4 != 0))
    return store, target


def run_benchmark(size: int, iterations: int) -> dict[str, float | int | str]:
    """Measure average recovery suggestion time in milliseconds."""
    store, target = build_store(size)
    engine = RecoveryEngine(store)
    start = perf_counter()
    last_type = ""
    for _ in range(iterations):
        last_type = engine.suggest_recovery(target).suggestion_type
    elapsed = perf_counter() - start
    return {
        "store_size": size,
        "iterations": iterations,
        "total_ms": round(elapsed * 1000, 4),
        "average_ms": round((elapsed / iterations) * 1000, 4),
        "last_suggestion_type": last_type,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=1000)
    parser.add_argument("--iterations", type=int, default=100)
    args = parser.parse_args()
    print(
        json.dumps(
            run_benchmark(args.size, args.iterations), indent=2, sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
