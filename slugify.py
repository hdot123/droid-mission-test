"""Slugify text: lowercase, collapse non-alphanumeric runs to '-', strip edges."""

import re

__all__ = ["slugify"]


def slugify(text):
    """Convert text to a lowercase slug.

    Each run of non-alphanumeric characters collapses to a single '-',
    and leading/trailing '-' characters are removed.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return slug.strip("-")
