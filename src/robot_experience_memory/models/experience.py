"""Experience record model."""

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel


class ExperienceRecord(MemoryModel):
    """A robot experience linking state, action, outcome, and metadata records."""


    experience_id: str = Field(min_length=1)
    state_id: str = Field(min_length=1)
    action_id: str = Field(min_length=1)
    outcome_id: str = Field(min_length=1)
    metadata_id: str = Field(min_length=1)
