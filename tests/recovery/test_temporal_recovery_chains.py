from datetime import timedelta

from robot_experience_memory.recovery import build_temporal_recovery_chain
from robot_experience_memory.timestamps import utc_now
from tests.store.factories import make_bundle


def test_temporal_recovery_chain_orders_related_experiences() -> None:
    start = utc_now()
    failed = make_bundle("exp-1", success=False, stored_at=start)
    retry = make_bundle("exp-2", success=False, stored_at=start + timedelta(seconds=5))
    fix = make_bundle(
        "exp-3",
        success=True,
        action_type="clear_obstacle",
        stored_at=start + timedelta(seconds=10),
    )
    unrelated = make_bundle(
        "exp-4", robot_id="other", stored_at=start + timedelta(seconds=1)
    )

    chain = build_temporal_recovery_chain(failed, [fix, unrelated, failed, retry])

    assert [step.experience_id for step in chain.steps] == ["exp-1", "exp-2", "exp-3"]
    assert chain.resolved is True
    assert chain.steps[-1].action_type == "clear_obstacle"
