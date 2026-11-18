"""Caesar cipher: shift ASCII letters by n positions."""


def shift(text: str, n: int) -> str:
    """Shift ASCII letters in ``text`` by ``n`` positions.

    ``n`` is taken modulo 26; negative values shift backward. Case is
    preserved and non-letter characters are left unchanged.
    """
    n %= 26
    if n == 0:
        return text
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + n) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + n) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)
