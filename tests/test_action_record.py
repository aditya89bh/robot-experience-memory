from robot_experience_memory.models.action import ActionRecord


def test_action_record_describes_execution_command() -> None:
    action = ActionRecord(
        action_id="action-1",
        action_type="navigate",
        command="move_to",
        parameters={"x": 1.0, "y": 2.0},
        controller="nav-stack",
    )

    assert action.action_type == "navigate"
    assert action.parameters["x"] == 1.0
