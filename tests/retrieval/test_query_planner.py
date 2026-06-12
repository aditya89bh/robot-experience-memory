from robot_experience_memory.retrieval import RetrievalQuery, plan_retrieval_query


def test_query_planner_creates_exact_pushdown_filters() -> None:
    query = RetrievalQuery(
        action_type="pick",
        robot_id="arm-1",
        environment="cell-a",
        success=True,
        tags=("cnc", "door"),
        error_code="GRIPPER_SLIP",
    )

    plan = plan_retrieval_query(query)

    assert plan.has_pushdown
    assert plan.filters is not None
    assert plan.filters.action_type == "pick"
    assert plan.filters.robot_id == "arm-1"
    assert plan.filters.environment == "cell-a"
    assert plan.filters.success is True
    assert plan.filters.tag == "cnc"
    assert "tags" in plan.residual_fields
    assert "error_code" in plan.residual_fields


def test_query_planner_handles_score_only_query() -> None:
    plan = plan_retrieval_query(RetrievalQuery())

    assert not plan.has_pushdown
    assert plan.filters is None
    assert plan.pushdown_fields == ()
