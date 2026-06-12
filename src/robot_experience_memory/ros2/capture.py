"""Helpers for recording ROS-style action executions."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import Field

from robot_experience_memory.models.base import MemoryModel
from robot_experience_memory.recorder import ExperienceRecorder
from robot_experience_memory.store import ExperienceBundle


class ROS2ActionCapture(MemoryModel):
    """Reusable capture helper around an ExperienceRecorder."""

    action_type: str = Field(min_length=1)
    robot_id: str = Field(min_length=1)
    environment: str = Field(default="unknown", min_length=1)
    operator: str | None = None
    controller: str | None = None
    tags: tuple[str, ...] = Field(default_factory=lambda: ("ros2",))

    def record_execution(
        self,
        recorder: ExperienceRecorder,
        *,
        state: Mapping[str, Any],
        command: str,
        parameters: Mapping[str, Any] | None = None,
        success: bool = True,
        summary: str | None = None,
        error_code: str | None = None,
        experience_id: str | None = None,
    ) -> ExperienceBundle:
        """Record one ROS-style action execution."""
        return recorder.record(
            state=state,
            action={
                "action_type": self.action_type,
                "command": command,
                "parameters": dict(parameters or {}),
                "controller": self.controller,
            },
            outcome={
                "success": success,
                "summary": summary or ("completed" if success else "failed"),
                "error_code": error_code,
            },
            metadata={
                "robot_id": self.robot_id,
                "environment": self.environment,
                "operator": self.operator,
                "tags": self.tags,
            },
            experience_id=experience_id,
        )


def capture_action_execution(
    recorder: ExperienceRecorder,
    *,
    action_type: str,
    robot_id: str,
    state: Mapping[str, Any],
    command: str,
    environment: str = "unknown",
    operator: str | None = None,
    controller: str | None = None,
    parameters: Mapping[str, Any] | None = None,
    success: bool = True,
    summary: str | None = None,
    error_code: str | None = None,
    tags: tuple[str, ...] = ("ros2",),
    experience_id: str | None = None,
) -> ExperienceBundle:
    """Capture one ROS-style action execution with an ExperienceRecorder."""
    capture = ROS2ActionCapture(
        action_type=action_type,
        robot_id=robot_id,
        environment=environment,
        operator=operator,
        controller=controller,
        tags=tags,
    )
    return capture.record_execution(
        recorder,
        state=state,
        command=command,
        parameters=parameters,
        success=success,
        summary=summary,
        error_code=error_code,
        experience_id=experience_id,
    )
