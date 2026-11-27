"""Burrows-Wheeler Transform (BWT).

Block rotation permutation (not compression, not run-length coding):
``bwt_encode`` sorts all cyclic rotations of the input string and returns
the last column plus the row of the original string; ``bwt_decode`` inverts
it with the standard LF-mapping iteration.

Standard library only; no imports from sibling modules.
"""

__all__ = ["bwt_encode", "bwt_decode"]


def _require_str(value, name):
    if not isinstance(value, str):
        raise TypeError(f"{name} must be str, got {type(value).__name__}")


def bwt_encode(s: str) -> tuple[str, int]:
    """Return ``(last_column, primary_index)`` for the BWT of ``s``.

    All ``n`` cyclic rotations of ``s`` are sorted ascending by
    ``(rotation_string, original_offset)``.  When rotation strings are equal
    (periodic strings), the smaller original offset sorts first -- the
    tie-break is explicit and never left to sort stability.

    Raises:
        TypeError: ``s`` is not a ``str``.
        ValueError: ``s`` is empty.
    """
    _require_str(s, "s")
    n = len(s)
    if n == 0:
        raise ValueError("cannot encode an empty string")
    # Explicit (rotation, offset) key pins the tie-break rule.
    order = sorted(((s[i:] + s[:i], i) for i in range(n)), key=lambda p: (p[0], p[1]))
    last_col = "".join(rot[-1] for rot, _ in order)
    index = next(i for i, (_, off) in enumerate(order) if off == 0)
    return last_col, index


def bwt_decode(last_col: str, index: int) -> str:
    """Invert the BWT: recover the original string from its last column.

    Args:
        last_col: last column produced by :func:`bwt_encode`.
        index: row of the original string (primary index).

    Raises:
        TypeError: ``last_col`` is not a ``str``, or ``index`` is not an
            ``int`` (``bool`` counts as non-int).
        ValueError: ``last_col`` is empty, or ``index`` is out of range
            (``< 0`` or ``>= len(last_col)``).
    """
    _require_str(last_col, "last_col")
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError(f"index must be int, got {type(index).__name__}")
    n = len(last_col)
    if n == 0:
        raise ValueError("cannot decode an empty last column")
    if index < 0 or index >= n:
        raise ValueError(f"index {index} out of range for length {n}")
    # LF-mapping: start from the primary row, repeatedly prepend the column
    # character and jump to the row where that character ranks next.
    total = {c: last_col.count(c) for c in set(last_col)}
    starts = {}
    running = 0
    for c in sorted(total):
        starts[c] = running
        running += total[c]
    rank = [0] * n
    seen = {}
    for i, c in enumerate(last_col):
        r = seen.get(c, 0)
        rank[i] = r
        seen[c] = r + 1
    row = index
    out = []
    for _ in range(n):
        out.append(last_col[row])
        row = starts[last_col[row]] + rank[row]
    return "".join(reversed(out))
