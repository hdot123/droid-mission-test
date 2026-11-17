"""Parse INI-format text into nested dicts (section -> key -> value)."""


def _strip_matching_quotes(value):
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    return value


def parse(text):
    """Parse INI text and return a dict of section name -> dict of key -> value.

    Rules:
    - Leading/trailing whitespace of each line is ignored.
    - Blank lines and full-line comments starting with ';' or '#' are ignored.
    - '[name]' headers set the current section (name stripped, case-sensitive).
    - 'key = value' / 'key: value': key stripped and lowercased, value stripped.
    - Keys before any section header go into section 'DEFAULT'.
    - A repeated key in a section overwrites the earlier value.
    - A repeated section header merges into the same section.
    - A value wrapped in one matching pair of double quotes has them stripped
      with no escape processing.
    - A line with neither '=' nor ':' (and not header/blank/comment) raises
      ValueError whose message contains the line number.
    - Empty text returns {}.
    """
    result = {}
    current = None
    for lineno, raw in enumerate(text.split("\n"), start=1):
        line = raw.strip()
        if not line or line[0] in ";#":
            continue
        if line.startswith("[") and line.endswith("]"):
            name = line[1:-1].strip()
            current = result.setdefault(name, {})
            continue
        if "=" in line:
            key, _, value = line.partition("=")
        elif ":" in line:
            key, _, value = line.partition(":")
        else:
            raise ValueError("invalid line %d: %r" % (lineno, line))
        key = key.strip().lower()
        value = _strip_matching_quotes(value.strip())
        if current is None:
            current = result.setdefault("DEFAULT", {})
        current[key] = value
    return result


def get(text, section, key, default=None):
    """Convenience accessor: section names case-sensitive, keys case-insensitive.

    Returns `default` when the section or key is missing.
    """
    sec = parse(text).get(section)
    if not sec:
        return default
    return sec.get(key.lower(), default)
