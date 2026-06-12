# Experience Recorder

Phase 3 adds `ExperienceRecorder`, a high-level API for capturing robot
state-action-outcome episodes and persisting them to any `MemoryStore` backend.

## Manual Recording

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

## Timestamps and Duration

The recorder captures timezone-aware UTC start and end times. They are stored as
Unix timestamp metrics on `OutcomeRecord.metrics`:

- `recorded_start_timestamp`
- `recorded_end_timestamp`
- `duration_seconds`

## Success and Failure Tags

Recorder-created metadata receives deterministic status tags:

- `success` for successful outcomes
- `failure` for failed outcomes or captured exceptions

Frozen Pydantic models are copied with updates rather than mutated.

## Exception Capture

`capture_exception()` records an exception as `OutcomeRecord(success=False)` with
an error code such as `exception.ValueError`. Tracebacks are not stored by
default.

## Metadata Defaults

Recorder-level defaults can populate missing metadata:

```python
recorder = ExperienceRecorder(
    store,
    default_environment="warehouse",
    default_operator="teleop",
)
```

Per-record `environment=` and `operator=` values override defaults.

## Sensor References

Use `SensorReference` to attach external data without storing heavy blobs:

```python
from robot_experience_memory.recorder import SensorReference

SensorReference(name="front_camera", uri="file:///frames/001.jpg")
```

References are stored in `StateSnapshot.sensor_readings["sensor_references"]`, and
URIs are mirrored in `OutcomeRecord.artifacts`.

## Hooks

Optional hooks support integrations:

- `before_record_hooks` receive `RecordContext` before persistence.
- `after_record_hooks` receive the stored `ExperienceBundle`.

Hook failures raise `RecorderHookError` so integrations fail loudly.

## Context Manager API

```python
with recorder.capture(
    state={},
    action={"action_type": "grasp", "command": "close_gripper"},
    metadata={"robot_id": "robot-a"},
):
    run_robot_action()
```

Normal exit records success. Exceptions record failure and are re-raised by
default.

## Decorator API

```python
@recorder.record_function(
    state={},
    action={"action_type": "compute", "command": "plan"},
    metadata={"robot_id": "robot-a"},
)
def plan() -> str:
    return "ready"
```

Successful returns record success. Raised exceptions record failure and are
re-raised by default.

## Recorder Benchmark

A lightweight recorder benchmark is available:

```bash
python benchmarks/benchmark_recorder.py
```

It uses `InMemoryStore` and compares manual recording, context manager capture,
and decorator capture. Results are printed as JSON.
