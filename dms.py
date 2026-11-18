"""Decimal degrees and degrees/minutes/seconds (DMS) conversion."""

from __future__ import annotations

__all__ = ["from_dms", "to_dms"]

_SECONDS_DECIMALS = 6


def to_dms(deg: float) -> tuple[int, int, float]:
    """Convert decimal degrees ``deg`` to ``(degrees, minutes, seconds)``.

    The sign lives only in the degrees component (south latitude / west
    longitude are negative degrees); minutes and seconds are always
    non-negative.  Seconds carry at most six decimal places, rounded to that
    precision, and rounding may carry into minutes and degrees.
    """
    sign = -1 if deg < 0 else 1
    magnitude = abs(deg)
    degrees = int(magnitude)
    minutes_float = (magnitude - degrees) * 60.0
    minutes = int(minutes_float)
    seconds = round((minutes_float - minutes) * 60.0, _SECONDS_DECIMALS)
    if seconds >= 60.0:
        seconds = 0.0
        minutes += 1
    if minutes >= 60:
        minutes -= 60
        degrees += 1
    return (sign * degrees, minutes, seconds)


def from_dms(d: int, m: int, s: float) -> float:
    """Recombine ``(degrees, minutes, seconds)`` into decimal degrees.

    ``m`` must be in ``[0, 59]`` and ``s`` in ``[0, 60)``; ``s == 60.0`` is
    accepted as the carry spelling of ``m + 1``.  Anything else raises
    ``ValueError``.

    The magnitudes are summed first and the sign of ``d`` is applied to the
    total, so ``from_dms(-118, 14, 37.32)`` is exactly ``-118.2437``
    (signing only ``d`` inside ``d + m/60 + s/3600`` would give
    ``-117.7563``).
    """
    if not 0 <= m <= 59:
        raise ValueError(f"minutes must be in [0, 59], got {m}")
    if not 0 <= s <= 60:
        raise ValueError(f"seconds must be in [0, 60), got {s}")
    magnitude = abs(d) + m / 60 + s / 3600
    return -magnitude if d < 0 else magnitude
