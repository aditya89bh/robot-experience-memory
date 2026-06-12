import json
from pathlib import Path

from robot_experience_memory.models.action import ActionRecord


def test_model_serializes_to_dict_and_json() -> None:
    action = ActionRecord(
        action_id="action-1",
        action_type="navigate",
        command="move_to",
        parameters={"x": 1.0},
    )

    assert action.to_dict()["action_id"] == "action-1"
    assert json.loads(action.to_json())["command"] == "move_to"


def test_model_serializes_to_file(tmp_path: Path) -> None:
    action = ActionRecord(action_id="action-1", action_type="stop", command="halt")

    path = action.to_file(tmp_path / "action.json")

    assert path.read_text(encoding="utf-8").strip().startswith("{")
