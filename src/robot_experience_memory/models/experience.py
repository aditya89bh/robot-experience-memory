"""Experience record model."""

from pydantic import BaseModel, ConfigDict, Field


class ExperienceRecord(BaseModel):
    """A robot experience linking state, action, outcome, and metadata records."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    experience_id: str = Field(min_length=1)
    state_id: str = Field(min_length=1)
    action_id: str = Field(min_length=1)
    outcome_id: str = Field(min_length=1)
    metadata_id: str = Field(min_length=1)
