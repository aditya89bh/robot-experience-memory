"""Lightweight deterministic benchmarks for memory store backends.

Run with:

    python benchmarks/benchmark_backends.py
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import Callable
from pathlib import Path
from time import perf_counter

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.store import (
    ExperienceBundle,
    InMemoryStore,
    JSONLMemoryStore,
    MemoryStore,
    SQLiteMemoryStore,
)

BUNDLE_COUNT = 50


def make_bundle(index: int) -> ExperienceBundle:
    """Create a deterministic benchmark bundle."""
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id=f"exp-{index}",
            state_id=f"state-{index}",
            action_id=f"action-{index}",
            outcome_id=f"outcome-{index}",
            metadata_id=f"metadata-{index}",
        ),
        state=StateSnapshot(
            state_id=f"state-{index}",
            joint_positions={"joint": float(index)},
        ),
        action=ActionRecord(
            action_id=f"action-{index}",
            action_type="navigate" if index % 2 == 0 else "recover",
            command="move",
            parameters={"index": index},
        ),
        outcome=OutcomeRecord(
            outcome_id=f"outcome-{index}",
            success=index % 3 != 0,
            summary="ok",
        ),
        metadata=Metadata(
            metadata_id=f"metadata-{index}",
            robot_id=f"robot-{index % 3}",
            operator="benchmark",
            environment="lab",
            tags=("benchmark",),
        ),
    )


def measure(operation: Callable[[], object]) -> float:
    """Return elapsed seconds for one operation."""
    start = perf_counter()
    operation()
    return perf_counter() - start


def run_backend(name: str, store: MemoryStore) -> dict[str, float | int | str]:
    """Run write/read/list operations for a backend."""
    bundles = [make_bundle(index) for index in range(BUNDLE_COUNT)]
    write_seconds = measure(lambda: store.put_many(bundles))
    experience_ids = [bundle.experience_id for bundle in bundles]
    read_seconds = measure(lambda: store.get_many(experience_ids))
    list_seconds = measure(lambda: store.list())
    return {
        "backend": name,
        "records": BUNDLE_COUNT,
        "write_seconds": round(write_seconds, 6),
        "read_seconds": round(read_seconds, 6),
        "list_seconds": round(list_seconds, 6),
    }


def main() -> None:
    """Run all backend benchmarks and print JSON results."""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        results = [
            run_backend("memory", InMemoryStore()),
            run_backend("sqlite", SQLiteMemoryStore(root / "memory.sqlite3")),
            run_backend("jsonl", JSONLMemoryStore(root / "memory.jsonl")),
        ]
    print(json.dumps({"results": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
