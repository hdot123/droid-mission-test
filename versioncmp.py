"""Compare dot-separated numeric version strings."""


def compare(a: str, b: str) -> int:
    """Compare two dot-separated numeric version strings.

    Returns -1 if a < b, 0 if equal, 1 if a > b. Segments are compared
    numerically, with the shorter side padded with zeros. Raises ValueError
    if any segment is non-numeric.
    """
    seg_a = a.split(".")
    seg_b = b.split(".")
    try:
        nums_a = [int(s) for s in seg_a]
        nums_b = [int(s) for s in seg_b]
    except ValueError:
        raise ValueError(f"non-numeric version segment in {a!r} or {b!r}") from None
    length = max(len(nums_a), len(nums_b))
    nums_a += [0] * (length - len(nums_a))
    nums_b += [0] * (length - len(nums_b))
    if nums_a < nums_b:
        return -1
    if nums_a > nums_b:
        return 1
    return 0
