import json

from robot_experience_memory.replay.cli import main
from robot_experience_memory.store import JSONLMemoryStore, SQLiteMemoryStore
from tests.store.factories import make_bundle


def test_replay_cli_outputs_json_for_jsonl_store(tmp_path, capsys) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "experiences.jsonl"
    store = JSONLMemoryStore(path)
    store.put(make_bundle("exp-1", robot_id="robot-a"))
    store.put(make_bundle("exp-2", robot_id="robot-b", success=False))

    exit_code = main(
        [
            "--backend",
            "jsonl",
            "--path",
            str(path),
            "--robot-id",
            "robot-b",
            "--failure",
            "--deterministic",
            "--output",
            "json",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["total_experiences"] == 1
    assert output["failure_count"] == 1


def test_replay_cli_outputs_text_for_sqlite_store(tmp_path, capsys) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "experiences.sqlite"
    store = SQLiteMemoryStore(path)
    store.put(make_bundle("exp-1"))

    exit_code = main(
        [
            "--backend",
            "sqlite",
            "--path",
            str(path),
            "--deterministic",
            "--output",
            "text",
        ]
    )

    assert exit_code == 0
    assert "replayed 1 experiences" in capsys.readouterr().out
