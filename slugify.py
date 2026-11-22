import re


def slugify(text):
    """Convert text to a URL slug.

    - Lowercase everything.
    - Replace every character that is not an English letter or digit with '-'.
    - Collapse runs of '-' into a single '-'.
    - Strip leading/trailing '-'.
    """
    lowered = text.lower()
    replaced = re.sub(r"[^a-z0-9]", "-", lowered)
    collapsed = re.sub(r"-+", "-", replaced)
    return collapsed.strip("-")
