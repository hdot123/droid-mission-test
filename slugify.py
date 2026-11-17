"""Slugify helper: convert arbitrary text to a URL-friendly slug."""

import re

__all__ = ["slugify"]


def slugify(text):
    """Lowercase, replace spaces/underscores with hyphens, drop non
    alphanumeric characters (except hyphens), collapse hyphen runs,
    and strip leading/trailing hyphens."""
    # (1) lowercase
    result = text.lower()
    # (2) replace spaces and underscores with hyphens
    result = result.replace(" ", "-").replace("_", "-")
    # (3) delete anything that is not a letter, digit, or hyphen
    result = re.sub(r"[^a-z0-9-]", "", result)
    # (4) collapse runs of consecutive hyphens into one
    result = re.sub(r"-{2,}", "-", result)
    # (5) strip leading and trailing hyphens
    return result.strip("-")
