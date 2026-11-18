"""Spartan scytale transposition cipher (encryption and decryption)."""


def _validate_circ(circ):
    if not isinstance(circ, int) or isinstance(circ, bool) or circ <= 0:
        raise ValueError("circ must be a positive integer")
    return circ


def scytale_encrypt(text: str, circ: int) -> str:
    """Encrypt plaintext by laying it out in `circ` columns and reading column by column.

    A short final row is padded with `X` to fill out the last full row.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    _validate_circ(circ)
    if text == "":
        return ""
    padded_len = ((len(text) + circ - 1) // circ) * circ
    padded = text + "X" * (padded_len - len(text))
    rows = [padded[i * circ:(i + 1) * circ] for i in range(padded_len // circ)]
    out = []
    for col in range(circ):
        for row in rows:
            out.append(row[col])
    return "".join(out)


def scytale_decrypt(cipher: str, circ: int) -> str:
    """Decrypt by filling the ciphertext column by column and reading row by row.

    Padding `X` characters are left in the result (not stripped).
    """
    if not isinstance(cipher, str):
        raise TypeError("cipher must be a str")
    _validate_circ(circ)
    if cipher == "":
        return ""
    if len(cipher) % circ != 0:
        raise ValueError("cipher length must be a multiple of circ")
    row_count = len(cipher) // circ
    out = []
    for row in range(row_count):
        for col in range(circ):
            out.append(cipher[col * row_count + row])
    return "".join(out)
