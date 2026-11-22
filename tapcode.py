"""Tap code (5x5 grid, C/K merged) encode/decode helpers."""

# Fixed 5x5 table, rows and columns 1-based. The table contains no K:
# K merges with C, so encoding K yields C's coordinate (1, 3).
_LETTERS = "ABCDEFGHIJLMNOPQRSTUVWXYZ"


def _letter_to_pair(letter: str) -> tuple[int, int]:
    """Map an uppercase A-Z letter (K treated as C) to its (row, column)."""
    if letter == "K":
        letter = "C"
    index = _LETTERS.index(letter)
    return (index // 5 + 1, index % 5 + 1)


def tapcode_encode(text: str) -> list[tuple[int, int]]:
    """Encode text to a list of (row, column) tap-code pairs.

    Preprocessing: uppercase the text and keep only A-Z characters
    (K is counted as C). Non-str input raises TypeError; an empty
    string returns [].
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    pairs: list[tuple[int, int]] = []
    for char in text.upper():
        if "A" <= char <= "Z":
            pairs.append(_letter_to_pair(char))
    return pairs


def _check_coordinate(value, name: str) -> int:
    """Validate one coordinate: int (bool rejected), within 1-5."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int")
    if not 1 <= value <= 5:
        raise ValueError(f"{name} must be in 1-5, got {value}")
    return value


def tapcode_decode(pairs) -> str:
    """Decode a list/tuple of (row, column) pairs back to uppercase text.

    pairs itself must be a list or tuple (a str is rejected); each item
    must be a (row, column) pair of ints (bool rejected) with both
    coordinates in 1-5. Malformed shape or non-int coordinates raise
    TypeError; out-of-range coordinates raise ValueError. An empty
    collection returns "".
    """
    if not isinstance(pairs, (list, tuple)):
        raise TypeError("pairs must be a list or tuple")
    chars: list[str] = []
    for item in pairs:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise TypeError("each pair must be a (row, column) sequence of length 2")
        row = _check_coordinate(item[0], "row")
        col = _check_coordinate(item[1], "column")
        chars.append(_LETTERS[(row - 1) * 5 + (col - 1)])
    return "".join(chars)
