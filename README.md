# Robot Experience Memory

Stores robot state-action-outcome episodes for replay and recovery.

This repository is intentionally minimal for now. It provides the initial Python project structure for future robot experience memory work.

## Minimal Storage Example

```python
from robot_experience_memory.store import InMemoryStore

store = InMemoryStore()
# Build an ExperienceBundle from ExperienceRecord, StateSnapshot, ActionRecord,
# OutcomeRecord, and Metadata, then persist it as one logical episode.
# store.put(bundle)
# restored = store.get(bundle.experience_id)
```

See `docs/storage.md` for the full storage overview.
