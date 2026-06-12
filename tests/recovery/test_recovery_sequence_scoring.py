from datetime import timedelta

from robot_experience_memory.recovery import (
    build_temporal_recovery_chain,
    score_recovery_sequence,
)
from robot_experience_memory.timestamps import utc_now
from tests.store.factories import make_bundle


def test_recovery_sequence_scoring_rewards_fast_resolution() -> None:
    start = utc_now()
    failed = make_bundle("exp-1", success=False, stored_at=start)
    success = make_bundle("exp-2", success=True, stored_at=start + timedelta(seconds=1))
    chain = build_temporal_recovery_chain(failed, [failed, success])

    score = score_recovery_sequence(chain)

    assert score.resolved is True
    assert score.score == 1.0
    assert score.successful_step_index == 1


def test_recovery_sequence_scoring_penalizes_unresolved_chain() -> None:
    failed = make_bundle("exp-1", success=False)
    chain = build_temporal_recovery_chain(failed, [failed])

    score = score_recovery_sequence(chain)

    assert score.resolved is False
    assert score.score == 0.1
