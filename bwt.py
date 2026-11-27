"""Burrows-Wheeler transform (BWT): encode and decode.

BWT is a block rotation permutation (it does not compress by itself);
it is unrelated to run-length coding helpers such as codec_rle/runlength.

Encoding sorts all cyclic rotations of the input string.  Ties between
identical rotation strings (which occur for periodic inputs such as
"abab" or "aaaa") are broken explicitly by the original offset in
ascending order -- the tie-break is pinned by the sort key itself and
not left to the stability of the sort.
"""

from __future__ import annotations

__all__ = ["bwt_encode", "bwt_decode"]


def _check_str(value, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, str):
        raise TypeError(f"{name} must be str, got {type(value).__name__}")


def bwt_encode(s: str) -> tuple[str, int]:
    """Return ``(last_column, primary_index)`` for string ``s``.

    All ``n`` cyclic rotations of ``s`` are sorted ascending by
    ``(rotation string, original offset)``.  The last column is the last
    character of each sorted rotation; the primary index is the row of the
    offset-0 rotation (the original string).

    Raises:
        TypeError: if ``s`` is not a ``str``.
        ValueError: if ``s`` is empty.
    """
    _check_str(s, "s")
    if len(s) == 0:
        raise ValueError("s must be a non-empty string")

    n = len(s)
    rotations = [(s[i:] + s[:i], i) for i in range(n)]
    rotations.sort(key=lambda item: (item[0], item[1]))

    last_column = "".join(rotation[-1] for rotation, _ in rotations)
    primary_index = next(i for _, i in rotations if i == 0)
    return last_column, primary_index


def bwt_decode(last_col: str, index: int) -> str:
    """Recover the original string from BWT output ``(last_col, index)``.

    Raises:
        TypeError: if ``last_col`` is not a ``str`` or ``index`` is not an
            ``int`` (``bool`` counts as not an ``int``).
        ValueError: if ``last_col`` is empty or ``index`` is out of range
            (``< 0`` or ``>= len(last_col)``).
    """
    _check_str(last_col, "last_col")
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError(f"index must be int, got {type(index).__name__}")
    if len(last_col) == 0:
        raise ValueError("last_col must be a non-empty string")
    if index < 0 or index >= len(last_col):
        raise ValueError(f"index {index} out of range for length {len(last_col)}")

    n = len(last_col)
    # Counting sort of the columns: full rotation-matrix construction,
    # then take the column preceding last_col.
    first_col = sorted(range(n), key=lambda i: (last_col[i], i))
    rows = ["" for _ in range(n)]
    for _ in range(n):
        rows = [last_col[i] + rows[i] for i in first_col]
    return rows[first_col[index]]
