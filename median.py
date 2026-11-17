"""Median helper using the lower-median rule (no averaging for even counts)."""


def median(nums):
    """Return the median of a numeric list.

    The list is sorted ascending. For an odd number of elements the middle
    element is returned; for an even number of elements the smaller of the
    two middle values is returned (they are not averaged).
    """
    if not nums:
        raise ValueError("median() arg is an empty sequence")
    ordered = sorted(nums)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return ordered[mid - 1]
