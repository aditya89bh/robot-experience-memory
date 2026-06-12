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

## Recorder Example

```python
from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import InMemoryStore

recorder = ExperienceRecorder(InMemoryStore(), default_environment="lab")
bundle = recorder.record(
    state={"battery_level": 90.0},
    action={"action_type": "navigate", "command": "move_to"},
    outcome={"success": True, "summary": "arrived"},
    metadata={"robot_id": "robot-a"},
)
```

See `docs/recorder.md` for manual, context manager, decorator, exception, hook,
and sensor-reference capture patterns.

## Replay Example

```python
from robot_experience_memory.replay import ReplayConfig, ReplayEngine

report = ReplayEngine(store, ReplayConfig(speed_multiplier=0.0)).replay()
print(report.total_experiences)
```

Replay is structured and inspectable; it does not control a physical robot. See
`docs/replay.md` for filtering, deterministic mode, callbacks, interruption, and
CLI usage.

## Recovery Intelligence

Phase 5 adds deterministic recovery suggestions for failed experiences. The recovery engine inspects stored `ExperienceBundle` records and recommends `retry`, `fallback`, or `escalate` without ML, LLMs, or robot control.

```python
from robot_experience_memory.recovery import RecoveryEngine

engine = RecoveryEngine(store)
suggestion = engine.suggest_recovery(failed_experience)
print(suggestion.suggestion_type, suggestion.confidence)
```

See [docs/recovery.md](docs/recovery.md) for policies, traces, examples, and evaluation notes.

