"""Caesar cipher helpers (standard library only)."""


def _shift_letter(letter, shift):
    base = ord("A") if letter.isupper() else ord("a")
    return chr((ord(letter) - base + shift) % 26 + base)


def encrypt(text, shift):
    """Shift English letters by `shift` (mod 26); other characters unchanged."""
    normalized = shift % 26
    return "".join(
        _shift_letter(ch, normalized) if ch.isalpha() and ch.isascii() else ch
        for ch in text
    )


def decrypt(text, shift):
    """Reverse of encrypt(text, shift)."""
    return encrypt(text, -shift)
