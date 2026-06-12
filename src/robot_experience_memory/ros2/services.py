"""Duck-typed service helpers for ROS2 integrations."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from robot_experience_memory.recovery import RecoveryEngine, RecoverySuggestion
from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalQuery,
    RetrievalResult,
)

RequestParser = Callable[[Any], Mapping[str, Any]]
ResponseBuilder = Callable[[Mapping[str, Any]], Any]


def handle_retrieval_request(
    request: Any,
    *,
    engine: RetrievalEngine,
    parse_request: RequestParser,
    build_response: ResponseBuilder,
) -> Any:
    """Handle a retrieval service request without depending on ROS2 types."""
    payload = parse_request(request)
    query = RetrievalQuery.model_validate(payload.get("query", payload))
    result = engine.retrieve(query)
    return build_response(retrieval_result_to_payload(result))


def handle_recovery_request(
    request: Any,
    *,
    engine: RecoveryEngine,
    parse_request: RequestParser,
    build_response: ResponseBuilder,
) -> Any:
    """Handle a recovery service request without depending on ROS2 types."""
    payload = parse_request(request)
    experience_id = str(payload["experience_id"])
    failed_experience = engine.store.get(experience_id)
    if failed_experience is None:
        raise KeyError(experience_id)
    suggestion = engine.suggest_recovery(failed_experience)
    return build_response(recovery_service_payload(suggestion))


def retrieval_result_to_payload(result: RetrievalResult) -> dict[str, Any]:
    """Convert RetrievalResult to a JSON-safe service payload."""
    return {
        "query": result.query.model_dump(mode="json"),
        "matches": [
            {
                "experience_id": match.experience.experience.experience_id,
                "score": match.score,
                "explanation": match.explanation.to_dict()
                if hasattr(match.explanation, "to_dict")
                else match.explanation,
            }
            for match in result.matches
        ],
        "total_matches": len(result.matches),
    }


def recovery_service_payload(suggestion: RecoverySuggestion) -> dict[str, Any]:
    """Convert RecoverySuggestion to a JSON-safe service payload."""
    return {
        "suggestion_type": suggestion.suggestion_type,
        "rationale": suggestion.rationale,
        "confidence": suggestion.confidence,
        "related_experience_ids": list(suggestion.related_experience_ids),
    }
