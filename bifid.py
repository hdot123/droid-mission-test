"""Bifid cipher: 5x5 Polybius square with period-based coordinate transposition.

Standard library only. The square is pinned to the alphabet
``ABCDEFGHIKLMNOPQRSTUVWXYZ`` (no J; J folds into I), filled row-major:
row r, column c (both 1-based) holds ``alphabet[(r - 1) * 5 + (c - 1)]``.
"""

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
SQUARE_SIZE = 5

_ROW = {ch: i // SQUARE_SIZE + 1 for i, ch in enumerate(ALPHABET)}
_COL = {ch: i % SQUARE_SIZE + 1 for i, ch in enumerate(ALPHABET)}
_LOOKUP = {r * 10 + c: ALPHABET[(r - 1) * SQUARE_SIZE + (c - 1)]
           for r in range(1, SQUARE_SIZE + 1)
           for c in range(1, SQUARE_SIZE + 1)}


def _validate_period(period: int) -> None:
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int")
    if period <= 0:
        raise ValueError("period must be positive")


def _validate_text(text) -> None:
    if not isinstance(text, str):
        raise TypeError("text must be a str")


def _prepare(text: str) -> str:
    """Uppercase, fold J into I, keep only in-alphabet characters."""
    prepared = []
    for ch in text.upper():
        if ch == "J":
            ch = "I"
        if ch in _ROW:
            prepared.append(ch)
    return "".join(prepared)


def bifid_encrypt(text: str, period: int = 5) -> str:
    """Encrypt *text* with the Bifid cipher at the given *period*."""
    _validate_text(text)
    _validate_period(period)
    prepared = _prepare(text)
    if not prepared:
        return ""
    out = []
    for start in range(0, len(prepared), period):
        group = prepared[start:start + period]
        rows = "".join(str(_ROW[ch]) for ch in group)
        cols = "".join(str(_COL[ch]) for ch in group)
        digits = rows + cols
        for i in range(0, len(digits), 2):
            out.append(_LOOKUP[int(digits[i]) * 10 + int(digits[i + 1])])
    return "".join(out)


def bifid_decrypt(cipher: str, period: int = 5) -> str:
    """Decrypt *cipher* produced by :func:`bifid_encrypt` at *period*.

    Returns the prepared plaintext (uppercase, J folded into I, non-letters
    removed).
    """
    _validate_text(cipher)
    _validate_period(period)
    prepared = _prepare(cipher)
    if not prepared:
        return ""
    out = []
    for start in range(0, len(prepared), period):
        group = prepared[start:start + period]
        digits = "".join(f"{_ROW[ch]}{_COL[ch]}" for ch in group)
        half = len(group)
        rows = digits[:half]
        cols = digits[half:]
        for r, c in zip(rows, cols):
            out.append(_LOOKUP[int(r) * 10 + int(c)])
    return "".join(out)
