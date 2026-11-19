"""Fixed-capacity ring (circular) buffer with FIFO overwrite."""

from __future__ import annotations


class RingBuffer:
    """A fixed-capacity circular buffer.

    Appending to a full buffer overwrites the oldest element (FIFO
    overwrite). Iteration and to_list() yield elements oldest-to-newest.
    """

    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError(f"capacity must be an int, got {type(capacity).__name__}")
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        self._capacity = capacity
        self._items: list = [None] * capacity
        self._start = 0  # index of the oldest element
        self._size = 0   # current number of elements

    @property
    def capacity(self) -> int:
        return self._capacity

    def append(self, item) -> None:
        """Append one item, overwriting the oldest when full."""
        if self._size < self._capacity:
            index = (self._start + self._size) % self._capacity
            self._items[index] = item
            self._size += 1
        else:
            self._items[self._start] = item
            self._start = (self._start + 1) % self._capacity

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._capacity

    def to_list(self) -> list:
        """Return all elements oldest-to-newest."""
        return [self._items[(self._start + i) % self._capacity] for i in range(self._size)]

    def __iter__(self):
        """Iterate oldest-to-newest."""
        return iter(self.to_list())
