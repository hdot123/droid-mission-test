"""Build uppercase dotted initials from a name."""


def initials(name: str) -> str:
    """Return the initials of a name, e.g. "ada lovelace" -> "A.L."."""
    if not name:
        return ""
    words = name.replace("-", " ").split()
    return "".join(word[0].upper() + "." for word in words if word)
