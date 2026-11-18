"""IBAN mod-97 validation (standard library only)."""


def is_valid(iban):
    """Return True if ``iban`` passes the IBAN mod-97 check.

    Strips spaces, upper-cases, moves the first 4 characters to the end,
    expands letters as A=10 ... Z=35, and checks that the resulting
    integer modulo 97 equals 1.  Strings containing characters other
    than letters and digits return False (no exception).  Length and
    country code are not validated.
    """
    if not isinstance(iban, str):
        return False
    compact = iban.replace(" ", "").upper()
    if not compact or not compact.isalnum():
        return False
    rearranged = compact[4:] + compact[:4]
    digits = "".join(
        str(ord(ch) - ord("A") + 10) if ch.isalpha() else ch
        for ch in rearranged
    )
    return int(digits) % 97 == 1
