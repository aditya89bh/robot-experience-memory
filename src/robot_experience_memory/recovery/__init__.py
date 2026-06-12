"""Recovery intelligence APIs."""

from robot_experience_memory.recovery.clustering import OutcomeCluster, cluster_outcomes
from robot_experience_memory.recovery.engine import RecoveryEngine, RecoveryResult
from robot_experience_memory.recovery.errors import RecoveryError
from robot_experience_memory.recovery.patterns import (
    FailurePattern,
    detect_failure_patterns,
)
from robot_experience_memory.recovery.strategies import (
    FallbackAction,
    find_fallback_action,
)
from robot_experience_memory.recovery.suggestions import (
    RecoverySuggestion,
    SuggestionType,
)

__all__ = [
    "FailurePattern",
    "FallbackAction",
    "OutcomeCluster",
    "RecoveryEngine",
    "RecoveryError",
    "RecoveryResult",
    "RecoverySuggestion",
    "SuggestionType",
    "cluster_outcomes",
    "detect_failure_patterns",
    "find_fallback_action",
]
