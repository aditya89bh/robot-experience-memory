"""Recovery trace models."""

from typing import Any

from robot_experience_memory.models.base import MemoryModel


class RecoveryTrace(MemoryModel):
    """Evidence and rule trace used to make a recovery suggestion."""

    matched_experience_ids: tuple[str, ...]
    rules_fired: tuple[str, ...]
    final_rationale: str
    evidence: dict[str, Any]
