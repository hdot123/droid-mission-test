"""Bifid cipher: 5x5 Polybius square plus period transposition.

Standard library only. Does not import any other project module.
"""

from __future__ import annotations

# 25 letters, no J (J is folded into I), row-major fill of the 5x5 square.
ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

__all__ = ["ALPHABET", "bifid_encrypt", "bifid_decrypt"]


def _check_period(period: int) -> None:
    if not isinstance(period, int):
        raise TypeError("period must be int, got %s" % type(period).__name__)
    if period <= 0:
        raise ValueError("period must be positive, got %r" % (period,))


def _prepare(text: str) -> list[str]:
    """Uppercase, fold J into I, keep only letters of the square."""
    folded = text.upper().replace("J", "I")
    return [ch for ch in folded if ch in ALPHABET]


def _row_col(ch: str) -> tuple[int, int]:
    """1-based (row, col) of a letter in the square."""
    idx = ALPHABET.index(ch)
    return idx // 5 + 1, idx % 5 + 1


def _char_at(row: int, col: int) -> str:
    return ALPHABET[(row - 1) * 5 + (col - 1)]


def bifid_encrypt(text: str, period: int = 5) -> str:
    """Encrypt plaintext with the Bifid cipher.

    The prepared text is split into groups of ``period`` characters (the last
    group may be shorter).  Within each group the row coordinates of all
    letters are written first, then the column coordinates; the resulting
    digit string is read two digits at a time as (row, col) pairs and mapped
    back to letters.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str, got %s" % type(text).__name__)
    _check_period(period)
    chars = _prepare(text)
    out: list[str] = []
    for start in range(0, len(chars), period):
        group = chars[start : start + period]
        rows = "".join(str(_row_col(ch)[0]) for ch in group)
        cols = "".join(str(_row_col(ch)[1]) for ch in group)
        digits = rows + cols
        for i in range(0, len(digits), 2):
            out.append(_char_at(int(digits[i]), int(digits[i + 1])))
    return "".join(out)


def bifid_decrypt(cipher: str, period: int = 5) -> str:
    """Decrypt Bifid ciphertext produced by :func:`bifid_encrypt`.

    Same grouping: within each group the two coordinates of every letter are
    written side by side, the first half of the digit string is the row
    coordinates and the second half the column coordinates; pairing them
    restores the letters.  Returns the prepared plaintext (uppercase, with J
    already folded into I).
    """
    if not isinstance(cipher, str):
        raise TypeError("cipher must be str, got %s" % type(cipher).__name__)
    _check_period(period)
    chars = _prepare(cipher)
    out: list[str] = []
    for start in range(0, len(chars), period):
        group = chars[start : start + period]
        n = len(group)
        digits = "".join(str(d) for ch in group for d in _row_col(ch))
        rows, cols = digits[:n], digits[n:]
        for i in range(n):
            out.append(_char_at(int(rows[i]), int(cols[i])))
    return "".join(out)
