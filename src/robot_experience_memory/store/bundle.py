"""Complete stored experience bundle."""

from datetime import datetime

from pydantic import Field, model_validator

from robot_experience_memory.models import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
)
from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.timestamps import utc_now


class ExperienceBundle(MemoryModel):
    """A complete robot experience stored and retrieved as one logical episode."""

    experience: ExperienceRecord
    state: StateSnapshot
    action: ActionRecord
    outcome: OutcomeRecord
    metadata: Metadata
    stored_at: datetime = Field(default_factory=utc_now)

    @property
    def experience_id(self) -> str:
        """Return the stable identifier of the bundled experience."""
        return self.experience.experience_id

    @model_validator(mode="after")
    def validate_references(self) -> "ExperienceBundle":
        """Ensure normalized records match the references in ExperienceRecord."""
        mismatches = {
            "state_id": (self.experience.state_id, self.state.state_id),
            "action_id": (self.experience.action_id, self.action.action_id),
            "outcome_id": (self.experience.outcome_id, self.outcome.outcome_id),
            "metadata_id": (self.experience.metadata_id, self.metadata.metadata_id),
        }
        invalid = [
            name
            for name, (expected, actual) in mismatches.items()
            if expected != actual
        ]
        if invalid:
            joined = ", ".join(invalid)
            msg = f"experience references do not match bundled records: {joined}"
            raise ValueError(msg)
        return self
