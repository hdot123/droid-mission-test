"""Playfair double-letter cipher (5x5 square, J merged into I)."""

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def _build_table(keyword: str) -> dict[str, tuple[int, int]]:
    if not isinstance(keyword, str):
        raise TypeError("keyword must be a str")
    if keyword == "" or not keyword.isalpha():
        raise ValueError("keyword must be a non-empty string of letters")

    seen = set()
    letters: list[str] = []
    for ch in keyword.upper():
        if ch == "J":
            ch = "I"
        if ch not in seen:
            seen.add(ch)
            letters.append(ch)
    for ch in ALPHABET:
        if ch not in seen:
            seen.add(ch)
            letters.append(ch)

    return {ch: (i // 5, i % 5) for i, ch in enumerate(letters)}


def _prepare(text: str) -> str:
    cleaned = [ch for ch in text.upper().replace("J", "I") if ch.isalpha()]
    if not cleaned:
        return ""
    prepared: list[str] = []
    i = 0
    while i < len(cleaned):
        a = cleaned[i]
        b = cleaned[i + 1] if i + 1 < len(cleaned) else ""
        prepared.append(a)
        if b == "":
            prepared.append("X")
            i += 1
            break
        if b == a:
            prepared.append("X")
            i += 1
            continue
        prepared.append(b)
        i += 2
    return "".join(prepared)


def playfair_encrypt(text: str, keyword: str) -> str:
    """Encrypt ``text`` with the Playfair cipher built from ``keyword``."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    table = _build_table(keyword)
    prepared = _prepare(text)
    out: list[str] = []
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i + 1]
        (r1, c1), (r2, c2) = table[a], table[b]
        if r1 == r2:
            out.append(_at(table, r1, (c1 + 1) % 5))
            out.append(_at(table, r2, (c2 + 1) % 5))
        elif c1 == c2:
            out.append(_at(table, (r1 + 1) % 5, c1))
            out.append(_at(table, (r2 + 1) % 5, c2))
        else:
            out.append(_at(table, r1, c2))
            out.append(_at(table, r2, c1))
    return "".join(out)


def playfair_decrypt(cipher: str, keyword: str) -> str:
    """Decrypt ``cipher`` back to the prepared plaintext (X kept)."""
    if not isinstance(cipher, str):
        raise TypeError("cipher must be a str")
    table = _build_table(keyword)
    if len(cipher) % 2 != 0:
        raise ValueError("ciphertext length must be even")
    out: list[str] = []
    for i in range(0, len(cipher), 2):
        a, b = cipher[i], cipher[i + 1]
        (r1, c1), (r2, c2) = table[a], table[b]
        if r1 == r2:
            out.append(_at(table, r1, (c1 - 1) % 5))
            out.append(_at(table, r2, (c2 - 1) % 5))
        elif c1 == c2:
            out.append(_at(table, (r1 - 1) % 5, c1))
            out.append(_at(table, (r2 - 1) % 5, c2))
        else:
            out.append(_at(table, r1, c2))
            out.append(_at(table, r2, c1))
    return "".join(out)


def _at(table: dict[str, tuple[int, int]], row: int, col: int) -> str:
    for ch, (r, c) in table.items():
        if r == row and c == col:
            return ch
    raise LookupError("position not found")  # pragma: no cover
