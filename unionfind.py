"""并查集（union-find）：元素 0..n-1，路径压缩 + 按秩合并。"""

__all__ = ["UnionFind"]


class UnionFind:
    """Disjoint-set forest over elements 0..n-1."""

    def __init__(self, n: int) -> None:
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("n must be an int")
        if n <= 0:
            raise ValueError("n must be positive")
        self._parent = list(range(n))
        self._rank = [0] * n
        self._count = n

    def _check(self, x) -> None:
        if isinstance(x, bool) or not isinstance(x, int):
            raise TypeError("element index must be an int")
        if x < 0 or x >= len(self._parent):
            raise IndexError(f"element index {x} out of range")

    def find(self, x: int) -> int:
        """Return the root of x's set with path compression."""
        self._check(x)
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != x:
            parent = self._parent[x]
            self._parent[x] = root
            x = parent
        return root

    def union(self, x: int, y: int) -> bool:
        """Merge the sets of x and y by rank; True if merged, False if same."""
        self._check(x)
        self._check(y)
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self._rank[rx] < self._rank[ry]:
            self._parent[rx] = ry
        elif self._rank[rx] > self._rank[ry]:
            self._parent[ry] = rx
        else:
            self._parent[ry] = rx
            self._rank[rx] += 1
        self._count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Whether x and y are in the same set."""
        self._check(x)
        self._check(y)
        return self.find(x) == self.find(y)

    @property
    def count(self) -> int:
        """Current number of disjoint sets."""
        return self._count

    def __len__(self) -> int:
        return len(self._parent)

    def groups(self) -> list[list[int]]:
        """Membership table: each group ascending, groups by first element."""
        buckets: dict[int, list[int]] = {}
        for x in range(len(self._parent)):
            buckets.setdefault(self.find(x), []).append(x)
        result = [sorted(members) for members in buckets.values()]
        result.sort(key=lambda group: group[0])
        return result
