"""Integer interval complement within a closed range [lo, hi]."""


def complement(ranges: list[tuple[int, int]], lo: int, hi: int) -> list[tuple[int, int]]:
    """Return closed intervals in [lo, hi] not covered by any input interval.

    Input ranges may overlap and may be unordered, and may extend outside
    [lo, hi]. The result is sorted ascending by start, non-overlapping and
    non-adjacent (adjacent gaps are merged).

    Raises ValueError if lo > hi or if any interval has start > end.
    """
    if lo > hi:
        raise ValueError("lo must be <= hi")
    for start, end in ranges:
        if start > end:
            raise ValueError("interval start must be <= end")

    # Clamp and merge covered intervals.
    covered = []
    for start, end in ranges:
        s = max(start, lo)
        e = min(end, hi)
        if s <= e:
            covered.append((s, e))
    covered.sort()

    result = []
    cursor = lo
    for s, e in covered:
        if s > cursor:
            result.append((cursor, s - 1))
        cursor = max(cursor, e + 1)
    if cursor <= hi:
        result.append((cursor, hi))
    return result
