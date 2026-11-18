def rot47(text: str) -> str:
    """Encode text with ROT47: printable ASCII (33-126) rotates by 47; others unchanged."""
    return "".join(
        chr(33 + (ord(c) - 33 + 47) % 94) if 33 <= ord(c) <= 126 else c
        for c in text
    )
