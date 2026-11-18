"""Text normalization utilities (standard library only)."""

import re


def normalize(text):
    """Normalize text: lowercase, drop non-alphanumeric/non-whitespace chars,
    collapse runs of whitespace to a single space, and strip ends."""
    lowered = text.lower()
    cleaned = re.sub(r"[^a-z0-9\s]", "", lowered)
    collapsed = re.sub(r"\s+", " ", cleaned)
    return collapsed.strip()
