"""Word and character counting text utilities."""


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in text."""
    return len(text.split())


def char_count(text: str, include_spaces: bool = True) -> int:
    """Return the number of characters in text.

    When include_spaces is False, whitespace characters are excluded.
    """
    if include_spaces:
        return len(text)
    return len("".join(ch for ch in text if not ch.isspace()))
