"""Lightweight recorder API overhead benchmark.

Run with:

    python benchmarks/benchmark_recorder.py
"""

from __future__ import annotations

import json
from time import perf_counter

from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore

ITERATIONS = 50


def base_state() -> dict[str, float]:
    return {"battery_level": 90.0}


def base_action() -> dict[str, str]:
    return {"action_type": "benchmark", "command": "noop"}


def base_metadata() -> dict[str, str]:
    return {"robot_id": "benchmark-robot", "environment": "benchmark"}


def measure(name: str, operation: object) -> dict[str, float | int | str]:
    start = perf_counter()
    callable_operation = operation
    for _ in range(ITERATIONS):
        callable_operation()  # type: ignore[operator]
    elapsed = perf_counter() - start
    return {
        "name": name,
        "iterations": ITERATIONS,
        "total_seconds": round(elapsed, 6),
        "seconds_per_operation": round(elapsed / ITERATIONS, 6),
    }


def main() -> None:
    manual_recorder = ExperienceRecorder(InMemoryStore())
    context_recorder = ExperienceRecorder(InMemoryStore())
    decorator_recorder = ExperienceRecorder(InMemoryStore())

    @decorator_recorder.record_function(
        state=base_state(),
        action=base_action(),
        metadata=base_metadata(),
    )
    def decorated_noop() -> None:
        return None

    results = [
        measure(
            "manual",
            lambda: manual_recorder.record(
                state=base_state(),
                action=base_action(),
                outcome={"success": True, "summary": "ok"},
                metadata=base_metadata(),
            ),
        ),
        measure(
            "context_manager",
            lambda: context_recorder.capture(
                state=base_state(),
                action=base_action(),
                metadata=base_metadata(),
            ).__enter__().__exit__(None, None, None),
        ),
        measure("decorator", decorated_noop),
    ]
    print(json.dumps({"results": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
