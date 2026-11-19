"""Swatch Internet Time (.beats) conversions.

BMT (Biel Mean Time) is UTC + 1 hour. A day is divided into 1000 .beats,
so one .beat is 86.4 seconds. ``to_beats`` converts a UTC wall clock time
to .beats; ``from_beats`` converts .beats back to a UTC (hour, minute,
second) triple with the second component floored down.
"""

import math

__all__ = ["to_beats", "from_beats"]

_SECONDS_PER_BEAT = 86.4
_SECONDS_PER_HOUR = 3600
_SECONDS_PER_DAY = 86400
_BEATS_PER_DAY = 1000


def _require_int(name: str, value: object) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")


def to_beats(hour: int, minute: int, second: int) -> float:
    """Convert a UTC time of day to Swatch .beats (rounded to 2 decimals)."""
    _require_int("hour", hour)
    _require_int("minute", minute)
    _require_int("second", second)
    if not 0 <= hour <= 23:
        raise ValueError(f"hour must be in 0..23, got {hour}")
    if not 0 <= minute <= 59:
        raise ValueError(f"minute must be in 0..59, got {minute}")
    if not 0 <= second <= 59:
        raise ValueError(f"second must be in 0..59, got {second}")

    # BMT = UTC + 1 hour, measured as seconds since BMT midnight.
    bmt_seconds = ((hour + 1) % 24) * _SECONDS_PER_HOUR + minute * 60 + second
    return round(bmt_seconds / _SECONDS_PER_BEAT, 2)


def from_beats(beats: float) -> tuple[int, int, int]:
    """Convert Swatch .beats (0 <= beats < 1000) to UTC (hour, minute, second)."""
    if isinstance(beats, bool) or not isinstance(beats, (int, float)):
        raise TypeError(f"beats must be a number, got {type(beats).__name__}")
    if not 0 <= beats < _BEATS_PER_DAY:
        raise ValueError(f"beats must be in [0, 1000), got {beats}")

    # Seconds since UTC midnight; BMT midnight is 1 hour ahead of UTC.
    utc_seconds = (beats * _SECONDS_PER_BEAT - _SECONDS_PER_HOUR) % _SECONDS_PER_DAY
    # Round away float representation noise before flooring so that values
    # which are integral seconds do not fall one second short.
    total = math.floor(round(utc_seconds, 9)) % _SECONDS_PER_DAY

    hour, remainder = divmod(total, _SECONDS_PER_HOUR)
    minute, second = divmod(remainder, 60)
    return hour, minute, second
