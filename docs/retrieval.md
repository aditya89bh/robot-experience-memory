# Similar Experience Retrieval

Phase 6 adds a deterministic retrieval layer for finding relevant past robot experiences from any `MemoryStore` backend.

Retrieval is intentionally simple and inspectable:

- no vector database
- no embeddings
- no LLM calls
- no heavy dependencies
- deterministic scoring and ordering

Use retrieval when you want to ask questions such as:

- Have we seen this robot state context before?
- Have we tried this action type before?
- Did similar experiences succeed or fail?
- Which previous experiences are most relevant?
- Why did the engine return these experiences?

## Basic usage

```python
from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery

engine = RetrievalEngine(store)
result = engine.retrieve(
    RetrievalQuery(
        action_type="navigate",
        robot_id="robot-a",
        environment="lab",
        tags=("navigation",),
        top_k=5,
    )
)

for match in result.matches:
    print(match.experience.experience.experience_id, match.score)
    print(match.explanation.reasons if match.explanation else ())
```

`RetrievalEngine` accepts any `MemoryStore`, including in-memory, JSONL, and SQLite stores.

## Exact matching

Exact matching supports:

- `action_type`
- `robot_id`
- `environment`
- `success`
- `error_code`

Exact scoring is deterministic and returns a value between `0.0` and `1.0` based on the requested exact fields that match the stored experience.

## Metadata similarity

Metadata similarity scores requested metadata fields independently:

- `robot_id`
- `environment`
- `operator`

Only fields present on the query contribute to the metadata score. This keeps a robot-only query from being penalized for not specifying environment or operator.

## Tag similarity

Tag similarity uses deterministic set overlap. The current implementation uses Jaccard similarity:

```text
intersection(query_tags, experience_tags) / union(query_tags, experience_tags)
```

If the query has no tags, tag similarity is `0.0`; empty tag queries should rely on other score components.

## Outcome similarity

Outcome matching supports:

- `success=True` / `success=False`
- `error_code="..."`

This lets callers ask whether similar attempted actions succeeded or failed.

## Temporal retrieval

Temporal scoring uses `ExperienceBundle.stored_at`.

When the temporal weight is enabled, more recent experiences score higher than older experiences. Recency is normalized across the candidate set for a query so the newest candidate receives the strongest temporal contribution.

## Weighting

`RetrievalWeights` controls the contribution of each component:

```python
from robot_experience_memory.retrieval import RetrievalWeights

weights = RetrievalWeights(
    action=2.0,
    metadata=1.0,
    tags=3.0,
    outcome=1.0,
    temporal=0.5,
)
engine = RetrievalEngine(store, weights=weights)
```

Weights must be non-negative, and at least one weight must be positive. Scores are normalized over active query components so a query that only specifies `action_type` can still produce a perfect `1.0` action match.

## Top-k retrieval

Set `top_k` on `RetrievalQuery` to limit results:

```python
result = engine.retrieve(RetrievalQuery(action_type="navigate", top_k=3))
```

`top_k` must be greater than zero.

## Ranking

Matches are ranked deterministically by:

1. score descending
2. `stored_at` descending
3. `experience_id` ascending

The tie-breakers make repeated retrieval calls stable even when scores are equal.

## Explanations

Each `RetrievalMatch` includes a `RetrievalExplanation` with:

- score components (`exact`, `metadata`, `tags`, `temporal`)
- human-readable reasons

Example reasons include:

- `action_type matched: navigate`
- `robot_id matched: robot-a`
- `environment matched: lab`
- `tags overlapped`
- `temporal recency contributed`

These explanations are designed for inspection and debugging, not natural-language planning.

## Caching

`RetrievalEngine` enables a small in-memory cache by default for repeated identical queries.

```python
engine = RetrievalEngine(store)
```

Disable it when inspecting a store that is mutating between calls:

```python
engine = RetrievalEngine(store, cache_enabled=False)
```

Cache keys are deterministic JSON representations of `RetrievalQuery`.

## CLI usage

Install the package and use:

```bash
robot-experience-retrieve \
  --backend jsonl \
  --path memory.jsonl \
  --action-type navigate \
  --robot-id robot-a \
  --environment lab \
  --tag navigation \
  --top-k 5
```

SQLite stores are supported with `--backend sqlite`.

Useful flags:

- `--backend jsonl|sqlite`
- `--path PATH`
- `--action-type VALUE`
- `--robot-id VALUE`
- `--environment VALUE`
- `--operator VALUE`
- `--tag VALUE` (repeatable)
- `--success` or `--failure`
- `--error-code VALUE`
- `--top-k N`
- `--no-cache`
- `--output text|json`

JSON output is useful for scripts:

```bash
robot-experience-retrieve --backend sqlite --path memory.db --failure --output json
```

## Benchmarks

Run the lightweight synthetic benchmark with:

```bash
python benchmarks/retrieval_benchmark.py --sizes 10 100 1000 --iterations 20
python benchmarks/retrieval_benchmark.py --json
```

The benchmark uses deterministic synthetic in-memory stores and reports average retrieval latency.

## Limitations

- Retrieval scans the store in memory; there is no index-aware query planner yet.
- Similarity is symbolic and deterministic; it does not understand semantic meaning.
- Tag similarity is simple set overlap.
- Temporal scoring is relative to the current candidate set, not absolute wall-clock age.
- Cache invalidation is manual: disable cache for stores that change between retrieval calls.
