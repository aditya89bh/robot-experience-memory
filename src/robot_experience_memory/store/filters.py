"""Filtering and pagination primitives for memory stores."""

from datetime import datetime

from pydantic import Field, field_validator, model_validator

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.store.bundle import ExperienceBundle
from robot_experience_memory.timestamps import ensure_utc


class ExperienceFilter(MemoryModel):
    """Optional criteria used to select stored robot experiences."""

    experience_id: str | None = None
    state_id: str | None = None
    action_id: str | None = None
    outcome_id: str | None = None
    metadata_id: str | None = None
    robot_id: str | None = None
    environment: str | None = None
    operator: str | None = None
    tag: str | None = None
    success: bool | None = None
    action_type: str | None = None
    stored_after: datetime | None = None
    stored_before: datetime | None = None

    @field_validator("stored_after", "stored_before")
    @classmethod
    def normalize_time(cls, value: datetime | None) -> datetime | None:
        """Normalize filter timestamps to timezone-aware UTC datetimes."""
        return ensure_utc(value) if value is not None else None

    @model_validator(mode="after")
    def validate_time_range(self) -> "ExperienceFilter":
        """Reject inverted time windows."""
        if (
            self.stored_after is not None
            and self.stored_before is not None
            and self.stored_after > self.stored_before
        ):
            msg = "stored_after must be before or equal to stored_before"
            raise ValueError(msg)
        return self

    def matches(self, bundle: ExperienceBundle) -> bool:
        """Return whether a bundle satisfies this filter."""
        checks = [
            self.experience_id is None
            or bundle.experience.experience_id == self.experience_id,
            self.state_id is None or bundle.experience.state_id == self.state_id,
            self.action_id is None or bundle.experience.action_id == self.action_id,
            self.outcome_id is None or bundle.experience.outcome_id == self.outcome_id,
            self.metadata_id is None
            or bundle.experience.metadata_id == self.metadata_id,
            self.robot_id is None or bundle.metadata.robot_id == self.robot_id,
            self.environment is None or bundle.metadata.environment == self.environment,
            self.operator is None or bundle.metadata.operator == self.operator,
            self.tag is None or self.tag in bundle.metadata.tags,
            self.success is None or bundle.outcome.success is self.success,
            self.action_type is None or bundle.action.action_type == self.action_type,
            self.stored_after is None or bundle.stored_at >= self.stored_after,
            self.stored_before is None or bundle.stored_at <= self.stored_before,
        ]
        return all(checks)


class Pagination(MemoryModel):
    """Offset/limit pagination with stable backend ordering."""

    limit: int | None = Field(default=None, gt=0)
    offset: int = Field(default=0, ge=0)

    def apply(self, bundles: list[ExperienceBundle]) -> list[ExperienceBundle]:
        """Apply pagination to an already ordered list of bundles."""
        start = self.offset
        stop = None if self.limit is None else start + self.limit
        return bundles[start:stop]
