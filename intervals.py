"""Closed-interval merging utilities (standard library only)."""


def _validate(interval):
    try:
        start, end = interval
    except (TypeError, ValueError):
        raise ValueError("interval must be a [start, end] pair")
    if start > end:
        raise ValueError("interval start must be <= end: %r" % (interval,))
    return start, end


def merge(intervals):
    """Merge overlapping or endpoint-sharing closed intervals.

    Sorts by start ascending (ties by end ascending), then merges when the
    next interval's start is <= the current merged interval's end.
    Returns a list of [start, end] lists, non-overlapping and ascending.
    Raises ValueError if any interval has start > end. Empty input -> [].
    """
    validated = [_validate(interval) for interval in intervals]
    if not validated:
        return []
    validated.sort(key=lambda pair: (pair[0], pair[1]))
    merged = [list(validated[0])]
    for start, end in validated[1:]:
        if start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1][1] = end
        else:
            merged.append([start, end])
    return merged


def total_length(intervals):
    """Sum of end - start over the merged intervals."""
    return sum(end - start for start, end in merge(intervals))
