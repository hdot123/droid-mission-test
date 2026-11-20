"""Bifid cipher: 5x5 Polybius square plus period transposition.

The square is pinned to the 25-letter alphabet ABCDEFGHIKLMNOPQRSTUVWXYZ
(no J; plaintext J folds into I), filled row-major: cell (r, c) with
r, c in 1..5 holds alphabet index (r - 1) * 5 + (c - 1) (0-based).

Only the standard library is used; this module imports nothing from the
rest of the project.
"""

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# letter -> (row, column), both 1-based
_SQUARE = {}
for _i, _ch in enumerate(ALPHABET):
    _SQUARE[_ch] = (_i // 5 + 1, _i % 5 + 1)


def _validate_period(period):
    """period must be a positive int: non-int -> TypeError, <= 0 -> ValueError."""
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int, got %s" % type(period).__name__)
    if period <= 0:
        raise ValueError("period must be positive, got %r" % (period,))


def _prepare(text):
    """Uppercase, fold J into I, keep only characters in the alphabet."""
    if not isinstance(text, str):
        raise TypeError("text must be a str, got %s" % type(text).__name__)
    out = []
    for ch in text.upper():
        if ch == "J":
            ch = "I"
        if ch in _SQUARE:
            out.append(ch)
    return "".join(out)


def bifid_encrypt(text: str, period: int = 5) -> str:
    """Encrypt plaintext with the Bifid cipher.

    Preprocess the text (uppercase, J -> I, drop non-alphabet characters),
    split it into groups of ``period`` characters (last group may be
    shorter), concatenate each group's row coordinates followed by its
    column coordinates into one digit string, then map every (row, column)
    pair of that string back to its character. Empty input returns "".
    """
    _validate_period(period)
    prepared = _prepare(text)
    if not prepared:
        return ""
    out = []
    for start in range(0, len(prepared), period):
        group = prepared[start:start + period]
        rows = []
        cols = []
        for ch in group:
            r, c = _SQUARE[ch]
            rows.append(str(r))
            cols.append(str(c))
        digits = "".join(rows) + "".join(cols)
        for i in range(0, len(digits), 2):
            r = int(digits[i])
            c = int(digits[i + 1])
            out.append(ALPHABET[(r - 1) * 5 + (c - 1)])
    return "".join(out)


def bifid_decrypt(cipher: str, period: int = 5) -> str:
    """Decrypt Bifid ciphertext (inverse of :func:`bifid_encrypt`).

    Same grouping: within each group write every character's two
    coordinates as a digit string; the first half of that string holds the
    row-coordinate column and the second half the column-coordinate
    column, paired digit-by-digit to recover the plaintext. Returns the
    preprocessed plaintext (including letters folded into I). Empty input
    returns "".
    """
    _validate_period(period)
    prepared = _prepare(cipher)
    if not prepared:
        return ""
    out = []
    for start in range(0, len(prepared), period):
        group = prepared[start:start + period]
        digits = []
        for ch in group:
            r, c = _SQUARE[ch]
            digits.append(str(r))
            digits.append(str(c))
        digits = "".join(digits)
        half = len(group)
        rows = digits[:half]
        cols = digits[half:]
        for i in range(half):
            r = int(rows[i])
            c = int(cols[i])
            out.append(ALPHABET[(r - 1) * 5 + (c - 1)])
    return "".join(out)
