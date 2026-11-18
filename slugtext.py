"""URL slug utilities (stdlib only, no imports from other modules)."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(text):
    """Convert arbitrary text to a URL slug.

    Lowercase first, replace each maximal run of characters outside
    [a-z0-9] with a single '-', then strip leading/trailing '-'.
    Non-ASCII letters (e.g. 'e' with acute) count as non-[a-z0-9].
    The result may be the empty string.
    """
    lowered = text.lower()
    slug = _NON_ALNUM.sub("-", lowered)
    return slug.strip("-")


def is_slug(s):
    """Report whether s is a valid slug: non-empty, only [a-z0-9] and '-',
    no leading/trailing '-', and no consecutive '--'."""
    if not s:
        return False
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", s))
