"""Luhn (mod 10) check-digit utilities."""


def check_digit(payload):
    """Return the Luhn check digit for `payload` (digits without check digit).

    Starting from the rightmost digit of `payload`, double every other digit
    (rightmost is position 1, then positions 3, 5, ... are doubled); subtract 9
    from any product greater than 9; sum all resulting digits; the check digit
    is (10 - (sum % 10)) % 10, returned as a character.

    Raises ValueError if `payload` is empty or contains a non-digit character.
    """
    if not isinstance(payload, str) or payload == "" or not payload.isdigit():
        raise ValueError("payload must be a non-empty string of digits")
    total = 0
    # Double every other digit counting from the right: positions 1, 3, 5, ...
    # (0-based reversed indices 0, 2, 4, ...) are doubled.
    for i, ch in enumerate(reversed(payload)):
        d = ord(ch) - 48
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return str((10 - (total % 10)) % 10)


def is_valid(number):
    """Return True if `number` (including its check digit) passes Luhn.

    Non-numeric input (including the empty string) returns False without
    raising.
    """
    if not isinstance(number, str) or number == "" or not number.isdigit():
        return False
    return number[-1] == check_digit(number[:-1])
