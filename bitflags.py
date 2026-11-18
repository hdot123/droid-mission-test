"""Bit flag definition and manipulation utilities."""

__all__ = ["define_flags", "combine", "contains", "names_of"]


def define_flags(names):
    """Map each name in order to a successive power of two.

    The first name maps to 1, the second to 2, and so on. Duplicate names
    raise ValueError. An empty list returns an empty dict.
    """
    flags = {}
    for name in names:
        if name in flags:
            raise ValueError("duplicate flag name: {!r}".format(name))
        flags[name] = 1 << len(flags)
    return flags


def combine(flags, *names):
    """Return the bitwise OR of the bit values for the given names.

    No names given returns 0. A name not present in flags raises ValueError.
    """
    value = 0
    for name in names:
        if name not in flags:
            raise ValueError("unknown flag name: {!r}".format(name))
        value |= flags[name]
    return value


def contains(value, flag):
    """Return whether integer value contains integer bit value flag."""
    return bool(value & flag)


def names_of(flags, value):
    """Return names of bits set in value, ordered ascending by bit value.

    If value contains bits undefined in flags, raise ValueError.
    """
    defined_bits = 0
    for bit in flags.values():
        defined_bits |= bit
    if value & ~defined_bits:
        raise ValueError("value contains bits undefined in flags: {!r}".format(value))
    ordered = sorted(flags.items(), key=lambda item: item[1])
    return [name for name, bit in ordered if value & bit]
