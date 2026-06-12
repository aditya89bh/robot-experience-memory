"""High-level experience recording API."""

from collections.abc import Mapping
from typing import Any

from robot_experience_memory.identifiers import generate_experience_id
from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.store import ExperienceBundle, MemoryStore
from robot_experience_memory.timestamps import utc_now

ModelInput = Mapping[str, Any]


class ExperienceRecorder:
    """Record complete robot state-action-outcome episodes to a memory store."""

    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def record(
        self,
        *,
        state: StateSnapshot | ModelInput,
        action: ActionRecord | ModelInput,
        outcome: OutcomeRecord | ModelInput,
        metadata: Metadata | ModelInput,
        experience_id: str | None = None,
    ) -> ExperienceBundle:
        """Build, persist, and return a complete experience bundle."""
        state_record = self._coerce_state(state)
        action_record = self._coerce_action(action)
        outcome_record = self._coerce_outcome(outcome)
        metadata_record = self._coerce_metadata(metadata)
        experience = ExperienceRecord(
            experience_id=experience_id or generate_experience_id(),
            state_id=state_record.state_id,
            action_id=action_record.action_id,
            outcome_id=outcome_record.outcome_id,
            metadata_id=metadata_record.metadata_id,
        )
        bundle = ExperienceBundle(
            experience=experience,
            state=state_record,
            action=action_record,
            outcome=outcome_record,
            metadata=metadata_record,
            stored_at=utc_now(),
        )
        return self.store.put(bundle)

    def _coerce_state(self, state: StateSnapshot | ModelInput) -> StateSnapshot:
        if isinstance(state, StateSnapshot):
            return state
        data = dict(state)
        data.setdefault("state_id", generate_experience_id("state"))
        return StateSnapshot.model_validate(data)

    def _coerce_action(self, action: ActionRecord | ModelInput) -> ActionRecord:
        if isinstance(action, ActionRecord):
            return action
        data = dict(action)
        data.setdefault("action_id", generate_experience_id("action"))
        return ActionRecord.model_validate(data)

    def _coerce_outcome(self, outcome: OutcomeRecord | ModelInput) -> OutcomeRecord:
        if isinstance(outcome, OutcomeRecord):
            return outcome
        data = dict(outcome)
        data.setdefault("outcome_id", generate_experience_id("outcome"))
        return OutcomeRecord.model_validate(data)

    def _coerce_metadata(self, metadata: Metadata | ModelInput) -> Metadata:
        if isinstance(metadata, Metadata):
            return metadata
        data = dict(metadata)
        data.setdefault("metadata_id", generate_experience_id("metadata"))
        return Metadata.model_validate(data)
