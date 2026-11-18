"""log_filter: filter parsed log records by level threshold and time window.

This module owns only the FILTERING capability of the log-analysis toolkit.
It does not import or edit the parsing, statistics, or formatting modules, and
it implements no CLI. Records are consumed duck-typed:

- each record carries a ``timestamp`` attribute holding a ``datetime.datetime``
  (if that attribute is absent, the ``datetime`` attribute is used instead),
- and a ``level`` attribute that is one of the four level names ``"DEBUG"``,
  ``"INFO"``, ``"WARN"``, ``"ERROR"`` (or this module's severity constants
  ``DEBUG``/``INFO``/``WARN``/``ERROR``).

``records`` may be any iterable sequence of such records (list, tuple, or
generator). Both public functions return a new list, preserve the relative
order of the input, and never modify the input.
"""

from datetime import datetime  # noqa: F401  (documents the expected timestamp type)

DEBUG = 0
INFO = 1
WARN = 2
ERROR = 3

_LEVEL_SEVERITY = {
    "DEBUG": DEBUG,
    "INFO": INFO,
    "WARN": WARN,
    "ERROR": ERROR,
}
_SEVERITY_LEVEL = {severity: name for name, severity in _LEVEL_SEVERITY.items()}


def _severity(level):
    """Normalize a level name or severity constant to its severity integer.

    Accepts exactly the four level-name strings (``"DEBUG"``, ``"INFO"``,
    ``"WARN"``, ``"ERROR"``) and the constants ``DEBUG``..``ERROR``. Raises
    ``ValueError`` for anything else.
    """
    if isinstance(level, str):
        if level in _LEVEL_SEVERITY:
            return _LEVEL_SEVERITY[level]
        raise ValueError("unknown level: %r" % (level,))
    if isinstance(level, int) and level in _SEVERITY_LEVEL:
        return level
    raise ValueError("unknown level: %r" % (level,))


def _timestamp(record):
    """Return the record's timestamp, trying ``timestamp`` then ``datetime``.

    Raises ``AttributeError`` when the record exposes neither attribute.
    """
    for name in ("timestamp", "datetime"):
        ts = getattr(record, name, None)
        if ts is not None:
            return ts
    raise AttributeError(
        "record has no 'timestamp' or 'datetime' attribute: %r" % (record,)
    )


def filter_by_level(records, min_level):
    """Keep only records whose level is ``min_level`` AND ABOVE.

    ``min_level`` may be a severity constant (``DEBUG``, ``INFO``, ``WARN``,
    ``ERROR``) or a level-name string (``"DEBUG"``, ``"INFO"``, ``"WARN"``,
    ``"ERROR"``). Severity orders levels as DEBUG < INFO < WARN < ERROR, so:

    - ``min_level=DEBUG`` keeps all four levels;
    - ``min_level=WARN`` keeps WARN and ERROR and drops INFO and DEBUG;
    - ``min_level=ERROR`` keeps only ERROR.

    Returns a new list with the input order preserved; the input ``records``
    is not modified. Raises ``ValueError`` if ``min_level`` or a record's
    level is not one of the four levels.

    Example::

        warnings_and_up = filter_by_level(records, WARN)
    """
    threshold = _severity(min_level)
    return [r for r in records if _severity(r.level) >= threshold]


def filter_by_time(records, start, end):
    """Keep only records whose timestamp lies in the closed interval
    ``[start, end]`` (both endpoints inclusive).

    ``start`` and ``end`` are ``datetime.datetime`` values compared directly
    against each record's timestamp; passing ``None`` for either side leaves
    that side unbounded (e.g. ``start=None`` keeps everything at or before
    ``end``). If ``start`` is later than ``end``, no record can satisfy both
    bounds and an empty list is returned.

    Returns a new list with the input order preserved; the input ``records``
    is not modified. Raises ``AttributeError`` if a record has neither a
    ``timestamp`` nor a ``datetime`` attribute.

    Example::

        during_incident = filter_by_time(records, t_begin, t_end)
    """
    result = []
    for record in records:
        ts = _timestamp(record)
        if start is not None and ts < start:
            continue
        if end is not None and ts > end:
            continue
        result.append(record)
    return result
