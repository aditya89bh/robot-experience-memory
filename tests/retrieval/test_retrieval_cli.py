import json
from pathlib import Path

import pytest

from robot_experience_memory.retrieval.cli import main
from robot_experience_memory.store import JSONLMemoryStore
from tests.store.factories import make_bundle


def test_retrieval_cli_outputs_text_for_jsonl_store(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "memory.jsonl"
    store = JSONLMemoryStore(path)
    store.put(make_bundle("exp-1", action_type="navigate"))
    store.put(make_bundle("exp-2", action_type="dock"))

    exit_code = main(
        [
            "--backend",
            "jsonl",
            "--path",
            str(path),
            "--action-type",
            "navigate",
            "--top-k",
            "1",
        ]
    )

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "retrieved 1 matches" in output
    assert "exp-1" in output


def test_retrieval_cli_outputs_json_for_jsonl_store(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "memory.jsonl"
    store = JSONLMemoryStore(path)
    store.put(make_bundle("exp-1", robot_id="robot-a"))

    exit_code = main(
        [
            "--backend",
            "jsonl",
            "--path",
            str(path),
            "--robot-id",
            "robot-a",
            "--output",
            "json",
            "--no-cache",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["matches"][0]["experience_id"] == "exp-1"
    assert payload["matches"][0]["robot_id"] == "robot-a"


def test_retrieval_cli_rejects_success_and_failure(tmp_path: Path) -> None:
    path = tmp_path / "memory.jsonl"
    JSONLMemoryStore(path)

    with pytest.raises(SystemExit):
        main(
            [
                "--backend",
                "jsonl",
                "--path",
                str(path),
                "--success",
                "--failure",
            ]
        )
