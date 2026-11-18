"""CSV single-field codec (RFC 4180 conventions)."""

SPECIALS = (",", '"', "\n", "\r")


def encode(field: str) -> str:
    """Encode one CSV field per RFC 4180.

    The field is wrapped in double quotes when it contains a comma, a
    double quote, or a newline (``\\n`` or ``\\r``); internal double
    quotes are written as two quotes.  Otherwise it is returned as-is.
    """
    if any(ch in field for ch in SPECIALS):
        return '"' + field.replace('"', '""') + '"'
    return field


def decode(text: str) -> str:
    """Decode one CSV field per RFC 4180 (inverse of :func:`encode`).

    Unquoted text is returned as-is.  Quoted text must be paired: the
    opening quote must be closed with nothing after it, and internal
    ``""`` pairs decode to a single ``"``.  Unclosed quotes or trailing
    characters after the closing quote raise ``ValueError``.
    """
    if not text.startswith('"'):
        return text

    out = []
    i = 1
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == '"':
            if i + 1 < n and text[i + 1] == '"':
                out.append('"')
                i += 2
            else:
                # Closing quote: nothing may follow it.
                if i + 1 != n:
                    raise ValueError(
                        "trailing characters after closing quote: %r" % text
                    )
                return "".join(out)
        else:
            out.append(ch)
            i += 1
    raise ValueError("unclosed quote: %r" % text)
