"""Recorder-specific exceptions."""


class RecorderError(Exception):
    """Base exception for recorder failures."""


class RecorderHookError(RecorderError):
    """Raised when a recorder hook fails."""
