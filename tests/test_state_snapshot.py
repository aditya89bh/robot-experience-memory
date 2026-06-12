from robot_experience_memory.models.state import StateSnapshot


def test_state_snapshot_captures_robot_state() -> None:
    state = StateSnapshot(
        state_id="state-1",
        joint_positions={"shoulder": 1.0},
        pose={"x": 0.0, "y": 1.0, "theta": 3.14},
        sensor_readings={"camera_frame": "frame-001"},
        battery_level=87.5,
    )

    assert state.joint_positions["shoulder"] == 1.0
    assert state.battery_level == 87.5
