"""RFC 4180 subset CSV parsing (standard library only)."""


def parse_line(line):
    """Parse a single CSV line into a list of fields.

    Rules:
    - Fields may be wrapped in double quotes.
    - Inside quotes, commas are literal and "" is an escaped quote.
    - Outside quotes, whitespace is preserved (no trimming).
    - An unclosed quote raises ValueError.
    - An empty line returns [""].
    """
    if not isinstance(line, str):
        raise ValueError("line must be a string")

    fields = []
    field = []
    in_quotes = False
    i = 0
    n = len(line)

    while i < n:
        ch = line[i]

        if in_quotes:
            if ch == '"':
                if i + 1 < n and line[i + 1] == '"':
                    field.append('"')
                    i += 2
                    continue
                in_quotes = False
                i += 1
                continue
            field.append(ch)
            i += 1
            continue

        # outside quotes
        if ch == '"':
            if not field:
                in_quotes = True
                i += 1
                continue
            # a quote appearing mid-field outside a quoted field is literal
            field.append(ch)
            i += 1
            continue

        if ch == ",":
            fields.append("".join(field))
            field = []
            i += 1
            continue

        field.append(ch)
        i += 1

    if in_quotes:
        raise ValueError("unclosed quote in CSV line")

    fields.append("".join(field))
    return fields


def parse(text):
    """Parse multi-line CSV text line by line.

    - A single trailing newline at the end of the text is ignored.
    - Empty text returns [].
    """
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    if text == "":
        return []

    body = text[:-1] if text.endswith("\n") else text
    # split on line boundaries; a final single trailing newline was already removed
    return [parse_line(line) for line in body.split("\n")]
