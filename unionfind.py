"""Disjoint-set (union-find) over elements 0..n-1.

Path compression in ``find`` and union by rank in ``union``.
Standard library only.
"""

__all__ = ["UnionFind"]


class UnionFind:
    """Disjoint-set forest for the elements 0..n-1."""

    def __init__(self, n: int):
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(f"n must be int, got {type(n).__name__}")
        if n <= 0:
            raise ValueError(f"n must be positive, got {n}")
        self._n = n
        self._parent = list(range(n))
        self._rank = [0] * n
        self._count = n

    # -- validation helpers -------------------------------------------------

    def _check(self, x) -> None:
        if isinstance(x, bool) or not isinstance(x, int):
            raise TypeError(f"element must be int, got {type(x).__name__}")
        if x < 0 or x >= self._n:
            raise IndexError(f"element {x} out of range [0, {self._n})")

    # -- core operations ----------------------------------------------------

    def find(self, x: int) -> int:
        """Return the root of x's set, with path compression."""
        self._check(x)
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        # path compression
        while self._parent[x] != x:
            parent = self._parent[x]
            self._parent[x] = root
            x = parent
        return root

    def union(self, x: int, y: int) -> bool:
        """Merge the sets of x and y by rank.

        Returns True when a merge happens, False when already same set.
        """
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
        """Current number of disjoint sets."""
        return self._count

    def __len__(self) -> int:
        return self._n

    def groups(self) -> list[list[int]]:
        """All sets: each group ascending, groups ordered by first element."""
        buckets: dict[int, list[int]] = {}
        for x in range(self._n):
            buckets.setdefault(self.find(x), []).append(x)
        ordered = [sorted(members) for members in buckets.values()]
        ordered.sort(key=lambda g: g[0])
        return ordered
