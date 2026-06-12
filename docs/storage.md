# Storage Backends

Phase 2 adds a persistence layer for robot episodic memory. Stores operate on an
`ExperienceBundle`, which groups the normalized Phase 1 models into one logical
episode:

```text
ExperienceBundle
├── ExperienceRecord
├── StateSnapshot
├── ActionRecord
├── OutcomeRecord
└── Metadata
```

## MemoryStore Interface

Every backend implements `MemoryStore`:

- `put(bundle)`: append one complete experience bundle.
- `get(experience_id)`: retrieve one bundle or return `None`.
- `list(filters=None, pagination=None)`: list bundles in stable insertion order.
- `put_many(bundles)`: append a batch in input order.
- `get_many(experience_ids)`: retrieve bundles in input ID order, returning
  `None` for missing IDs.
- `query_by_robot_id(robot_id)`: convenience metadata query.
- `query_by_environment(environment)`: convenience metadata query.
- `query_by_tag(tag)`: convenience metadata query.
- `query_by_operator(operator)`: convenience metadata query.

## InMemoryStore

`InMemoryStore` keeps bundles in Python dictionaries and lists. It is fastest for
unit tests, prototypes, and short-lived agent runs, but data disappears when the
process exits.

Use it when:

- you are testing model or workflow behavior;
- you need a temporary scratch store;
- persistence is not required.

## SQLiteMemoryStore

`SQLiteMemoryStore` uses the standard-library `sqlite3` module. It creates
normalized tables automatically for experiences, states, actions, outcomes, and
metadata. Structured fields that do not map directly to columns are stored as
validated JSON text.

SQLite indexes are created for common query fields, including experience
references, robot ID, environment, operator, success, and action type.

Use it when:

- you need durable local storage;
- you want one portable database file;
- you expect repeated retrieval and filtering.

## JSONLMemoryStore

`JSONLMemoryStore` stores one complete `ExperienceBundle` per line. Writes are
append-only and easy to inspect with normal text tools. On initialization, the
backend builds an in-memory index for efficient reads during the process lifetime.

Use it when:

- you want a simple append log;
- easy diffing/export matters;
- write volume is modest and local-file portability matters.

## Append-only Behavior

Stores reject duplicate `experience_id` values with `DuplicateExperienceError`.
The historical `allow_overwrite` parameter is accepted for compatibility, but it
does not permit overwrites. This protects robot experience history from silent
mutation.

## Filtering

Use `ExperienceFilter` with `list()`:

```python
from robot_experience_memory.store import ExperienceFilter

failures = store.list(ExperienceFilter(success=False))
robot_memories = store.list(ExperienceFilter(robot_id="robot-a"))
recovery_events = store.list(ExperienceFilter(tag="recovery"))
```

Supported filters include:

- `experience_id`
- `state_id`, `action_id`, `outcome_id`, `metadata_id`
- `robot_id`
- `environment`
- `operator`
- `tag`
- `success`
- `action_type`
- `stored_after` / `stored_before`

## Pagination

Use `Pagination(limit=..., offset=...)` for stable offset pagination:

```python
from robot_experience_memory.store import Pagination

first_page = store.list(pagination=Pagination(limit=10, offset=0))
second_page = store.list(pagination=Pagination(limit=10, offset=10))
```

Negative offsets and non-positive limits are rejected by validation.

## Batch Operations

`put_many()` stores bundles in input order. SQLite performs batch insertion in a
single transaction so duplicate IDs do not leave partial writes. `get_many()`
preserves input order and returns `None` for missing IDs.

```python
store.put_many([bundle_a, bundle_b])
restored = store.get_many(["exp-b", "missing", "exp-a"])
```

## Backend Configuration

Use `StoreConfig` and `create_memory_store()` to select a backend:

```python
from robot_experience_memory.store import StoreConfig, create_memory_store

store = create_memory_store(StoreConfig(backend="sqlite", path="memory.sqlite3"))
```

Supported backends:

- `memory`
- `sqlite`
- `jsonl`

Durable backends require a path.

## Benchmarks

A lightweight deterministic benchmark is available:

```bash
python benchmarks/benchmark_backends.py
```

It writes, reads, and lists a small fixed set of bundles for the in-memory,
SQLite, and JSONL backends, then prints a JSON summary. It is intended for quick
local comparisons rather than rigorous performance analysis.
