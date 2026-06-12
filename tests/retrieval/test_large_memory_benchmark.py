from benchmarks.large_memory_benchmark import (
    build_large_memory_store,
    run_retrieval_benchmark,
)


def test_large_memory_benchmark_builds_varied_dataset() -> None:
    store = build_large_memory_store(40)

    assert len(store.list()) == 40
    assert store.list()[0].metadata.robot_id == "robot-0"


def test_large_memory_benchmark_reports_matches() -> None:
    result = run_retrieval_benchmark(80)

    assert result.name == "symbolic_retrieval_large_memory"
    assert result.records == 80
    assert result.matches <= 10
