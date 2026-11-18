"""Min-priority queue with FIFO tie-breaking."""

import heapq


class PriorityQueue:
    """Priority queue where smaller priority values dequeue first.

    Ties in priority are broken by enqueue order (first in, first out).
    Items themselves do not need to be comparable.
    """

    def __init__(self):
        self._heap = []
        self._seq = 0

    def push(self, item, priority):
        """Enqueue ``item`` with the given numeric ``priority``."""
        heapq.heappush(self._heap, (priority, self._seq, item))
        self._seq += 1

    def pop(self):
        """Remove and return the element with the smallest priority."""
        if not self._heap:
            raise IndexError("pop from empty PriorityQueue")
        _, _, item = heapq.heappop(self._heap)
        return item

    def peek(self):
        """Return the next element without removing it."""
        if not self._heap:
            raise IndexError("peek from empty PriorityQueue")
        return self._heap[0][2]

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        """Return whether the queue is empty."""
        return not self._heap
