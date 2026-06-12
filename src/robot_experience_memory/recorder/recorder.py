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
from robot_experience_memory.recorder.sensor_refs import SensorReference
from robot_experience_memory.store import ExperienceBundle, MemoryStore
from robot_experience_memory.timestamps import utc_now

ModelInput = Mapping[str, Any]
SensorReferenceInput = SensorReference | Mapping[str, Any]


class ExperienceRecorder:
    """Record complete robot state-action-outcome episodes to a memory store."""

    def __init__(
        self,
        store: MemoryStore,
        *,
        default_environment: str = "unknown",
        default_operator: str | None = None,
    ) -> None:
        self.store = store
        self.default_environment = default_environment
        self.default_operator = default_operator

    def record(
        self,
        *,
        state: StateSnapshot | ModelInput,
        action: ActionRecord | ModelInput,
        outcome: OutcomeRecord | ModelInput,
        metadata: Metadata | ModelInput,
        experience_id: str | None = None,
        environment: str | None = None,
        operator: str | None = None,
        sensor_references: list[SensorReferenceInput] | None = None,
    ) -> ExperienceBundle:
        """Build, persist, and return a complete experience bundle."""
        recorded_start = utc_now()
        state_record = self._coerce_state(state)
        action_record = self._coerce_action(action)
        outcome_record = self._coerce_outcome(outcome)
        recorded_end = utc_now()
        outcome_record = self._with_outcome_metric(
            outcome_record, "recorded_start_timestamp", recorded_start.timestamp()
        )
        outcome_record = self._with_outcome_metric(
            outcome_record, "recorded_end_timestamp", recorded_end.timestamp()
        )
        duration_seconds = max(0.0, (recorded_end - recorded_start).total_seconds())
        outcome_record = self._with_outcome_metric(
            outcome_record, "duration_seconds", duration_seconds
        )
        references = self._coerce_sensor_references(sensor_references or [])
        if references:
            state_record = self._with_sensor_references(state_record, references)
            outcome_record = self._with_sensor_artifacts(outcome_record, references)
        metadata_record = self._coerce_metadata(
            metadata, environment=environment, operator=operator
        )
        metadata_record = self._with_status_tag(metadata_record, outcome_record.success)
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
            stored_at=recorded_end,
        )
        return self.store.put(bundle)

    def capture_exception(
        self,
        exception: BaseException,
        *,
        state: StateSnapshot | ModelInput,
        action: ActionRecord | ModelInput,
        metadata: Metadata | ModelInput,
        experience_id: str | None = None,
        environment: str | None = None,
        operator: str | None = None,
        sensor_references: list[SensorReferenceInput] | None = None,
    ) -> ExperienceBundle:
        """Record an exception as a failed robot experience."""
        exception_type = type(exception).__name__
        return self.record(
            state=state,
            action=action,
            outcome={
                "success": False,
                "summary": f"{exception_type}: {exception}",
                "error_code": f"exception.{exception_type}",
            },
            metadata=metadata,
            experience_id=experience_id,
            environment=environment,
            operator=operator,
            sensor_references=sensor_references,
        )

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

    def _coerce_metadata(
        self,
        metadata: Metadata | ModelInput,
        *,
        environment: str | None = None,
        operator: str | None = None,
    ) -> Metadata:
        if isinstance(metadata, Metadata):
            updates: dict[str, Any] = {}
            if environment is not None:
                updates["environment"] = environment
            if operator is not None:
                updates["operator"] = operator
            return metadata.model_copy(update=updates) if updates else metadata
        data = dict(metadata)
        data.setdefault("metadata_id", generate_experience_id("metadata"))
        data["environment"] = (
            environment or data.get("environment") or self.default_environment
        )
        selected_operator = operator or data.get("operator") or self.default_operator
        if selected_operator is not None:
            data["operator"] = selected_operator
        return Metadata.model_validate(data)

    def _with_outcome_metric(
        self, outcome: OutcomeRecord, key: str, value: float
    ) -> OutcomeRecord:
        metrics = dict(outcome.metrics)
        metrics[key] = value
        return outcome.model_copy(update={"metrics": metrics})

    def _with_status_tag(self, metadata: Metadata, success: bool) -> Metadata:
        status_tag = "success" if success else "failure"
        tags = tuple(dict.fromkeys((*metadata.tags, status_tag)))
        return metadata.model_copy(update={"tags": tags})

    def _coerce_sensor_references(
        self, references: list[SensorReferenceInput]
    ) -> list[SensorReference]:
        return [
            reference
            if isinstance(reference, SensorReference)
            else SensorReference.model_validate(dict(reference))
            for reference in references
        ]

    def _with_sensor_references(
        self, state: StateSnapshot, references: list[SensorReference]
    ) -> StateSnapshot:
        readings = dict(state.sensor_readings)
        readings["sensor_references"] = [
            reference.to_dict() for reference in references
        ]
        return state.model_copy(update={"sensor_readings": readings})

    def _with_sensor_artifacts(
        self, outcome: OutcomeRecord, references: list[SensorReference]
    ) -> OutcomeRecord:
        artifacts = [*outcome.artifacts, *(reference.uri for reference in references)]
        return outcome.model_copy(update={"artifacts": artifacts})
