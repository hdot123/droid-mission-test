"""IPv4 address validation and parsing helpers (standard library only)."""


def is_valid_ipv4(s):
    """Return True if s is a valid IPv4 address, False otherwise (never raises)."""
    if not isinstance(s, str):
        return False
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part or not all("0" <= ch <= "9" for ch in part):
            return False
        if len(part) > 1 and part[0] == "0":
            return False
        if int(part) > 255:
            return False
    return True


def parse_ipv4(s):
    """Parse a valid IPv4 address into a tuple of four ints.

    Raises ValueError if s is not a valid IPv4 address.
    """
    if not is_valid_ipv4(s):
        raise ValueError("invalid IPv4 address: {!r}".format(s))
    return tuple(int(part) for part in s.split("."))
