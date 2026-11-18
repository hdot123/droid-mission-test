"""ASCII URL slugifier.

Rules (per spec):
- lowercase the input
- keep only ASCII letters and digits
- every run of other characters becomes a single '-'
- strip leading/trailing '-'
- non-ASCII letters (e.g. e-acute) count as non-alphanumeric (no transliteration)
"""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    lowered = text.lower()
    slug = _NON_ALNUM.sub("-", lowered)
    return slug.strip("-")
