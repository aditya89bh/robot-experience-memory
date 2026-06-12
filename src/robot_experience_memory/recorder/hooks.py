"""Recorder hook types."""

from collections.abc import Callable
from dataclasses import dataclass

from robot_experience_memory.store import ExperienceBundle


@dataclass(frozen=True)
class RecordContext:
    """Context passed to recorder hooks before persistence."""

    bundle: ExperienceBundle


BeforeRecordHook = Callable[[RecordContext], None]
AfterRecordHook = Callable[[ExperienceBundle], None]
