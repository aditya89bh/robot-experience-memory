from robot_experience_memory.models.outcome import OutcomeRecord


def test_outcome_record_describes_result() -> None:
    outcome = OutcomeRecord(
        outcome_id="outcome-1",
        success=True,
        summary="Reached waypoint",
        metrics={"duration_seconds": 2.5},
        artifacts=["log://run-1"],
    )

    assert outcome.success is True
    assert outcome.metrics["duration_seconds"] == 2.5
