"""Gregorian calendar dates <-> ISO week dates (ISO 8601)."""

from datetime import date, timedelta

__all__ = ["to_iso_week", "from_iso_week"]


def _require_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int, got {type(value).__name__}")


def to_iso_week(y: int, m: int, d: int) -> tuple:
    """Convert a Gregorian calendar date to (iso_year, iso_week, iso_weekday).

    iso_weekday runs 1-7 with Monday as 1.
    Raises ValueError for an invalid date, TypeError for non-int inputs.
    """
    _require_int(y, "y")
    _require_int(m, "m")
    _require_int(d, "d")
    if not 1 <= y <= 9999:
        raise ValueError(f"invalid date: year {y} out of range")
    try:
        day = date(y, m, d)
    except ValueError as exc:
        raise ValueError(f"invalid date: {y}-{m}-{d}") from exc
    iso_year, iso_week, iso_weekday = day.isocalendar()
    return (int(iso_year), int(iso_week), int(iso_weekday))


def from_iso_week(iso_year: int, iso_week: int, iso_weekday: int) -> tuple:
    """Convert an ISO week date to a Gregorian (year, month, day).

    Raises ValueError when the ISO week does not exist in that year
    (e.g. week 53 of a 52-week year) or when iso_weekday is outside 1-7,
    and TypeError for non-int inputs.
    """
    _require_int(iso_year, "iso_year")
    _require_int(iso_week, "iso_week")
    _require_int(iso_weekday, "iso_weekday")
    if not 1 <= iso_year <= 9999:
        raise ValueError(f"invalid ISO week date: year {iso_year} out of range")
    if not 1 <= iso_weekday <= 7:
        raise ValueError(f"iso_weekday must be in 1..7, got {iso_weekday}")
    if not 1 <= iso_week <= 53:
        raise ValueError(f"iso_week must be in 1..53, got {iso_week}")
    # ISO week 1 is the week containing January 4th; its Monday starts week 1.
    jan4 = date(iso_year, 1, 4)
    week1_monday = jan4 - timedelta(days=jan4.weekday())
    try:
        candidate = week1_monday + timedelta(weeks=iso_week - 1, days=iso_weekday - 1)
    except (OverflowError, OSError) as exc:
        raise ValueError("invalid ISO week date") from exc
    cand_year, cand_week, _ = candidate.isocalendar()
    if cand_year != iso_year or cand_week != iso_week:
        raise ValueError(f"ISO week {iso_week} does not exist in year {iso_year}")
    return (candidate.year, candidate.month, candidate.day)
