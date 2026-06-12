"""Recovery intelligence APIs."""

from robot_experience_memory.recovery.clustering import OutcomeCluster, cluster_outcomes
from robot_experience_memory.recovery.engine import RecoveryEngine, RecoveryResult
from robot_experience_memory.recovery.errors import RecoveryError
from robot_experience_memory.recovery.evaluation import (
    RecoveryEvaluationCase,
    RecoveryEvaluationMetrics,
    evaluate_recovery_cases,
)
from robot_experience_memory.recovery.patterns import (
    FailurePattern,
    detect_failure_patterns,
)
from robot_experience_memory.recovery.policies import RecoveryPolicy
from robot_experience_memory.recovery.strategies import (
    FallbackAction,
    find_fallback_action,
    score_confidence,
)
from robot_experience_memory.recovery.suggestions import (
    RecoverySuggestion,
    SuggestionType,
)
from robot_experience_memory.recovery.traces import RecoveryTrace

__all__ = [
    "FailurePattern",
    "FallbackAction",
    "OutcomeCluster",
    "RecoveryEngine",
    "RecoveryEvaluationCase",
    "RecoveryEvaluationMetrics",
    "RecoveryError",
    "RecoveryPolicy",
    "RecoveryResult",
    "RecoverySuggestion",
    "RecoveryTrace",
    "SuggestionType",
    "cluster_outcomes",
    "detect_failure_patterns",
    "evaluate_recovery_cases",
    "find_fallback_action",
    "score_confidence",
]
