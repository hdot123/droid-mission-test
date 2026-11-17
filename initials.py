"""Initials tool: derive dotted uppercase initials from a space-separated name."""


def initials(name: str) -> str:
    """Return the uppercase first letter of each space-separated word,
    joined by dots and terminated by a dot. Extra spaces are ignored."""
    words = name.split()
    if not words:
        return ""
    return ".".join(word[0].upper() for word in words) + "."
