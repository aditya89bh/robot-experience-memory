from robot_experience_memory.models.experience import ExperienceRecord


def test_experience_record_links_references() -> None:
    record = ExperienceRecord(
        experience_id="exp-1",
        state_id="state-1",
        action_id="action-1",
        outcome_id="outcome-1",
        metadata_id="metadata-1",
    )

    assert record.experience_id == "exp-1"
    assert record.state_id == "state-1"
