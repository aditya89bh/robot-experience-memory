# Storage Layer

Phase 2 adds a persistence layer for robot episodic memory. Storage works with a
complete `ExperienceBundle`, which groups the normalized Phase 1 records into one
logical episode:

```text
ExperienceBundle
├── ExperienceRecord
├── StateSnapshot
├── ActionRecord
├── OutcomeRecord
└── Metadata
```

## Backends

Three backends are available:

- `InMemoryStore`: process-local storage for tests and prototypes.
- `JSONLMemoryStore`: append-oriented JSON Lines storage for portable files.
- `SQLiteMemoryStore`: durable local SQLite storage using the Python standard
  library.

All backends implement `MemoryStore` and support:

- `put(bundle)`
- `get(experience_id)`
- `list(filters=None, pagination=None)`
- `put_many(bundles)`
- `get_many(experience_ids)`

Duplicate experience IDs raise `DuplicateExperienceError` unless
`allow_overwrite=True` is passed explicitly.

## Filtering

Use `ExperienceFilter` to filter by:

- `experience_id`
- `state_id`, `action_id`, `outcome_id`, `metadata_id`
- `robot_id`
- `environment`
- `tag`
- `success`
- `action_type`
- `stored_after` / `stored_before`

## Pagination

Use `Pagination(limit=..., offset=...)` for stable offset pagination. Backends
return records in stable insertion order.

## Configuration

`StoreConfig` and `create_memory_store` provide a small factory for selecting a
backend:

```python
from robot_experience_memory.store import StoreConfig, create_memory_store

store = create_memory_store(StoreConfig(backend="sqlite", path="memory.sqlite3"))
```
