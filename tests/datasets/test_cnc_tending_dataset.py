import json
from pathlib import Path


def test_cnc_tending_dataset_contains_recovery_evidence() -> None:
    path = Path("datasets/industrial/cnc_tending.jsonl")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 5
    assert {row["environment"] for row in rows} == {"cnc-cell-a"}
    assert any(row["error_code"] == "gripper_slip" for row in rows)
    assert rows[-1]["success"] is True
