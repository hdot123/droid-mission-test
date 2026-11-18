"""Keyword columnar transposition cipher."""

__all__ = ["columnar_encrypt", "columnar_decrypt"]


def _validate(text: object, keyword: object) -> tuple[str, str]:
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(keyword, str):
        raise TypeError("keyword must be a str")
    if not keyword or not keyword.isalpha():
        raise ValueError("keyword must be a non-empty pure alphabetic string")
    return text, keyword


def _column_order(keyword: str) -> list[int]:
    """Column read order: stable sort on (letter, column index)."""
    return sorted(range(len(keyword)), key=lambda i: (keyword[i], i))


def columnar_encrypt(text: str, keyword: str) -> str:
    text, keyword = _validate(text, keyword)
    if text == "":
        return ""
    width = len(keyword)
    padded = text + "X" * ((-len(text)) % width)
    rows = [padded[i : i + width] for i in range(0, len(padded), width)]
    order = _column_order(keyword)
    return "".join(rows[r][c] for c in order for r in range(len(rows)))


def columnar_decrypt(cipher: str, keyword: str) -> str:
    cipher, keyword = _validate(cipher, keyword)
    if cipher == "":
        return ""
    width = len(keyword)
    if len(cipher) % width != 0:
        raise ValueError("ciphertext length must be a multiple of keyword length")
    height = len(cipher) // width
    order = _column_order(keyword)
    grid = [[""] * width for _ in range(height)]
    for pos, c in enumerate(order):
        col = cipher[pos * height : (pos + 1) * height]
        for r in range(height):
            grid[r][c] = col[r]
    return "".join("".join(row) for row in grid)
