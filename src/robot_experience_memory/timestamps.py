"""Timezone-aware UTC timestamp utilities."""

from datetime import UTC, datetime, timedelta, timezone


def utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""
    return datetime.now(UTC)


def ensure_utc(value: datetime) -> datetime:
    """Return a timezone-aware datetime normalized to UTC."""
    if value.tzinfo is None or value.utcoffset() is None:
        msg = "datetime must be timezone-aware"
        raise ValueError(msg)
    return value.astimezone(UTC)


def utc_timestamp() -> str:
    """Return the current UTC timestamp as an ISO 8601 string."""
    return utc_now().isoformat()


IST = timezone(timedelta(hours=5, minutes=30))
