"""Context manager support for recorder captures."""

from collections.abc import Mapping
from types import TracebackType
from typing import Any

from robot_experience_memory.models import ActionRecord, Metadata, StateSnapshot
from robot_experience_memory.store import ExperienceBundle

ModelInput = Mapping[str, Any]


class RecordingContext:
    """Context manager that records a robot action block."""

    def __init__(
        self,
        recorder: Any,
        *,
        state: StateSnapshot | ModelInput,
        action: ActionRecord | ModelInput,
        metadata: Metadata | ModelInput,
        success_summary: str = "completed",
        re_raise: bool = True,
    ) -> None:
        self.recorder = recorder
        self.state = state
        self.action = action
        self.metadata = metadata
        self.success_summary = success_summary
        self.re_raise = re_raise
        self.bundle: ExperienceBundle | None = None

    def __enter__(self) -> "RecordingContext":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        _ = traceback
        if exc is None:
            self.bundle = self.recorder.record(
                state=self.state,
                action=self.action,
                outcome={"success": True, "summary": self.success_summary},
                metadata=self.metadata,
            )
            return False
        self.bundle = self.recorder.capture_exception(
            exc,
            state=self.state,
            action=self.action,
            metadata=self.metadata,
        )
        return not self.re_raise
