"""Replay-specific exceptions."""


class ReplayError(Exception):
    """Base exception for replay failures."""


class ReplayCallbackError(ReplayError):
    """Raised when a replay event callback fails."""


class ReplayInterrupted(ReplayError):
    """Raised by callbacks or engine policy to stop replay cleanly."""
