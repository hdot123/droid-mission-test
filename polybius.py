"""Polybius square cipher (5x5 square keyed with MONARCHY, J treated as I)."""

_KEYWORD = "MONARCHY"
_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _build_square():
    seen = set()
    letters = []
    for ch in _KEYWORD:
        c = ch.upper()
        if c == "J":
            c = "I"
        if c not in seen:
            seen.add(c)
            letters.append(c)
    for ch in _ALPHABET:
        if ch == "J":
            continue
        if ch not in seen:
            seen.add(ch)
            letters.append(ch)
    return "".join(letters)


_SQUARE = _build_square()
_POSITION = {ch: (i // 5 + 1, i % 5 + 1) for i, ch in enumerate(_SQUARE)}


def encode(text: str) -> str:
    """Encode letters as 1-based (row, column) pairs formatted RC, space-separated.

    Letters are handled case-insensitively; J is treated as I. Non-letters are
    skipped. Returns an empty string when the text contains no letters.
    """
    pairs = []
    for ch in text:
        if not ch.isalpha():
            continue
        c = ch.upper()
        if c == "J":
            c = "I"
        row, col = _POSITION[c]
        pairs.append(f"{row}{col}")
    return " ".join(pairs)


def decode(text: str) -> str:
    """Decode a sequence of RC coordinate pairs into an uppercase letter string.

    Raises ValueError on non-digit characters, odd-length input, or
    coordinates outside the 5x5 square.
    """
    compact = "".join(text.split())
    if len(compact) % 2 != 0:
        raise ValueError("odd-length coordinate input")
    if any(c not in "0123456789" for c in compact):
        raise ValueError("non-digit characters in coordinate input")
    letters = []
    for i in range(0, len(compact), 2):
        row = int(compact[i])
        col = int(compact[i + 1])
        if not (1 <= row <= 5 and 1 <= col <= 5):
            raise ValueError(f"coordinate out of range: {row}{col}")
        letters.append(_SQUARE[(row - 1) * 5 + (col - 1)])
    return "".join(letters)
