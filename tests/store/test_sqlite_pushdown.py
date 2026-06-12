from pathlib import Path

from robot_experience_memory.store import ExperienceFilter, SQLiteMemoryStore
from tests.store.factories import make_bundle


def test_sqlite_list_pushes_exact_filters_into_query(tmp_path: Path) -> None:
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite")
    store.put_many(
        [
            make_bundle("exp-1", robot_id="r1", action_type="pick", tag="cnc"),
            make_bundle("exp-2", robot_id="r1", action_type="place", tag="cnc"),
            make_bundle("exp-3", robot_id="r2", action_type="pick", tag="weld"),
        ]
    )

    selected = store.list(
        ExperienceFilter(robot_id="r1", action_type="pick", tag="cnc")
    )

    assert [bundle.experience_id for bundle in selected] == ["exp-1"]


def test_sqlite_filter_sql_uses_parameters(tmp_path: Path) -> None:
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite")

    sql, parameters = store._select_with_filters(  # noqa: SLF001
        ExperienceFilter(robot_id="robot' OR 1=1 --", success=False)
    )

    assert "?" in sql
    assert "robot' OR 1=1 --" in parameters
    assert "outcomes.success = ?" in sql
