"""Caesar cipher: shift letters A-Z / a-z, leave everything else unchanged."""


def encode(text, shift):
    """Shift letters in `text` by `shift` positions (mod 26, negatives legal).

    Case is preserved; non-letter characters are returned unchanged.
    """
    result = []
    for ch in text:
        if "a" <= ch <= "z":
            base = ord("a")
        elif "A" <= ch <= "Z":
            base = ord("A")
        else:
            result.append(ch)
            continue
        result.append(chr(base + (ord(ch) - base + shift) % 26))
    return "".join(result)


def decode(text, shift):
    """Inverse of `encode(text, shift)`."""
    return encode(text, -shift)
