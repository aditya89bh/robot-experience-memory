# Replay Workflows

Phase 4 adds a generic replay layer for stored robot experience memories.

## What replay is

Replay turns stored `ExperienceBundle` records into structured replay events that
can be inspected, filtered, serialized, tested, and used by future tooling.

## What replay is not

Replay does **not** physically control a robot yet. It does not publish ROS2
messages, command actuators, or perform real-world playback. Those integrations
belong in a later phase.

## ReplayEngine

`ReplayEngine` accepts any `MemoryStore` and replays matching bundles in stable
store order:

```python
from robot_experience_memory.replay import ReplayConfig, ReplayEngine

report = ReplayEngine(store, ReplayConfig(speed_multiplier=0.0)).replay()
```

## ReplayConfig

`ReplayConfig` controls replay behavior:

- `speed_multiplier`: controls delay between experiences; `0.0` means instant.
- `deterministic`: disables sleeping and uses stable timestamps.
- `include_state_events`: emits `state_observed` events.
- `include_action_events`: emits `action_replayed` events.
- `include_outcome_events`: emits `outcome_observed` events.
- `stop_on_failure`: interrupts replay after a failed outcome.

## ReplayEvent

Replay emits generic events, not framework-specific robot commands:

- `replay_started`
- `experience_started`
- `state_observed`
- `action_replayed`
- `outcome_observed`
- `experience_completed`
- `replay_completed`
- `replay_interrupted`

`ReplayEvent.to_visualization_dict()` returns JSON-safe fields for a future UI,
including event type, experience ID, robot ID, action type, success, timestamp,
and summary.

## ReplayReport

`ReplayEngine.replay()` returns `ReplayReport` with timing, totals, success and
failure counts, interruption status, emitted events, and aggregate statistics.

## Filtering

Replay reuses store-layer filters and pagination:

```python
from robot_experience_memory.store import ExperienceFilter, Pagination

report = engine.replay(
    filters=ExperienceFilter(robot_id="robot-a", success=True),
    pagination=Pagination(limit=10),
)
```

## Speed controls

Use `speed_multiplier=0.0` for instant replay in tests. Positive values sleep
between experiences using `1 / speed_multiplier` seconds.

## Deterministic mode

`deterministic=True` avoids sleeping and uses stable timestamps so tests and
serialized outputs are reproducible.

## Callbacks

Callbacks receive each `ReplayEvent`:

```python
def on_event(event):
    print(event.event_type)

ReplayEngine(store, callbacks=[on_event]).replay()
```

Callback failures raise `ReplayCallbackError`. A callback can raise
`ReplayInterrupted` to stop replay cleanly.

## Interruption

Replay can stop early when `stop_on_failure=True` or when a callback raises
`ReplayInterrupted`. The returned report is marked `interrupted=True` and includes
`interruption_reason`.

## CLI usage

The package installs `robot-experience-replay`:

```bash
robot-experience-replay --backend jsonl --path experiences.jsonl --output json
robot-experience-replay --backend sqlite --path memory.sqlite --failure --deterministic
```

Useful flags include `--robot-id`, `--environment`, `--action-type`, `--success`,
`--failure`, `--limit`, `--offset`, and `--output json|text`.
