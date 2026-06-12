"""Decorator support for recorder captures."""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def recording_decorator(
    function: Callable[P, R],
    *,
    recorder: object,
    state: object,
    action: object,
    metadata: object,
    re_raise: bool = True,
) -> Callable[P, R | None]:
    """Wrap a function and record success or failure through a recorder."""

    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            result = function(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            recorder.capture_exception(  # type: ignore[attr-defined]
                exc,
                state=state,
                action=action,
                metadata=metadata,
            )
            if re_raise:
                raise
            return None
        recorder.record(  # type: ignore[attr-defined]
            state=state,
            action=action,
            outcome={"success": True, "summary": f"{function.__name__} returned"},
            metadata=metadata,
        )
        return result

    return wrapper
