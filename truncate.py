"""Word-boundary-first text truncation."""


def truncate(text: str, max_len: int, ellipsis: str = "…") -> str:
    """Truncate ``text`` so the result is at most ``max_len`` characters.

    If ``text`` already fits, it is returned unchanged. Otherwise the budget
    for content is ``max_len - len(ellipsis)``; the head is cut at that budget
    and, when it contains a space, trimmed back to the last word boundary
    (falling back to the hard cut when nothing but spaces precedes it).
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(ellipsis, str):
        raise TypeError("ellipsis must be a str")
    if isinstance(max_len, bool) or not isinstance(max_len, int):
        raise TypeError("max_len must be an int")
    if max_len < len(ellipsis):
        raise ValueError("max_len must be at least the length of ellipsis")

    if len(text) <= max_len:
        return text

    budget = max_len - len(ellipsis)
    head = text[:budget]
    if " " in head:
        candidate = head[: head.rfind(" ")].rstrip(" ")
        if candidate:
            head = candidate
    return head + ellipsis
