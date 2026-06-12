from robot_experience_memory.models.metadata import Metadata


def test_metadata_captures_context() -> None:
    metadata = Metadata(
        metadata_id="metadata-1",
        robot_id="robot-a",
        operator="aditya",
        environment="lab",
        tags=("recovery", "navigation"),
    )

    assert metadata.robot_id == "robot-a"
    assert metadata.tags == ("recovery", "navigation")
