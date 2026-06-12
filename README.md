# Robot Experience Memory

Stores robot state-action-outcome episodes for replay and recovery.

This repository provides the foundational data and storage layer for a robotic
episodic memory system.

## Minimal Storage Example

```python
from robot_experience_memory import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.store import (
    ExperienceBundle,
    ExperienceFilter,
    InMemoryStore,
)

bundle = ExperienceBundle(
    experience=ExperienceRecord(
        experience_id="exp-001",
        state_id="state-001",
        action_id="action-001",
        outcome_id="outcome-001",
        metadata_id="metadata-001",
    ),
    state=StateSnapshot(
        state_id="state-001",
        joint_positions={"shoulder": 1.2},
        battery_level=88.0,
    ),
    action=ActionRecord(
        action_id="action-001",
        action_type="navigate",
        command="move_to",
        parameters={"x": 1.0, "y": 2.0},
    ),
    outcome=OutcomeRecord(
        outcome_id="outcome-001",
        success=False,
        summary="Navigation blocked by obstacle",
        error_code="OBSTACLE_BLOCKED",
    ),
    metadata=Metadata(
        metadata_id="metadata-001",
        robot_id="robot-a",
        operator="aditya",
        environment="lab",
        tags=("navigation", "recovery"),
    ),
)

store = InMemoryStore()
store.put(bundle)

restored = store.get("exp-001")
failures = store.list(ExperienceFilter(success=False))
robot_memories = store.query_by_robot_id("robot-a")
```

See `docs/storage.md` for the full storage backend guide.
