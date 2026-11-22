"""Binary search over a sorted (ascending) list."""


def search(sorted_list, target):
    """Return an index of target in sorted_list, or -1 if not present."""
    low = 0
    high = len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        value = sorted_list[mid]
        if value == target:
            return mid
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
