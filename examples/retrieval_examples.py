"""Examples for deterministic similar-experience retrieval."""

from datetime import UTC, datetime

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.retrieval import (
    RetrievalEngine,
    RetrievalQuery,
    RetrievalWeights,
)
from robot_experience_memory.store import ExperienceBundle, InMemoryStore


def make_example_bundle(
    experience_id: str,
    *,
    action_type: str,
    robot_id: str = "robot-a",
    environment: str = "lab",
    tags: tuple[str, ...] = (),
    success: bool = True,
    stored_at: datetime | None = None,
) -> ExperienceBundle:
    """Build a small synthetic experience for examples."""
    suffix = experience_id.removeprefix("exp-")
    return ExperienceBundle(
        experience=ExperienceRecord(
            experience_id=experience_id,
            state_id=f"state-{suffix}",
            action_id=f"action-{suffix}",
            outcome_id=f"outcome-{suffix}",
            metadata_id=f"metadata-{suffix}",
        ),
        state=StateSnapshot(state_id=f"state-{suffix}"),
        action=ActionRecord(
            action_id=f"action-{suffix}",
            action_type=action_type,
            command=action_type,
        ),
        outcome=OutcomeRecord(
            outcome_id=f"outcome-{suffix}",
            success=success,
            summary="completed" if success else "failed",
        ),
        metadata=Metadata(
            metadata_id=f"metadata-{suffix}",
            robot_id=robot_id,
            environment=environment,
            tags=tags,
        ),
        stored_at=stored_at or datetime(2026, 1, 1, tzinfo=UTC),
    )


def build_store() -> InMemoryStore:
    """Create an in-memory store with deterministic example experiences."""
    store = InMemoryStore()
    store.put(
        make_example_bundle(
            "exp-1",
            action_type="navigate",
            tags=("navigation", "hallway"),
            stored_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
    )
    store.put(
        make_example_bundle(
            "exp-2",
            action_type="dock",
            tags=("charging", "dock"),
            stored_at=datetime(2026, 1, 2, tzinfo=UTC),
        )
    )
    store.put(
        make_example_bundle(
            "exp-3",
            action_type="navigate",
            robot_id="robot-b",
            tags=("navigation", "recovery"),
            success=False,
            stored_at=datetime(2026, 1, 3, tzinfo=UTC),
        )
    )
    return store


def main() -> None:
    """Run retrieval examples and print concise summaries."""
    store = build_store()

    exact = RetrievalEngine(store).retrieve(RetrievalQuery(action_type="navigate"))
    exact_ids = [m.experience.experience.experience_id for m in exact.matches]
    print("exact matching:", exact_ids)

    tag = RetrievalEngine(store).retrieve(RetrievalQuery(tags=("navigation",)))
    tag_scores = [(m.experience.experience.experience_id, m.score) for m in tag.matches]
    print("tag similarity:", tag_scores)

    weighted = RetrievalEngine(
        store,
        weights=RetrievalWeights(action=2.0, metadata=1.0, tags=3.0, temporal=0.5),
    ).retrieve(RetrievalQuery(action_type="navigate", tags=("recovery",)))
    weighted_scores = [
        (m.experience.experience.experience_id, m.score) for m in weighted.matches
    ]
    print("weighted retrieval:", weighted_scores)

    top_k = RetrievalEngine(store).retrieve(
        RetrievalQuery(tags=("navigation",), top_k=1)
    )
    top_k_ids = [m.experience.experience.experience_id for m in top_k.matches]
    print("top-k retrieval:", top_k_ids)

    first = weighted.matches[0]
    print("explanation:", first.explanation)


if __name__ == "__main__":
    main()
