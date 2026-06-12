# Model Reference

Phase 1 defines a small, typed data layer for robotic episodic memory. All models
are immutable Pydantic v2 models. Unknown fields are rejected so persisted records
stay predictable.

## ExperienceRecord

Represents the top-level episode reference.

Fields:

- `experience_id`: Stable identifier for the episode.
- `state_id`: Identifier of the pre-execution `StateSnapshot`.
- `action_id`: Identifier of the executed `ActionRecord`.
- `outcome_id`: Identifier of the resulting `OutcomeRecord`.
- `metadata_id`: Identifier of contextual `Metadata`.

Example:

```python
from robot_experience_memory import ExperienceRecord

experience = ExperienceRecord(
    experience_id="exp-001",
    state_id="state-001",
    action_id="action-001",
    outcome_id="outcome-001",
    metadata_id="metadata-001",
)
```

## StateSnapshot

Captures robot state immediately before execution.

Fields:

- `state_id`: Stable identifier for the state record.
- `joint_positions`: Mapping of joint names to numeric positions.
- `pose`: Optional mapping of pose component names to numeric values.
- `sensor_readings`: Lightweight sensor values or references to larger artifacts.
- `battery_level`: Optional percentage from `0.0` to `100.0`.

Example:

```python
from robot_experience_memory import StateSnapshot

state = StateSnapshot(
    state_id="state-001",
    joint_positions={"shoulder": 1.2},
    pose={"x": 1.0, "y": 2.0, "theta": 0.5},
    sensor_readings={"camera_frame": "frame-42"},
    battery_level=84.0,
)
```

## ActionRecord

Describes an action executed by the robot.

Fields:

- `action_id`: Stable identifier for the action record.
- `action_type`: High-level category such as `navigate`, `grasp`, or `recover`.
- `command`: Concrete command issued to the control layer.
- `parameters`: Command parameters.
- `controller`: Optional controller or subsystem name.

Example:

```python
from robot_experience_memory import ActionRecord

action = ActionRecord(
    action_id="action-001",
    action_type="navigate",
    command="move_to",
    parameters={"x": 1.0, "y": 2.0},
    controller="nav-stack",
)
```

## OutcomeRecord

Describes the result after execution.

Fields:

- `outcome_id`: Stable identifier for the outcome record.
- `success`: Whether execution succeeded.
- `summary`: Human-readable result summary.
- `error_code`: Optional failure or recovery code.
- `metrics`: Numeric execution metrics such as duration or confidence.
- `artifacts`: References to logs, images, traces, or other external artifacts.

Example:

```python
from robot_experience_memory import OutcomeRecord

outcome = OutcomeRecord(
    outcome_id="outcome-001",
    success=True,
    summary="Reached waypoint",
    metrics={"duration_seconds": 3.4},
    artifacts=["log://run-001"],
)
```

## Metadata

Stores contextual information for search, grouping, and auditability.

Fields:

- `metadata_id`: Stable identifier for the metadata record.
- `robot_id`: Robot that produced the episode.
- `operator`: Optional human or process supervising execution.
- `environment`: Environment name such as `lab`, `warehouse`, or `field`.
- `tags`: Unique labels for filtering and retrieval.
- `notes`: Optional free-form context.

Example:

```python
from robot_experience_memory import Metadata

metadata = Metadata(
    metadata_id="metadata-001",
    robot_id="robot-a",
    operator="aditya",
    environment="lab",
    tags=("navigation", "recovery"),
)
```
