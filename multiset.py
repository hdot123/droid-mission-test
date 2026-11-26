"""MultiSet — a mutable multiset with set algebra.

Standard library only; does not import from any sibling work-order module.

Set-algebra semantics (deliberately not arithmetic):
  - union: per-item maximum (not a sum)
  - intersection: per-item minimum (not a product)
  - difference: per-item subtraction, floored at 0 with zero items dropped
"""

__all__ = ["MultiSet"]


class MultiSet:
    """Mutable multiset: per-item counts kept in first-insertion order."""

    def __init__(self, iterable=None):
        self._counts = {}
        if iterable is not None:
            for item in iterable:
                self._counts[item] = self._counts.get(item, 0) + 1

    # -- internal helpers ---------------------------------------------

    @staticmethod
    def _validate_n(n):
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("n must be an int, got %s" % (type(n).__name__,))
        if n < 1:
            raise ValueError("n must be >= 1, got %r" % (n,))

    @staticmethod
    def _require_multiset(other):
        if not isinstance(other, MultiSet):
            raise TypeError(
                "expected a MultiSet, got %s" % (type(other).__name__,)
            )

    @classmethod
    def _from_counts(cls, counts):
        ms = cls()
        ms._counts = counts
        return ms

    # -- mutation ------------------------------------------------------

    def add(self, item, n=1):
        """Add n copies of item. n must be an int >= 1 (bool not allowed)."""
        self._validate_n(n)
        self._counts[item] = self._counts.get(item, 0) + n

    def remove(self, item, n=1):
        """Remove n copies of item.

        Raises ValueError when fewer than n copies are held; a count that
        reaches zero deletes the item entirely.
        """
        self._validate_n(n)
        held = self._counts.get(item, 0)
        if n > held:
            raise ValueError(
                "cannot remove %d of %r: only %d held" % (n, item, held)
            )
        left = held - n
        if left > 0:
            self._counts[item] = left
        else:
            del self._counts[item]

    # -- queries --------------------------------------------------------

    def count(self, item):
        """Number of copies of item; 0 when the item is absent."""
        return self._counts.get(item, 0)

    def total(self):
        """Sum of all counts."""
        return sum(self._counts.values())

    def distinct(self):
        """Number of distinct items."""
        return len(self._counts)

    def elements(self):
        """All items listed grouped, in first-insertion order."""
        out = []
        for item, n in self._counts.items():
            out.extend([item] * n)
        return out

    def to_dict(self):
        """A plain-dict copy of {item: count}."""
        return dict(self._counts)

    # -- set algebra: each returns a NEW MultiSet, originals untouched --

    def union(self, other):
        self._require_multiset(other)
        counts = dict(self._counts)
        for item, n in other._counts.items():
            if n > counts.get(item, 0):
                counts[item] = n
        return self._from_counts(counts)

    def intersection(self, other):
        self._require_multiset(other)
        counts = {}
        for item, n in self._counts.items():
            m = other._counts.get(item, 0)
            if m:
                counts[item] = n if n < m else m
        return self._from_counts(counts)

    def difference(self, other):
        self._require_multiset(other)
        counts = {}
        for item, n in self._counts.items():
            left = n - other._counts.get(item, 0)
            if left > 0:
                counts[item] = left
        return self._from_counts(counts)

    def is_subset(self, other):
        """True when every item of self is held in other at >= the count."""
        self._require_multiset(other)
        return all(
            other._counts.get(item, 0) >= n
            for item, n in self._counts.items()
        )

    # -- protocols -------------------------------------------------------

    def __len__(self):
        return self.total()

    def __contains__(self, item):
        return item in self._counts

    def __eq__(self, other):
        if not isinstance(other, MultiSet):
            return False
        return self._counts == other._counts

    def __repr__(self):
        return "MultiSet(%r)" % (self._counts,)
