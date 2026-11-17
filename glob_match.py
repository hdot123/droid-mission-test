"""Unix wildcard subset matching (glob).

Implements exactly one public function, match(pattern, name), with:

- '*' matches any sequence of characters, including the empty sequence
- '?' matches exactly one character
- '[seq]' matches any single character contained in the sequence,
  including ranges such as 'a-c'
- '[!seq]' matches any single character not in the sequence
- every other character matches literally
- matching is case-sensitive
- an empty pattern matches only the empty string
- an unclosed '[' raises ValueError
"""


def _parse_class(pattern, start):
    """Parse a character class starting at pattern[start] == '['.

    Returns (token, next_index) or raises ValueError when unclosed.
    """
    i = start + 1
    n = len(pattern)
    negated = False
    if i < n and pattern[i] == '!':
        negated = True
        i += 1
    members = []
    first = True
    while i < n:
        c = pattern[i]
        if c == ']' and not first:
            return ('class', negated, members), i + 1
        first = False
        # Range such as 'a-c' (a trailing '-' before ']' stays literal).
        if i + 2 < n and pattern[i + 1] == '-' and pattern[i + 2] != ']':
            lo, hi = c, pattern[i + 2]
            if lo > hi:
                lo, hi = hi, lo
            members.append(('range', lo, hi))
            i += 3
        else:
            members.append(('char', c))
            i += 1
    raise ValueError(
        "unclosed character class in pattern at position %d" % start
    )


def _tokenize(pattern):
    tokens = []
    i = 0
    n = len(pattern)
    while i < n:
        c = pattern[i]
        if c == '*':
            tokens.append(('any',))
            i += 1
        elif c == '?':
            tokens.append(('one',))
            i += 1
        elif c == '[':
            token, i = _parse_class(pattern, i)
            tokens.append(token)
        else:
            tokens.append(('lit', c))
            i += 1
    return tokens


def _class_matches(token, ch):
    negated = token[1]
    hit = False
    for member in token[2]:
        if member[0] == 'char':
            if ch == member[1]:
                hit = True
                break
        else:  # range
            if member[1] <= ch <= member[2]:
                hit = True
                break
    return hit != negated


def match(pattern, name):
    """Return True if name matches the glob pattern, else False.

    Raises ValueError if the pattern contains an unclosed '['.
    """
    tokens = _tokenize(pattern)
    # Set of positions in name reachable after consuming each token.
    positions = {0}
    for token in tokens:
        kind = token[0]
        nxt = set()
        if kind == 'any':
            if positions:
                nxt.update(range(min(positions), len(name) + 1))
        elif kind == 'one':
            for p in positions:
                if p < len(name):
                    nxt.add(p + 1)
        elif kind == 'lit':
            ch = token[1]
            for p in positions:
                if p < len(name) and name[p] == ch:
                    nxt.add(p + 1)
        else:  # class
            for p in positions:
                if p < len(name) and _class_matches(token, name[p]):
                    nxt.add(p + 1)
        if not nxt:
            return False
        positions = nxt
    return len(name) in positions
