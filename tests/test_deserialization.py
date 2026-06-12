from pathlib import Path

from robot_experience_memory.models.action import ActionRecord


def test_model_deserializes_from_dict_and_json() -> None:
    action = ActionRecord.from_dict(
        {"action_id": "action-1", "action_type": "navigate", "command": "move_to"}
    )

    restored = ActionRecord.from_json(action.to_json())

    assert restored == action


def test_model_deserializes_from_file(tmp_path: Path) -> None:
    path = tmp_path / "action.json"
    path.write_text(
        '{"action_id":"action-1","action_type":"stop","command":"halt"}',
        encoding="utf-8",
    )

    action = ActionRecord.from_file(path)

    assert action.command == "halt"
