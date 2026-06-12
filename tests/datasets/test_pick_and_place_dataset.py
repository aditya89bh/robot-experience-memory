import json
from pathlib import Path


def test_pick_and_place_dataset_models_pose_recovery() -> None:
    path = Path("datasets/industrial/pick_and_place.jsonl")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    action_types = [row["action_type"] for row in rows]

    assert len(rows) == 5
    assert "pose_uncertainty" in {row["error_code"] for row in rows}
    assert action_types.index("relocalize_part") > action_types.index("pick_part")
    assert rows[-1]["action_type"] == "place_part"
