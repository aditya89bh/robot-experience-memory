"""Identifier utilities for robot experiences."""

from uuid import UUID, uuid4

EXPERIENCE_ID_PREFIX = "exp"


def generate_experience_uuid() -> UUID:
    """Generate a random UUID for an experience."""
    return uuid4()


def generate_experience_id(prefix: str = EXPERIENCE_ID_PREFIX) -> str:
    """Generate a stable string identifier for an experience."""
    normalized_prefix = prefix.strip()
    if not normalized_prefix:
        msg = "experience id prefix must be non-empty"
        raise ValueError(msg)
    return f"{normalized_prefix}_{generate_experience_uuid()}"
