"""Retrieval evaluation metrics for deterministic test sets."""

from __future__ import annotations

from collections.abc import Iterable

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.retrieval.query import RetrievalResult


class RetrievalEvaluationMetrics(MemoryModel):
    """Precision/recall style metrics for one retrieval result."""

    relevant_ids: tuple[str, ...]
    retrieved_ids: tuple[str, ...]
    true_positives: int = Field(ge=0)
    precision_at_k: float = Field(ge=0.0, le=1.0)
    recall_at_k: float = Field(ge=0.0, le=1.0)


def evaluate_retrieval_result(
    result: RetrievalResult,
    relevant_experience_ids: Iterable[str],
) -> RetrievalEvaluationMetrics:
    """Evaluate retrieval output against known relevant experience IDs."""
    relevant = tuple(dict.fromkeys(relevant_experience_ids))
    retrieved = tuple(match.experience.experience_id for match in result.matches)
    relevant_set = set(relevant)
    true_positives = sum(
        1 for experience_id in retrieved if experience_id in relevant_set
    )
    precision = 0.0 if not retrieved else true_positives / len(retrieved)
    recall = 0.0 if not relevant else true_positives / len(relevant)
    return RetrievalEvaluationMetrics(
        relevant_ids=relevant,
        retrieved_ids=retrieved,
        true_positives=true_positives,
        precision_at_k=round(precision, 4),
        recall_at_k=round(recall, 4),
    )
