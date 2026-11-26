"""IPv6 text formatting: strict expansion and RFC 5952 compression.

Standalone helpers for the IPv6 *text representation* only. This module is
deliberately independent of the existing IPv4-family modules (ipaddr, ipv4,
ipv4kit): different address family, different functions, no cross-imports.
Only the Python standard library is used.

Contract (both functions):
- accepted inputs: any valid IPv6 text form, expanded or compressed alike;
- invalid address text -> ValueError (bad group count, group out of range,
  multiple '::', leading/trailing single colon, empty string,
  IPv4-embedded form such as '::ffff:1.2.3.4', '%zone' form such as
  'fe80::1%eth0');
- non-str input -> TypeError.
"""

import re

__all__ = ["expand_ipv6", "compress_ipv6"]

# One IPv6 group: 1..4 hex digits (no leading-zero rule at parse time;
# RFC 5952 output rules apply only when compressing).
_GROUP_RE = re.compile(r"\A[0-9a-fA-F]{1,4}\Z")

_NUM_GROUPS = 8


def _split_groups(part):
    """Split a ':'-separated fragment into validated groups ('' -> [])."""
    if part == "":
        return []
    groups = part.split(":")
    for group in groups:
        if not _GROUP_RE.match(group):
            raise ValueError("invalid IPv6 group: %r" % (group,))
    return groups


def _parse(addr):
    """Parse IPv6 text into a list of 8 ints (each 0..65535)."""
    if not isinstance(addr, str):
        raise TypeError(
            "IPv6 address must be str, got %s" % type(addr).__name__
        )
    if "." in addr:
        raise ValueError("IPv4-embedded IPv6 form is not supported: %r" % (addr,))
    if "%" in addr:
        raise ValueError("%zone suffix is not supported: %r" % (addr,))
    if "::" in addr:
        head, _, tail = addr.partition("::")
        if "::" in tail:
            raise ValueError("IPv6 address must contain at most one '::'")
        head_groups = _split_groups(head)
        tail_groups = _split_groups(tail)
        # '::' stands for at least one group of zeros (RFC 4291/5952).
        if len(head_groups) + len(tail_groups) > _NUM_GROUPS - 1:
            raise ValueError("'::' must stand for at least one group")
        zeros = _NUM_GROUPS - len(head_groups) - len(tail_groups)
        groups = head_groups + ["0"] * zeros + tail_groups
    else:
        groups = _split_groups(addr)
        if len(groups) != _NUM_GROUPS:
            raise ValueError(
                "IPv6 address must have %d groups, got %d"
                % (_NUM_GROUPS, len(groups))
            )
    return [int(group, 16) for group in groups]


def expand_ipv6(addr):
    """Expand an IPv6 address to 8 groups of 4 lowercase hex digits.

    Accepts any valid IPv6 text form (expanded or compressed). Raises
    TypeError for non-str input and ValueError for invalid address text.
    """
    values = _parse(addr)
    return ":".join("%04x" % value for value in values)


def _longest_zero_run(values):
    """Return (start, length) of the longest zero run of length >= 2.

    Among equal-length runs the leftmost one wins; runs of a single zero
    group are never compressed (RFC 5952 section 4.2.1).
    """
    best_start = -1
    best_len = 0
    i = 0
    while i < _NUM_GROUPS:
        if values[i] != 0:
            i += 1
            continue
        j = i
        while j < _NUM_GROUPS and values[j] == 0:
            j += 1
        run = j - i
        if run >= 2 and run > best_len:
            best_start, best_len = i, run
        i = j
    return best_start, best_len


def compress_ipv6(addr):
    """Compress an IPv6 address per RFC 5952.

    No leading zeros, lowercase output; only the longest zero run of
    length >= 2 becomes '::' (single zero groups are kept, equal-length
    runs resolve to the leftmost). Accepts any valid IPv6 text form.
    """
    values = _parse(addr)
    parts = ["%x" % value for value in values]
    start, length = _longest_zero_run(values)
    if start >= 0:
        left = ":".join(parts[:start])
        right = ":".join(parts[start + length:])
        return left + "::" + right
    return ":".join(parts)
