from robot_experience_memory.store import (
    DuplicateExperienceError,
    ExperienceNotFoundError,
)


def test_duplicate_error_includes_experience_id() -> None:
    error = DuplicateExperienceError("exp-1")

    assert error.experience_id == "exp-1"
    assert "exp-1" in str(error)


def test_not_found_error_includes_experience_id() -> None:
    error = ExperienceNotFoundError("exp-missing")

    assert error.experience_id == "exp-missing"
    assert "exp-missing" in str(error)
