"""Statistics/aggregation helpers for parsed log records.

Consumes duck-typed records exposing ``timestamp`` (datetime), ``level``
(one of DEBUG/INFO/WARN/ERROR) and ``message`` attributes. Does not import
the parser module.
"""

from datetime import datetime

LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")


def count_by_level(records):
    """Return a dict mapping each of the four levels to its record count.

    Every level in ``LEVELS`` appears in the result, including levels with
    zero records. Records whose level is not one of the four known levels
    are ignored.
    """
    counts = {level: 0 for level in LEVELS}
    for record in records:
        level = getattr(record, "level", None)
        if level in counts:
            counts[level] += 1
    return counts


def error_frequency(records, start, end):
    """Count ERROR records whose timestamp lies within ``[start, end]``.

    Boundaries are inclusive: a record timestamped exactly ``start`` or
    ``end`` is counted. Records outside the window, and non-ERROR records
    inside it, are not counted. Returns an int (the ERROR count for the
    window); divide by the window duration externally for a rate.
    """
    count = 0
    for record in records:
        if getattr(record, "level", None) != "ERROR":
            continue
        timestamp = getattr(record, "timestamp", None)
        if timestamp is None:
            continue
        if start <= timestamp <= end:
            count += 1
    return count


def error_rate(records, start, end):
    """Return ERROR records per hour within ``[start, end]``.

    Computes :func:`error_frequency` over the window and divides by the
    window's duration in hours. Returns 0.0 when the window has zero or
    negative duration (no time elapses, so no rate can be expressed).
    """
    window = end - start
    total_seconds = window.total_seconds()
    if total_seconds <= 0:
        return 0.0
    return error_frequency(records, start, end) / (total_seconds / 3600.0)


def top_messages(records, limit=10):
    """Return the ``limit`` most frequent messages as ``[(message, count)]``.

    Sorted by descending count; ties are broken by ascending message text
    so the order is deterministic. ``limit`` must be a non-negative int;
    a value of 0 (or a negative value) returns an empty list. Messages are
    compared exactly as stored on the records.
    """
    if limit <= 0:
        return []
    counts = {}
    for record in records:
        message = getattr(record, "message", None)
        counts[message] = counts.get(message, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ordered[:limit]
