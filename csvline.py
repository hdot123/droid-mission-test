"""Minimal CSV line parsing and generation (no csv module)."""


def parse(line: str) -> list[str]:
    """Parse one line of CSV text into a list of fields.

    Fields are separated by commas. A field wrapped in double quotes may
    contain commas; a doubled double quote inside a quoted field decodes
    to a single double quote. An unquoted field ends at the next comma.
    """
    fields: list[str] = []
    field: list[str] = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch == '"':
            # Quoted run: consume until the closing quote, decoding
            # doubled quotes as a single quote.
            i += 1
            while i < n:
                if line[i] == '"':
                    if i + 1 < n and line[i + 1] == '"':
                        field.append('"')
                        i += 2
                    else:
                        i += 1  # closing quote
                        break
                else:
                    field.append(line[i])
                    i += 1
        elif ch == ',':
            fields.append("".join(field))
            field = []
            i += 1
        else:
            field.append(ch)
            i += 1
    fields.append("".join(field))
    return fields


def join(fields: list[str]) -> str:
    """Generate a CSV line from a list of fields (inverse of parse).

    Fields containing a comma, double quote, or newline are wrapped in
    double quotes; any double quote inside such a field is doubled.
    """
    parts: list[str] = []
    for f in fields:
        if '"' in f:
            parts.append('"' + f.replace('"', '""') + '"')
        elif "," in f or "\n" in f:
            parts.append('"' + f + '"')
        else:
            parts.append(f)
    return ",".join(parts)
