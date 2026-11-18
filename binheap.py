"""Binary min-heap implemented from scratch (no heapq usage)."""

__all__ = ["BinHeap"]


def _is_number(value):
    """True for ints and floats (bools are explicitly rejected)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class BinHeap:
    """A binary min-heap storing numeric values (bool excluded)."""

    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def is_empty(self):
        """Return True when the heap holds no elements."""
        return not self._items

    def push(self, x):
        """Insert x, maintaining the min-heap property."""
        if not _is_number(x):
            raise TypeError(
                "BinHeap.push accepts numeric values only, got %s" % type(x).__name__
            )
        items = self._items
        items.append(x)
        self._sift_up(len(items) - 1)

    def peek(self):
        """Return the smallest element without removing it."""
        if not self._items:
            raise IndexError("peek from empty BinHeap")
        return self._items[0]

    def pop(self):
        """Remove and return the smallest element."""
        items = self._items
        if not items:
            raise IndexError("pop from empty BinHeap")
        smallest = items[0]
        last = items.pop()
        if items:
            items[0] = last
            self._sift_down(0)
        return smallest

    def _sift_up(self, index):
        items = self._items
        value = items[index]
        while index > 0:
            parent = (index - 1) >> 1
            parent_value = items[parent]
            if value >= parent_value:
                break
            items[index] = parent_value
            index = parent
        items[index] = value

    def _sift_down(self, index):
        items = self._items
        size = len(items)
        value = items[index]
        while True:
            left = index * 2 + 1
            if left >= size:
                break
            right = left + 1
            child = left
            if right < size and items[right] < items[left]:
                child = right
            child_value = items[child]
            if child_value >= value:
                break
            items[index] = child_value
            index = child
        items[index] = value
