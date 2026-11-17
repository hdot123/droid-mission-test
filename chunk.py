"""Chunking utilities: split a list into fixed-size pieces and flatten back."""


def chunk(items, size):
    """Split *items* into sublists of at most *size* elements, preserving order.

    Returns an empty list when *items* is empty.
    Raises ValueError when *size* <= 0.
    """
    if size <= 0:
        raise ValueError("size must be a positive integer")
    return [items[i:i + size] for i in range(0, len(items), size)]


def flatten(chunks):
    """Concatenate a sequence of sublists in order into a single list."""
    result = []
    for part in chunks:
        result.extend(part)
    return result
