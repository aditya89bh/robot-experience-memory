"""Deterministic retrieval scoring helpers."""

from robot_experience_memory.retrieval.query import RetrievalQuery
from robot_experience_memory.store import ExperienceBundle


def exact_match_score(query: RetrievalQuery, bundle: ExperienceBundle) -> float:
    """Score exact query fields against a bundle between 0.0 and 1.0."""
    checks: list[bool] = []
    if query.action_type is not None:
        checks.append(bundle.action.action_type == query.action_type)
    if query.robot_id is not None:
        checks.append(bundle.metadata.robot_id == query.robot_id)
    if query.environment is not None:
        checks.append(bundle.metadata.environment == query.environment)
    if query.success is not None:
        checks.append(bundle.outcome.success is query.success)
    if query.error_code is not None:
        checks.append(bundle.outcome.error_code == query.error_code)
    if not checks:
        return 0.0
    return sum(1 for check in checks if check) / len(checks)


def metadata_similarity_score(query: RetrievalQuery, bundle: ExperienceBundle) -> float:
    """Score robot, environment, and operator metadata similarity."""
    checks: list[bool] = []
    if query.robot_id is not None:
        checks.append(bundle.metadata.robot_id == query.robot_id)
    if query.environment is not None:
        checks.append(bundle.metadata.environment == query.environment)
    if query.operator is not None:
        checks.append(bundle.metadata.operator == query.operator)
    if not checks:
        return 0.0
    return sum(1 for check in checks if check) / len(checks)


def tag_similarity_score(query: RetrievalQuery, bundle: ExperienceBundle) -> float:
    """Score tag overlap using Jaccard similarity."""
    query_tags = set(query.tags)
    bundle_tags = set(bundle.metadata.tags)
    if not query_tags and not bundle_tags:
        return 0.0
    if not query_tags or not bundle_tags:
        return 0.0
    return len(query_tags & bundle_tags) / len(query_tags | bundle_tags)
