"""deque — a double-ended queue (标准库 only).

Deque supports O(1) append/pop at both ends with a Python list as the
backing store (amortized; pops from the left shift the list, which is
fine for the sizes exercised here, but we use collections.deque under
the hood to keep both ends truly O(1)).

Only the standard library is used; no imports of sibling modules.
"""

from collections import deque as _CDeque
from typing import Iterable, Iterator, Optional


class Deque:
    """Double-ended queue constructible from an iterable.

    Deque() builds an empty queue; Deque(iterable) enqueues items in
    iteration order (left to right).
    """

    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        if iterable is None:
            self._items: _CDeque = _CDeque()
        else:
            self._items = _CDeque(iterable)

    def append(self, x) -> None:
        """Enqueue x at the right end."""
        self._items.append(x)

    def appendleft(self, x) -> None:
        """Enqueue x at the left end."""
        self._items.appendleft(x)

    def pop(self):
        """Dequeue and return the right-end item.

        Raises IndexError on an empty deque.
        """
        if not self._items:
            raise IndexError("pop from an empty Deque")
        return self._items.pop()

    def popleft(self):
        """Dequeue and return the left-end item.

        Raises IndexError on an empty deque.
        """
        if not self._items:
            raise IndexError("popleft from an empty Deque")
        return self._items.popleft()

    def peek(self):
        """Return the right-end item without removing it.

        Raises IndexError on an empty deque.
        """
        if not self._items:
            raise IndexError("peek from an empty Deque")
        return self._items[-1]

    def peekleft(self):
        """Return the left-end item without removing it.

        Raises IndexError on an empty deque.
        """
        if not self._items:
            raise IndexError("peekleft from an empty Deque")
        return self._items[0]

    def clear(self) -> None:
        """Remove all items."""
        self._items.clear()

    def is_empty(self) -> bool:
        """Return True when the deque holds no items."""
        return not self._items

    def to_list(self) -> list:
        """Return a left-to-right list snapshot of the deque."""
        return list(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator:
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Deque({self.to_list()!r})"
