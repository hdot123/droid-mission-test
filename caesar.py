"""Caesar shift cipher: encode/decode for ASCII letters only."""


def encode(text, shift):
    """Shift A-Z and a-z in ``text`` by ``shift`` (mod 26), preserving case.

    All other characters are returned unchanged. Negative shifts are legal.
    """
    result = []
    for ch in text:
        if "A" <= ch <= "Z":
            base = ord("A")
            result.append(chr(base + (ord(ch) - base + shift) % 26))
        elif "a" <= ch <= "z":
            base = ord("a")
            result.append(chr(base + (ord(ch) - base + shift) % 26))
        else:
            result.append(ch)
    return "".join(result)


def decode(text, shift):
    """Reverse of ``encode``: shift by ``-shift``."""
    return encode(text, -shift)
