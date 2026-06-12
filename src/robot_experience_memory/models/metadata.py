"""Context metadata model."""

from pydantic import Field, field_validator

from robot_experience_memory.models.base import MemoryModel


class Metadata(MemoryModel):
    """Contextual information associated with a robot experience."""


    metadata_id: str = Field(min_length=1)
    robot_id: str = Field(min_length=1)
    operator: str | None = Field(default=None, min_length=1)
    environment: str = Field(min_length=1)
    tags: tuple[str, ...] = Field(default_factory=tuple)
    notes: str | None = None

    @field_validator("robot_id", "environment")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            msg = "metadata text fields must be non-empty"
            raise ValueError(msg)
        return stripped

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        normalized = tuple(tag.strip() for tag in value if tag.strip())
        if len(set(normalized)) != len(normalized):
            msg = "tags must be unique"
            raise ValueError(msg)
        return normalized
