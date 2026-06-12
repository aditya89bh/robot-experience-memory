"""End-to-end industrial validation demo.

Loads synthetic industrial datasets, retrieves a failed episode, builds a temporal
recovery chain, scores the chain, and asks the deterministic recovery engine for a
suggestion. No ROS2, ML, embeddings, or external services are required.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.recovery import (
    RecoveryEngine,
    build_temporal_recovery_chain,
    score_recovery_sequence,
)
from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery
from robot_experience_memory.store import ExperienceBundle, InMemoryStore
from robot_experience_memory.timestamps import utc_now


class IndustrialDatasetRow(TypedDict):
    experience_id: str
    robot_id: str
    environment: str
    action_type: str
    success: bool
    error_code: str | None
    tags: list[str]
    summary: str


class IndustrialDemoResult(TypedDict):
    retrieved: list[str]
    suggestion: str
    sequence_resolved: bool
    sequence_score: float


DATASET_DIR = Path(__file__).resolve().parents[1] / "datasets" / "industrial"


def bundle_from_dataset_row(row: IndustrialDatasetRow) -> ExperienceBundle:
    """Convert one industrial JSONL row into a typed experience bundle."""
    experience_id = str(row["experience_id"])
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id=experience_id,
            state_id=f"state-{experience_id}",
            action_id=f"action-{experience_id}",
            outcome_id=f"outcome-{experience_id}",
            metadata_id=f"metadata-{experience_id}",
        ),
        state=StateSnapshot(state_id=f"state-{experience_id}"),
        action=ActionRecord(
            action_id=f"action-{experience_id}",
            action_type=row["action_type"],
            command=row["action_type"],
        ),
        outcome=OutcomeRecord(
            outcome_id=f"outcome-{experience_id}",
            success=row["success"],
            summary=row["summary"],
            error_code=row["error_code"],
        ),
        metadata=Metadata(
            metadata_id=f"metadata-{experience_id}",
            robot_id=row["robot_id"],
            environment=row["environment"],
            tags=tuple(row["tags"]),
        ),
        stored_at=utc_now().replace(microsecond=0),
    )


def load_industrial_store(dataset_dir: Path = DATASET_DIR) -> InMemoryStore:
    """Load all industrial validation datasets into an in-memory store."""
    store = InMemoryStore()
    rows: list[IndustrialDatasetRow] = []
    for path in sorted(dataset_dir.glob("*.jsonl")):
        rows.extend(
            cast(IndustrialDatasetRow, json.loads(line))
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    for row in rows:
        store.put(bundle_from_dataset_row(row))
    return store


def run_demo() -> IndustrialDemoResult:
    """Run retrieval, recovery suggestion, and sequence scoring together."""
    store = load_industrial_store()
    failed = store.get("cnc-003")
    if failed is None:
        msg = "expected cnc-003 failure in dataset"
        raise RuntimeError(msg)
    retrieval = RetrievalEngine(store).retrieve(
        RetrievalQuery(robot_id="cnc-tender-1", environment="cnc-cell-a", top_k=3)
    )
    suggestion = RecoveryEngine(store, max_retries=1).suggest_recovery(failed)
    chain = build_temporal_recovery_chain(failed, store.list())
    sequence_score = score_recovery_sequence(chain)
    return {
        "retrieved": [match.experience.experience_id for match in retrieval.matches],
        "suggestion": suggestion.suggestion_type,
        "sequence_resolved": sequence_score.resolved,
        "sequence_score": sequence_score.score,
    }


if __name__ == "__main__":
    print(run_demo())
