# Architecture Overview

`robot-experience-memory` starts with a foundational data layer for robotic
episodic memory. The first phase intentionally avoids storage engines, replay
planners, and retrieval algorithms. It focuses on stable records that can be
persisted, validated, serialized, and tested.

## Episode Shape

A robot experience is represented by an `ExperienceRecord`. It links four record
families by identifier:

```text
ExperienceRecord
├── state_id    -> StateSnapshot
├── action_id   -> ActionRecord
├── outcome_id  -> OutcomeRecord
└── metadata_id -> Metadata
```

This reference-based shape keeps the episode lightweight and allows future
storage backends to colocate or shard records without changing the public model
contracts.

## Model Responsibilities

- `StateSnapshot` captures the robot state before execution.
- `ActionRecord` captures what command was executed and with which parameters.
- `OutcomeRecord` captures whether execution succeeded and what evidence or
  metrics were produced.
- `Metadata` captures search and audit context such as robot, environment,
  operator, and tags.
- `ExperienceRecord` binds those records into one replayable episode.

## Serialization Boundary

Every model inherits shared helpers for JSON and dictionary serialization:

- `to_dict()`
- `to_json()`
- `to_file(path)`
- `from_dict(data)`
- `from_json(data)`
- `from_file(path)`

The helpers use Pydantic v2 validation on read, so malformed persisted records
fail at the boundary instead of leaking into replay or recovery logic.

## Time and Identity

Identifier utilities generate UUID-backed experience identifiers. Timestamp
utilities always use timezone-aware UTC datetimes. This keeps future data from
multiple robots and environments comparable across systems.

## Intentional Non-Goals for Phase 1

The following are deliberately left out:

- database adapters
- vector indexing
- replay execution
- recovery planning
- robot middleware integrations
- large binary artifact storage

Those features can be added once the core data contracts are stable.
