"""Caesar cipher: encode/decode with case preservation."""


def encode(text, shift):
    """Shift A-Z and a-z by `shift` (mod 26); other characters unchanged."""
    shift %= 26
    out = []
    for ch in text:
        if "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        elif "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        else:
            out.append(ch)
    return "".join(out)


def decode(text, shift):
    """Inverse of encode: shift by -shift."""
    return encode(text, -shift)
