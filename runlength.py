"""Run-length encoding utilities (standard library only)."""


def encode(s):
    """Return run-length encoding of s as a list of (char, run_length) tuples.

    Consecutive identical characters are compressed into a single tuple in
    order of appearance. The empty string encodes to [].
    """
    pairs = []
    if not s:
        return pairs
    current = s[0]
    count = 1
    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            pairs.append((current, count))
            current = ch
            count = 1
    pairs.append((current, count))
    return pairs


def decode(pairs):
    """Expand a list of (char, count) tuples back into the original string.

    Raises ValueError if any count is not a positive integer.
    """
    result = []
    for item in pairs:
        ch, count = item
        if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
            raise ValueError("count must be a positive integer: {!r}".format(count))
        result.append(ch * count)
    return "".join(result)
