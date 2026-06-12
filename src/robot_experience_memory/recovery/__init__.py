"""Recovery intelligence APIs."""

from robot_experience_memory.recovery.clustering import OutcomeCluster, cluster_outcomes
from robot_experience_memory.recovery.engine import RecoveryEngine, RecoveryResult
from robot_experience_memory.recovery.errors import RecoveryError
from robot_experience_memory.recovery.patterns import (
    FailurePattern,
    detect_failure_patterns,
)
from robot_experience_memory.recovery.suggestions import (
    RecoverySuggestion,
    SuggestionType,
)

__all__ = [
    "FailurePattern",
    "RecoveryEngine",
    "RecoveryError",
    "RecoveryResult", "RecoverySuggestion", "SuggestionType",
    "detect_failure_patterns", "OutcomeCluster", "cluster_outcomes",
]
