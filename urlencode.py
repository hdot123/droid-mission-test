"""Percent-encoding helpers (UTF-8 based), standard library only."""

_ALWAYS_SAFE = frozenset(
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~"
)


def quote(s, safe="/"):
    """Percent-encode s as UTF-8 bytes with uppercase hex.

    Unreserved characters (A-Z a-z 0-9 -_.~) and characters in safe are
    left unencoded; space becomes %20.
    """
    if not isinstance(s, str):
        raise TypeError("quote() expects a str")
    safe_bytes = safe.encode("utf-8")
    out = []
    for byte in s.encode("utf-8"):
        if byte in _ALWAYS_SAFE or byte in safe_bytes:
            out.append(chr(byte))
        else:
            out.append("%%%02X" % byte)
    return "".join(out)


def unquote(s):
    """Decode '%XX' sequences; invalid sequences are kept literally.

    Assembled bytes are decoded as UTF-8; a UnicodeDecodeError raises
    ValueError.
    """
    if not isinstance(s, str):
        raise TypeError("unquote() expects a str")
    data = bytearray()
    i = 0
    n = len(s)
    while i < n:
        if s[i] == "%":
            hex_part = s[i + 1 : i + 3]
            if len(hex_part) == 2 and all(
                c in "0123456789abcdefABCDEF" for c in hex_part
            ):
                data.append(int(hex_part, 16))
                i += 3
                continue
        data.extend(s[i].encode("utf-8"))
        i += 1
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid UTF-8 sequence in %s: %s" % (s, exc)) from None


def quote_plus(s):
    """Form encoding: space becomes '+', safe defaults to the empty string."""
    if not isinstance(s, str):
        raise TypeError("quote_plus() expects a str")
    return quote(s, safe="").replace("%20", "+")


def unquote_plus(s):
    """Replace '+' with spaces, then apply unquote."""
    if not isinstance(s, str):
        raise TypeError("unquote_plus() expects a str")
    return unquote(s.replace("+", " "))
