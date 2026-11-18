"""Fixed-capacity LRU cache (stdlib only).

Implements the LRUCache class required by work order #248 / sub-issue #250.
"""

from collections import OrderedDict

__all__ = ["LRUCache"]


class LRUCache:
    """A fixed-capacity least-recently-used cache.

    capacity must be a positive integer, otherwise ValueError is raised.
    """

    def __init__(self, capacity):
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self._capacity = capacity
        self._data = OrderedDict()  # insertion order == recency order (oldest first)

    @property
    def capacity(self):
        return self._capacity

    def get(self, key, default=None):
        """Return the value for key and mark it most recently used.

        On a miss, return default and leave the order unchanged.
        """
        if key in self._data:
            value = self._data.pop(key)
            self._data[key] = value
            return value
        return default

    def put(self, key, value):
        """Insert or update key.

        An existing key is refreshed to most-recently-used. After writing, if
        the element count exceeds capacity, the least recently used item is
        evicted.
        """
        if key in self._data:
            self._data.pop(key)
        self._data[key] = value
        if len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        """Check key existence without refreshing recency order."""
        return key in self._data

    def keys_oldest_first(self):
        """Return keys from least recently used to most recently used."""
        return list(self._data.keys())
