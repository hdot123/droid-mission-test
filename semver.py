"""Semantic version comparison (standard library only)."""


def _parse(version):
    if not isinstance(version, str):
        raise ValueError("version must be a string")
    if version == "":
        raise ValueError("empty version string")
    parts = version.split(".")
    if len(parts) > 3:
        raise ValueError("more than three segments: %r" % (version,))
    numbers = []
    for part in parts:
        if part == "" or not part.isdigit():
            raise ValueError("non-numeric segment in %r" % (version,))
        numbers.append(int(part))
    while len(numbers) < 3:
        numbers.append(0)
    return tuple(numbers)


def compare(a, b):
    """Compare two semantic version strings.

    Returns -1 if a < b, 0 if a == b, 1 if a > b.
    Segments may be omitted and are padded with 0.
    Raises ValueError for invalid formats.
    """
    left = _parse(a)
    right = _parse(b)
    if left < right:
        return -1
    if left > right:
        return 1
    return 0
