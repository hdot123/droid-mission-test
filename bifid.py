"""Bifid cipher (5x5 Polybius square + period transposition)."""

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # 25 letters, no J; J merges into I

_SQUARE = {
    char: (idx // 5 + 1, idx % 5 + 1) for idx, char in enumerate(ALPHABET)
}  # letter -> (row, column), both 1-based


def _preprocess(text: str) -> str:
    """Uppercase, merge J into I, keep only in-alphabet characters."""
    out = []
    for ch in text.upper():
        if ch == "J":
            ch = "I"
        if ch in _SQUARE:
            out.append(ch)
    return "".join(out)


def _validate_period(period: int) -> None:
    if isinstance(period, bool) or not isinstance(period, int):
        raise TypeError("period must be an int")
    if period <= 0:
        raise ValueError("period must be positive")


def bifid_encrypt(text: str, period: int = 5) -> str:
    """Encrypt plaintext with the Bifid cipher."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    _validate_period(period)

    plain = _preprocess(text)
    if not plain:
        return ""

    result = []
    for start in range(0, len(plain), period):
        group = plain[start : start + period]
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
            result.append(ALPHABET[(r - 1) * 5 + (c - 1)])
    return "".join(result)


def bifid_decrypt(cipher: str, period: int = 5) -> str:
    """Decrypt Bifid ciphertext back to preprocessed plaintext."""
    if not isinstance(cipher, str):
        raise TypeError("cipher must be a str")
    _validate_period(period)

    if not cipher:
        return ""

    result = []
    for start in range(0, len(cipher), period):
        group = cipher[start : start + period]
        digits = []
        for ch in group:
            up = ch.upper()
            if up == "J":
                up = "I"
            if up not in _SQUARE:
                continue
            r, c = _SQUARE[up]
            digits.append(str(r))
            digits.append(str(c))
        half = len(digits) // 2
        rows = digits[:half]
        cols = digits[half:]
        for r_str, c_str in zip(rows, cols):
            r = int(r_str)
            c = int(c_str)
            result.append(ALPHABET[(r - 1) * 5 + (c - 1)])
    return "".join(result)
