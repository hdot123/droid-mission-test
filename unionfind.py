"""Disjoint set (union-find) over elements 0..n-1.

Path compression in find(), union by rank in union(). Standard library only.
"""


class UnionFind:
    """Union-find structure over the integer elements 0..n-1."""

    def __init__(self, n):
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(f"n must be int, got {type(n).__name__}")
        if n <= 0:
            raise ValueError(f"n must be positive, got {n}")
        self._parent = list(range(n))
        self._rank = [0] * n
        self._count = n

    def _check(self, x):
        if isinstance(x, bool) or not isinstance(x, int):
            raise TypeError(f"element must be int, got {type(x).__name__}")
        if x < 0 or x >= len(self._parent):
            raise IndexError(f"element {x} out of range [0, {len(self._parent)})")

    def find(self, x):
        """Return the root of x's set, compressing the path along the way."""
        self._check(x)
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, x, y):
        """Merge the sets of x and y by rank.

        Returns True if a merge happened, False if they were already united.
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

    def connected(self, x, y):
        """Whether x and y belong to the same set."""
        return self.find(x) == self.find(y)

    @property
    def count(self):
        """Current number of disjoint sets."""
        return self._count

    def __len__(self):
        return len(self._parent)

    def groups(self):
        """All set memberships: each group ascending, groups by first element."""
        buckets = {}
        for i in range(len(self._parent)):
            buckets.setdefault(self.find(i), []).append(i)
        result = list(buckets.values())
        result.sort(key=lambda g: g[0])
        return result
