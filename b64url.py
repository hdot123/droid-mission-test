"""URL-safe Base64 encoding (RFC 4648) with padding stripped."""

import base64


def encode(data: bytes) -> str:
    """Encode bytes as URL-safe Base64, replacing '+'/'/' with '-'/'_' and
    stripping all trailing '=' padding."""
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be bytes-like")
    return base64.urlsafe_b64encode(bytes(data)).decode("ascii").rstrip("=")


def decode(s: str) -> bytes:
    """Decode a URL-safe Base64 string (with or without padding).

    Returns b"" for the empty string; raises ValueError on illegal
    characters or an invalid length.
    """
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    if s == "":
        return b""
    # Tolerate (but do not require) trailing '=' padding; reject it elsewhere.
    core = s.rstrip("=")
    pad = len(s) - len(core)
    if pad > 2:
        raise ValueError("too much base64url padding")
    if pad and len(s) % 4 != 0:
        raise ValueError("padding must make the total length a multiple of 4")
    if any(c not in
           "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
           for c in core):
        raise ValueError("invalid character in base64url string")
    # Length must not be congruent to 1 mod 4 (one leftover char is illegal).
    if len(core) % 4 == 1:
        raise ValueError("invalid base64url length")
    padded = core + "=" * ((4 - len(core) % 4) % 4)
    try:
        return base64.urlsafe_b64decode(padded)
    except (base64.binascii.Error, ValueError) as exc:
        raise ValueError(f"invalid base64url string: {exc}") from exc
