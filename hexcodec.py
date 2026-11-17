"""Encode bytes as a lowercase hex string and decode it back."""


def encode(data: bytes) -> str:
    """Return the lowercase hexadecimal representation of *data*."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes-like")
    return bytes(data).hex()


def decode(s: str) -> bytes:
    """Decode a hex string back to bytes.

    Raises ValueError on odd-length strings or non-hex characters.
    """
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    if len(s) % 2 != 0:
        raise ValueError(f"odd-length hex string: {s!r}")
    # Strict check: bytes.fromhex tolerates ASCII whitespace, but the
    # spec requires any non-hex character to be rejected.
    if any(c not in "0123456789abcdefABCDEF" for c in s):
        raise ValueError(f"invalid hex character in string: {s!r}")
    return bytes.fromhex(s)
