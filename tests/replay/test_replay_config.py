import pytest
from pydantic import ValidationError

from robot_experience_memory.replay import ReplayConfig


def test_replay_config_defaults() -> None:
    config = ReplayConfig()

    assert config.speed_multiplier == 1.0
    assert config.deterministic is False
    assert config.include_state_events is True
    assert config.include_action_events is True
    assert config.include_outcome_events is True
    assert config.stop_on_failure is False


def test_replay_config_rejects_negative_speed() -> None:
    with pytest.raises(ValidationError):
        ReplayConfig(speed_multiplier=-1.0)
