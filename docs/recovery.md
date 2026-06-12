# Recovery Intelligence

Recovery intelligence analyzes stored robot experiences after a failure and returns a deterministic suggestion. It is intentionally rule-based for Phase 5: no ML, no LLMs, no robot control, and no heavy dependencies.

## What it does

Given a failed `ExperienceBundle`, `RecoveryEngine` inspects a `MemoryStore` and answers:

- what failed, via outcome/error/action context
- whether similar failures happened before
- whether the same action succeeded before
- whether an alternate action succeeded in the same context
- whether retry, fallback, or escalation is recommended
- how confident the recommendation is
- what evidence and rules produced the suggestion

## What it does not do

- It does not command or move a robot.
- It does not publish ROS messages.
- It does not learn from embeddings, models, or LLM calls.
- It does not replace operator judgment for safety-critical failures.

## Basic usage

```python
from robot_experience_memory.recovery import RecoveryEngine
from robot_experience_memory.store import InMemoryStore

store = InMemoryStore()
# Store ExperienceBundle records here.
engine = RecoveryEngine(store)
suggestion = engine.suggest_recovery(failed_experience)

print(suggestion.suggestion_type)
print(suggestion.rationale)
print(suggestion.confidence)
print(suggestion.trace)
```

## Policy tuning

`RecoveryPolicy` controls deterministic thresholds:

```python
from robot_experience_memory.recovery import RecoveryEngine, RecoveryPolicy

policy = RecoveryPolicy(
    max_retries=1,
    escalation_threshold=3,
    minimum_confidence=0.4,
)
engine = RecoveryEngine(store, policy=policy)
```

## Suggestions

- `retry`: failures are rare or the same robot/action has succeeded before.
- `fallback`: repeated failures exist and an alternate action succeeded in the same robot/environment context.
- `escalate`: retry budget is exhausted, repeated failures exceed threshold, or confidence is too low.

## Traces

Each suggestion can include a `RecoveryTrace` with matched experience IDs, rules fired, final rationale, and evidence counts. Traces are intended for debugging and operator-facing explanations.

## Evaluation

Phase 5 includes deterministic evaluation scenarios in `robot_experience_memory.recovery.evaluation`. The suite reports total cases, suggestion counts, average confidence, and expected-suggestion accuracy.

## Evaluation metrics

The evaluation suite exposes `evaluate_recovery_cases(...)`, returning:

- `total_cases`
- `suggested_retry`
- `suggested_fallback`
- `suggested_escalation`
- `average_confidence`
- `correct_expected_suggestion_rate`
