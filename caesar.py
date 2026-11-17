"""Caesar shift cipher: encode and decode letters only."""


def encode(text, shift):
    """Shift A-Z and a-z by `shift` (mod 26); other characters pass through.

    Negative shifts are legal. Letter case is preserved.
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
    """Exact inverse of encode: shift back by `shift` (mod 26)."""
    return encode(text, -shift)
