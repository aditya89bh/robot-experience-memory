"""Lightweight benchmarks for deterministic retrieval."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from time import perf_counter

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery
from robot_experience_memory.store import ExperienceBundle, InMemoryStore


def make_benchmark_bundle(index: int) -> ExperienceBundle:
    """Create a deterministic synthetic benchmark bundle."""
    experience_id = f"exp-{index:05d}"
    action_type = "navigate" if index % 2 == 0 else "dock"
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id=experience_id,
            state_id=f"state-{index:05d}",
            action_id=f"action-{index:05d}",
            outcome_id=f"outcome-{index:05d}",
            metadata_id=f"metadata-{index:05d}",
        ),
        state=StateSnapshot(state_id=f"state-{index:05d}"),
        action=ActionRecord(
            action_id=f"action-{index:05d}",
            action_type=action_type,
            command=action_type,
        ),
        outcome=OutcomeRecord(
            outcome_id=f"outcome-{index:05d}",
            success=index % 3 != 0,
            summary="benchmark outcome",
        ),
        metadata=Metadata(
            metadata_id=f"metadata-{index:05d}",
            robot_id=f"robot-{index % 4}",
            environment=f"zone-{index % 3}",
            tags=("navigation" if index % 2 == 0 else "charging",),
        ),
        stored_at=datetime(2026, 1, 1, tzinfo=UTC) + timedelta(seconds=index),
    )


def build_store(size: int) -> InMemoryStore:
    """Build an in-memory store with synthetic experiences."""
    store = InMemoryStore()
    for index in range(size):
        store.put(make_benchmark_bundle(index))
    return store


def benchmark_size(size: int, iterations: int) -> dict[str, float | int]:
    """Benchmark retrieval over one synthetic store size."""
    store = build_store(size)
    engine = RetrievalEngine(store)
    query = RetrievalQuery(
        action_type="navigate",
        robot_id="robot-0",
        tags=("navigation",),
        top_k=5,
    )

    start = perf_counter()
    for _ in range(iterations):
        engine.retrieve(query)
    elapsed = perf_counter() - start
    return {
        "store_size": size,
        "iterations": iterations,
        "total_seconds": round(elapsed, 6),
        "average_seconds": round(elapsed / iterations, 6),
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the benchmark CLI parser."""
    parser = argparse.ArgumentParser(description="Benchmark retrieval latency")
    parser.add_argument("--sizes", nargs="+", type=int, default=[10, 100, 1000])
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run retrieval benchmarks."""
    args = build_parser().parse_args(argv)
    results = [benchmark_size(size, args.iterations) for size in args.sizes]
    if args.as_json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for result in results:
            print(
                "retrieval "
                f"size={result['store_size']} "
                f"iterations={result['iterations']} "
                f"avg={result['average_seconds']}s"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
