"""Flatten arbitrarily nested lists into a one-dimensional list."""


def flatten(nested):
    """Flatten arbitrarily nested lists, preserving element order.

    Non-list elements are kept as-is. An empty list returns an empty list.
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
