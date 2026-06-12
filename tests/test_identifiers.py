from uuid import UUID

import pytest

from robot_experience_memory.identifiers import (
    generate_experience_id,
    generate_experience_uuid,
)


def test_generate_experience_uuid_returns_uuid() -> None:
    assert isinstance(generate_experience_uuid(), UUID)


def test_generate_experience_id_uses_prefix() -> None:
    experience_id = generate_experience_id("robot-exp")

    assert experience_id.startswith("robot-exp_")
    UUID(experience_id.removeprefix("robot-exp_"))


def test_generate_experience_id_rejects_empty_prefix() -> None:
    with pytest.raises(ValueError, match="prefix"):
        generate_experience_id(" ")
