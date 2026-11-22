"""Minimal CSV parsing (RFC 4180 subset).

Standard library only; no third-party dependencies.

Public API:
    parse_line(line) -- parse one CSV line into a list of fields
    parse(text)      -- parse multi-line CSV text into a list of field lists

Rules:
    * A field may be wrapped in double quotes.
    * Inside quotes, commas and escaped double quotes (``""``) are allowed.
    * Whitespace outside quotes is preserved verbatim.
    * An unterminated quoted field raises ValueError.
    * An empty line parses to [""].
"""

__all__ = ["parse_line", "parse"]


def parse_line(line):
    """Parse a single CSV line into a list of fields.

    Raises ValueError for non-string input, unterminated quoted fields,
    or stray characters directly after a closing quote.
    """
    if not isinstance(line, str):
        raise ValueError("line must be a string")

    fields = []
    i = 0
    n = len(line)

    while True:
        if i < n and line[i] == '"':
            # Quoted field: read until the closing quote; "" is an escape.
            i += 1
            buf = []
            closed = False
            while i < n:
                ch = line[i]
                if ch == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        buf.append('"')
                        i += 2
                        continue
                    closed = True
                    i += 1
                    break
                buf.append(ch)
                i += 1
            if not closed:
                raise ValueError("unterminated quoted field")
            if i < n and line[i] != ",":
                raise ValueError("unexpected character after closing quote")
            fields.append("".join(buf))
        else:
            # Unquoted field: read verbatim up to the next comma.
            j = line.find(",", i)
            if j == -1:
                fields.append(line[i:])
                return fields
            fields.append(line[i:j])
            i = j

        # Consume the field separator; loop for the next field.
        if i < n:
            if line[i] != ",":  # pragma: no cover - guarded above
                raise ValueError("unexpected character after closing quote")
            i += 1
            continue
        return fields


def parse(text):
    """Parse multi-line CSV *text* into a list of field lists.

    A single trailing line ending (\\n or \\r\\n) is ignored; empty text
    returns []. Blank interior lines become [""]. Per-line CRLF endings
    are tolerated.
    """
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if text == "":
        return []
    if text.endswith("\r\n"):
        text = text[:-2]
    elif text.endswith("\n"):
        text = text[:-1]
    if text == "":
        return []
    lines = text.split("\n")
    return [parse_line(ln[:-1] if ln.endswith("\r") else ln) for ln in lines]
