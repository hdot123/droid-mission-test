"""Duration parsing and formatting helpers (standard library only)."""

import re

_UNIT_SECONDS = {"d": 86400, "h": 3600, "m": 60, "s": 1}
_ORDER = ("d", "h", "m", "s")


def parse_duration(s):
    """Parse a duration string like ``"1h30m"`` into total seconds (int).

    Each unit (d, h, m, s) may appear at most once and must appear in
    descending order d, h, m, s. Raises ValueError on invalid format.
    """
    if not isinstance(s, str) or not s:
        raise ValueError("invalid duration: {!r}".format(s))

    tokens = re.findall(r"(\d+)([dhms])", s)
    if not tokens or "".join(n + u for n, u in tokens) != s:
        raise ValueError("invalid duration: {!r}".format(s))

    units = [u for _, u in tokens]
    if len(set(units)) != len(units):
        raise ValueError("duplicate unit in duration: {!r}".format(s))
    if any(_ORDER.index(units[i]) >= _ORDER.index(units[i + 1])
           for i in range(len(units) - 1)):
        raise ValueError("units out of order in duration: {!r}".format(s))

    return sum(int(n) * _UNIT_SECONDS[u] for n, u in tokens)


def format_duration(seconds):
    """Format a non-negative number of seconds as a duration string.

    Splits into d/h/m/s and omits zero-valued units; 0 returns ``"0s"``.
    Raises ValueError on negative input.
    """
    if not isinstance(seconds, (int, float)) or isinstance(seconds, bool):
        raise ValueError("invalid seconds: {!r}".format(seconds))
    if seconds < 0:
        raise ValueError("negative seconds: {!r}".format(seconds))

    total = int(seconds)
    if total == 0:
        return "0s"

    parts = []
    for unit in _ORDER:
        value, total = divmod(total, _UNIT_SECONDS[unit])
        if value:
            parts.append("{}{}".format(value, unit))
    return "".join(parts)
