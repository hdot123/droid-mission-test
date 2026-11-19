"""Word-boundary-first text truncation with an ellipsis suffix."""


def truncate(text: str, max_len: int, ellipsis: str = "…") -> str:
    """Truncate ``text`` to at most ``max_len`` characters.

    Prefers cutting at the last space inside the budget; falls back to a
    hard cut when there is no usable word boundary.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str")
    if not isinstance(ellipsis, str):
        raise TypeError("ellipsis must be str")
    if isinstance(max_len, bool) or not isinstance(max_len, int):
        raise TypeError("max_len must be int")
    if max_len < len(ellipsis):
        raise ValueError("max_len must be >= len(ellipsis)")
    if len(text) <= max_len:
        return text

    budget = max_len - len(ellipsis)
    head = text[:budget]
    if " " in head:
        candidate = head[: head.rfind(" ")].rstrip(" ")
        if candidate:
            head = candidate
    return head + ellipsis
