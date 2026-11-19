"""Union-Find (disjoint set) over elements 0..n-1.

Path compression + union by rank. Standard library only.
"""

from __future__ import annotations

__all__ = ["UnionFind"]


class UnionFind:
    """Disjoint set forest over the integers 0..n-1."""

    def __init__(self, n: int) -> None:
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("n must be an int")
        if n <= 0:
            raise ValueError("n must be positive")
        self._n: int = n
        self._parent: list[int] = list(range(n))
        self._rank: list[int] = [0] * n
        self._count: int = n

    def _check(self, x: int) -> int:
        if isinstance(x, bool) or not isinstance(x, int):
            raise TypeError("element must be an int")
        if x < 0 or x >= self._n:
            raise IndexError("element out of range")
        return x

    def find(self, x: int) -> int:
        """Return the root of x's set with path compression."""
        x = self._check(x)
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        # Path compression.
        while self._parent[x] != x:
            parent = self._parent[x]
            self._parent[x] = root
            x = parent
        return root

    def union(self, x: int, y: int) -> bool:
        """Merge the sets containing x and y; True if a merge happened."""
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx
        self._parent[ry] = rx
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1
        self._count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Whether x and y are in the same set."""
        return self.find(x) == self.find(y)

    @property
    def count(self) -> int:
        """Current number of sets."""
        return self._count

    def __len__(self) -> int:
        return self._n

    def groups(self) -> list[list[int]]:
        """Members of every set; groups sorted by first element ascending."""
        buckets: dict[int, list[int]] = {}
        for elem in range(self._n):
            buckets.setdefault(self.find(elem), []).append(elem)
        result = [sorted(members) for members in buckets.values()]
        result.sort(key=lambda members: members[0])
        return result
