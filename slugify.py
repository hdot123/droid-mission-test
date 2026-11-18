"""URL slug generation utility (unrelated to the plugin registry)."""

import re

__all__ = ["slugify"]


def slugify(text):
    """Return a URL slug for *text*.

    Lowercases the text, collapses runs of whitespace and underscores into a
    single hyphen, removes every character other than ASCII letters, digits,
    and hyphens, then strips leading and trailing hyphens.
    """
    lowered = text.lower()
    collapsed = re.sub(r"[\s_]+", "-", lowered)
    cleaned = re.sub(r"[^a-z0-9-]", "", collapsed)
    return cleaned.strip("-")
