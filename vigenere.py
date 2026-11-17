"""Vigenere cipher: encrypt/decrypt with a letter-only key."""


def _validate_key(key):
    if not isinstance(key, str) or key == "" or not key.isalpha():
        raise ValueError("key must be a non-empty string of letters only")


def _shift_char(ch, shift):
    if ch.isupper():
        base = ord("A")
    elif ch.islower():
        base = ord("a")
    else:
        return ch
    return chr(base + (ord(ch) - base + shift) % 26)


def encrypt(text, key):
    """Shift alphabetic characters forward by the cycling key letters."""
    _validate_key(key)
    lowered = key.lower()
    result = []
    idx = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(lowered[idx % len(lowered)]) - ord("a")
            result.append(_shift_char(ch, shift))
            idx += 1
        else:
            result.append(ch)
    return "".join(result)


def decrypt(text, key):
    """Reverse of encrypt: shift alphabetic characters backward by the key."""
    _validate_key(key)
    lowered = key.lower()
    result = []
    idx = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(lowered[idx % len(lowered)]) - ord("a")
            result.append(_shift_char(ch, -shift))
            idx += 1
        else:
            result.append(ch)
    return "".join(result)
