from datetime import timedelta

from robot_experience_memory.recovery import find_fallback_action
from robot_experience_memory.timestamps import utc_now
from tests.store.factories import make_bundle


def test_causal_fallback_prefers_success_after_same_error_failure() -> None:
    start = utc_now()
    failed = make_bundle(
        "exp-1",
        success=False,
        action_type="pick",
        error_code="vacuum_drop",
        stored_at=start,
    )
    repeated = make_bundle(
        "exp-2",
        success=False,
        action_type="pick",
        error_code="vacuum_drop",
        stored_at=start + timedelta(seconds=1),
    )
    fallback = make_bundle(
        "exp-3",
        success=True,
        action_type="two_finger_grasp",
        stored_at=start + timedelta(seconds=2),
    )
    stale_success = make_bundle(
        "exp-4",
        success=True,
        action_type="nudge_part",
        stored_at=start - timedelta(seconds=10),
    )

    result = find_fallback_action(failed, [stale_success, repeated, fallback])

    assert result is not None
    assert result.action_type == "two_finger_grasp"
    assert result.causal_error_code == "vacuum_drop"
    assert result.experience_ids == ("exp-3",)
