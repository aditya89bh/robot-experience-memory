from benchmarks.recovery_benchmark import run_benchmark
from robot_experience_memory.models import OutcomeRecord
from robot_experience_memory.recovery import (
    RecoveryEngine,
    RecoveryPolicy,
    RecoverySuggestion,
    cluster_outcomes,
    detect_failure_patterns,
)
from robot_experience_memory.store import ExperienceBundle, InMemoryStore
from tests.store.factories import make_bundle


def with_error(bundle: ExperienceBundle, error_code: str) -> ExperienceBundle:
    return bundle.model_copy(
        update={
            "outcome": OutcomeRecord(
                outcome_id=bundle.outcome.outcome_id,
                success=False,
                summary="failed",
                error_code=error_code,
            )
        }
    )


def test_recovery_engine_answers_core_questions() -> None:
    store = InMemoryStore()
    failure = with_error(make_bundle("exp-1", success=False), "blocked")
    prior_failure = with_error(make_bundle("exp-2", success=False), "blocked")
    fallback_success = make_bundle("exp-3", success=True, action_type="reroute")
    for bundle in (failure, prior_failure, fallback_success):
        store.put(bundle)

    suggestion = RecoveryEngine(store).suggest_recovery(failure)

    assert isinstance(suggestion, RecoverySuggestion)
    assert suggestion.suggestion_type == "fallback"
    assert "alternate action" in suggestion.rationale
    assert suggestion.confidence > 0
    assert set(suggestion.related_experience_ids) == {"exp-1", "exp-2", "exp-3"}
    assert suggestion.trace is not None
    assert "fallback_success" in suggestion.trace.rules_fired


def test_patterns_and_clusters_share_deterministic_evidence() -> None:
    bundles = [
        with_error(make_bundle("exp-1", success=False), "blocked"),
        with_error(make_bundle("exp-2", success=False), "blocked"),
        make_bundle("exp-3", success=True, action_type="reroute"),
    ]

    patterns = detect_failure_patterns(bundles, min_count=2)
    clusters = cluster_outcomes(bundles)

    assert patterns[0].count == 2
    assert any(cluster.count == 2 and not cluster.success for cluster in clusters)
    assert clusters == cluster_outcomes(reversed(bundles))


def test_policy_trace_and_benchmark_integration() -> None:
    store = InMemoryStore()
    failure = make_bundle("exp-1", success=False)
    store.put(failure)

    suggestion = RecoveryEngine(
        store, policy=RecoveryPolicy(minimum_confidence=0.99)
    ).suggest_recovery(failure)
    benchmark = run_benchmark(size=10, iterations=3)

    assert suggestion.suggestion_type == "escalate"
    assert suggestion.trace is not None
    assert suggestion.trace.final_rationale == suggestion.rationale
    assert benchmark["store_size"] == 10
    assert benchmark["iterations"] == 3
    average_ms = benchmark["average_ms"]
    assert isinstance(average_ms, int | float)
    assert average_ms >= 0
