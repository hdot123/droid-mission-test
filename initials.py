"""initials: derive dotted initials from a space-separated name."""


def initials(name):
    """Return the uppercase first letters of each space-separated word,
    joined by dots and terminated with a dot. Extra spaces are ignored."""
    words = name.split()
    return "".join(word[0].upper() + "." for word in words)
