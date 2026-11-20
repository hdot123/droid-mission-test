"""Text truncation with word-boundary preference."""

__all__ = ["truncate"]


def truncate(text: str, max_len: int, ellipsis: str = "…") -> str:
    """Truncate ``text`` to at most ``max_len`` characters.

    Prefers cutting at the last word boundary inside the budget before the
    ellipsis; falls back to a hard character cut when no word boundary is
    available (or the boundary candidate would be empty).
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(ellipsis, str):
        raise TypeError("ellipsis must be a str")
    if isinstance(max_len, bool) or not isinstance(max_len, int):
        raise TypeError("max_len must be an int")
    if max_len < len(ellipsis):
        raise ValueError("max_len must be >= len(ellipsis)")

    if len(text) <= max_len:
        return text

    budget = max_len - len(ellipsis)
    head = text[:budget]
    if " " in head:
        candidate = head.rsplit(" ", 1)[0].rstrip(" ")
        if candidate:
            head = candidate
    return head + ellipsis
