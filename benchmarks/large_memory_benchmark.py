"""Deterministic large-memory benchmark helpers."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery
from robot_experience_memory.store import InMemoryStore
from tests.store.factories import make_bundle


@dataclass(frozen=True)
class BenchmarkResult:
    name: str
    records: int
    elapsed_seconds: float
    matches: int


def build_large_memory_store(records: int) -> InMemoryStore:
    """Build a synthetic memory store with varied robots/actions/tags."""
    store = InMemoryStore()
    for index in range(records):
        store.put(
            make_bundle(
                f"exp-{index}",
                robot_id=f"robot-{index % 8}",
                environment=f"cell-{index % 4}",
                action_type="pick" if index % 2 == 0 else "place",
                tag="cnc" if index % 3 == 0 else "assembly",
                success=index % 5 != 0,
            )
        )
    return store


def run_retrieval_benchmark(records: int = 1_000) -> BenchmarkResult:
    """Run a practical retrieval benchmark without external dependencies."""
    store = build_large_memory_store(records)
    engine = RetrievalEngine(store, cache_enabled=False)
    query = RetrievalQuery(robot_id="robot-2", action_type="pick", top_k=10)
    started = perf_counter()
    result = engine.retrieve(query)
    elapsed = perf_counter() - started
    return BenchmarkResult(
        name="symbolic_retrieval_large_memory",
        records=records,
        elapsed_seconds=elapsed,
        matches=len(result.matches),
    )


if __name__ == "__main__":
    print(run_retrieval_benchmark())
