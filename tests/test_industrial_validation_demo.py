from examples.industrial_validation_demo import run_demo


def test_industrial_validation_demo_runs_end_to_end() -> None:
    result = run_demo()

    assert "cnc-003" in result["retrieved"]
    assert result["suggestion"] in {"retry", "fallback", "escalate"}
    assert result["sequence_resolved"] is True
