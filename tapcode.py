"""Tap code (5x5 Polybius square with C/K merged).

Rows and columns are 1-based:
    row 1 = A B C D E
    row 2 = F G H I J
    row 3 = L M N O P
    row 4 = Q R S T U
    row 5 = V W X Y Z

The table contains no K: K merges with C, so encoding K yields C's
coordinate (1, 3) and decoding (1, 3) returns "C".
"""

__all__ = ["tapcode_encode", "tapcode_decode"]

# 25 letters, K removed (K is treated as C).
_TABLE = "ABCDEFGHIJLMNOPQRSTUVWXYZ"
_ROW_COL = {ch: (i // 5 + 1, i % 5 + 1) for i, ch in enumerate(_TABLE)}
_LETTER_AT = {i: ch for i, ch in enumerate(_TABLE)}


def tapcode_encode(text: str) -> list[tuple[int, int]]:
    """Encode ``text`` into a list of (row, column) tap-code pairs.

    Preprocessing: text is uppercased and only A-Z letters are kept
    (K counts as C). Non-string input raises TypeError; an empty result
    of preprocessing returns [].
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    pairs: list[tuple[int, int]] = []
    for ch in text.upper():
        if not ("A" <= ch <= "Z"):
            continue
        if ch == "K":
            ch = "C"
        pairs.append(_ROW_COL[ch])
    return pairs


def tapcode_decode(pairs) -> str:
    """Decode a list/tuple of (row, column) pairs back into a string.

    ``pairs`` must be a list or tuple (a str is rejected). Each item must
    be a (row, col) pair of ints (bool rejected) within 1-5; malformed
    shapes or non-int coordinates raise TypeError, out-of-range
    coordinates raise ValueError. An empty sequence returns "".
    """
    if not isinstance(pairs, (list, tuple)):
        raise TypeError(
            f"pairs must be list or tuple, got {type(pairs).__name__}"
        )
    letters: list[str] = []
    for item in pairs:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise TypeError(
                "each pair must be a (row, col) sequence of length 2, "
                f"got {item!r}"
            )
        row, col = item
        if not isinstance(row, int) or isinstance(row, bool):
            raise TypeError(
                f"row must be int, got {type(row).__name__}"
            )
        if not isinstance(col, int) or isinstance(col, bool):
            raise TypeError(
                f"col must be int, got {type(col).__name__}"
            )
        if not (1 <= row <= 5):
            raise ValueError(f"row {row} out of range 1-5")
        if not (1 <= col <= 5):
            raise ValueError(f"col {col} out of range 1-5")
        letters.append(_LETTER_AT[(row - 1) * 5 + (col - 1)])
    return "".join(letters)
