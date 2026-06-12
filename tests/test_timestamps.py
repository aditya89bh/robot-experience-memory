from datetime import UTC, datetime, timedelta

import pytest

from robot_experience_memory.timestamps import IST, ensure_utc, utc_now, utc_timestamp


def test_utc_now_is_timezone_aware_utc() -> None:
    current = utc_now()

    assert current.tzinfo is UTC
    assert current.utcoffset() == timedelta(0)


def test_ensure_utc_rejects_naive_datetime() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        ensure_utc(datetime(2026, 1, 1))


def test_ensure_utc_normalizes_datetime() -> None:
    value = datetime(2026, 1, 1, tzinfo=IST)

    assert ensure_utc(value).tzinfo is UTC


def test_utc_timestamp_is_isoformatted() -> None:
    assert "+00:00" in utc_timestamp()
