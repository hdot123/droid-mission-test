"""Base45 encode/decode (RFC 9285).

Standard library only. No dependencies on other modules.
"""

__all__ = ["base45_encode", "base45_decode"]

_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
_TABLE = {c: i for i, c in enumerate(_ALPHABET)}


def base45_encode(data: bytes) -> str:
    """Encode bytes to a Base45 string (RFC 9285).

    Every pair of bytes becomes 3 characters (low order first); a trailing
    single byte becomes 2 characters. Raises TypeError for non-bytes input.
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if len(data) == 0:
        return ""
    out = []
    i = 0
    n = len(data)
    while i + 1 < n:
        x = data[i] * 256 + data[i + 1]
        out.append(_ALPHABET[x % 45])
        out.append(_ALPHABET[(x // 45) % 45])
        out.append(_ALPHABET[x // 2025])
        i += 2
    if i < n:
        x = data[i]
        out.append(_ALPHABET[x % 45])
        out.append(_ALPHABET[x // 45])
    return "".join(out)


def base45_decode(s: str) -> bytes:
    """Decode a Base45 string back to bytes (RFC 9285).

    Raises ValueError for length mod 3 == 1, characters outside the alphabet,
    or decoded group values exceeding 255 (2-char) / 65535 (3-char).
    Raises TypeError for non-str input.
    """
    if not isinstance(s, str):
        raise TypeError("s must be str")
    if len(s) % 3 == 1:
        raise ValueError("invalid length: length mod 3 must not be 1")
    out = bytearray()
    n = len(s)
    i = 0
    while i + 3 <= n:
        try:
            v0 = _TABLE[s[i]]
            v1 = _TABLE[s[i + 1]]
            v2 = _TABLE[s[i + 2]]
        except KeyError as exc:
            raise ValueError("invalid character in input") from exc
        x = v0 + 45 * v1 + 2025 * v2
        if x > 0xFFFF:
            raise ValueError("decoded 3-char group exceeds 65535")
        out.append(x >> 8)
        out.append(x & 0xFF)
        i += 3
    if i < n:
        # Remaining must be exactly 2 chars (length mod 3 == 1 already rejected).
        try:
            v0 = _TABLE[s[i]]
            v1 = _TABLE[s[i + 1]]
        except KeyError as exc:
            raise ValueError("invalid character in input") from exc
        x = v0 + 45 * v1
        if x > 0xFF:
            raise ValueError("decoded 2-char group exceeds 255")
        out.append(x)
    return bytes(out)
