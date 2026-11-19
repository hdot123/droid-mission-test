"""Gas Mark oven temperature lookup (mark -> Celsius -> Fahrenheit).

Standard library only; no imports from other project modules.
"""

# Pinned lookup table, in table order (mark -> Celsius -> Fahrenheit).
_TABLE = (
    ("1/4", 110, 225),
    ("1/2", 120, 250),
    ("1", 140, 275),
    ("2", 150, 300),
    ("3", 165, 325),
    ("4", 180, 350),
    ("5", 190, 375),
    ("6", 200, 400),
    ("7", 220, 425),
    ("8", 230, 450),
    ("9", 240, 475),
)

_VALID_MARKS = frozenset(mark for mark, _, _ in _TABLE)


def _normalize_mark(mark):
    """Validate a mark parameter and return its table string form."""
    if isinstance(mark, bool):
        raise TypeError("mark must be int 1-9 or str, not bool")
    if isinstance(mark, int):
        if 1 <= mark <= 9:
            return str(mark)
        raise ValueError(f"invalid gas mark: {mark!r}")
    if isinstance(mark, str):
        if mark in _VALID_MARKS:
            return mark
        raise ValueError(f"invalid gas mark: {mark!r}")
    raise TypeError("mark must be int 1-9 or str")


def gasmark_to_celsius(mark) -> int:
    """Return the Celsius temperature for a gas mark."""
    key = _normalize_mark(mark)
    for m, c, _ in _TABLE:
        if m == key:
            return c
    raise ValueError(f"invalid gas mark: {mark!r}")


def gasmark_to_fahrenheit(mark) -> int:
    """Return the Fahrenheit temperature for a gas mark."""
    key = _normalize_mark(mark)
    for m, _, f in _TABLE:
        if m == key:
            return f
    raise ValueError(f"invalid gas mark: {mark!r}")


def celsius_to_gasmark(c) -> str:
    """Return the gas mark whose Celsius value is closest to c.

    On a tie, the lower (earlier in table order) mark wins.
    """
    if isinstance(c, bool) or not isinstance(c, (int, float)):
        raise TypeError("c must be a number (int or float)")
    best_mark = _TABLE[0][0]
    best_diff = abs(_TABLE[0][1] - c)
    for mark, deg, _ in _TABLE[1:]:
        diff = abs(deg - c)
        if diff < best_diff:  # strictly smaller keeps the earlier mark on ties
            best_diff = diff
            best_mark = mark
    return best_mark
