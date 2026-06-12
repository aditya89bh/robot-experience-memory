from robot_experience_memory import (
    ActionRecord,
    ExperienceRecord,
    Metadata,
    OutcomeRecord,
    StateSnapshot,
    generate_experience_id,
    utc_now,
)


def test_public_api_exports_core_models_and_utilities() -> None:
    assert ActionRecord.__name__ == "ActionRecord"
    assert ExperienceRecord.__name__ == "ExperienceRecord"
    assert Metadata.__name__ == "Metadata"
    assert OutcomeRecord.__name__ == "OutcomeRecord"
    assert StateSnapshot.__name__ == "StateSnapshot"
    assert generate_experience_id().startswith("exp_")
    assert utc_now().tzinfo is not None
