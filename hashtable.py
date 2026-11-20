"""Open-addressing hash table: linear probing, tombstones, growth.

Keys must be str.  Hashing is pinned to djb2 (32-bit), never builtin hash().
"""

_EMPTY = object()
_TOMBSTONE = object()


def djb2(key: str) -> int:
    """djb2 over the UTF-8 bytes of key, 32-bit wraparound."""
    h = 5381
    for byte in key.encode("utf-8"):
        h = (h * 33 + byte) & 0xFFFFFFFF
    return h


class HashTable:
    """Open-addressing hash table with linear probing and tombstones."""

    def __init__(self) -> None:
        self._capacity = 8
        self._size = 0
        self._table = [_EMPTY] * self._capacity

    @property
    def capacity(self) -> int:
        """Current table capacity."""
        return self._capacity

    def __len__(self) -> int:
        return self._size

    @staticmethod
    def _check_key(key) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be str, got %s" % type(key).__name__)

    def _home(self, key: str) -> int:
        return djb2(key) % self._capacity

    def _find(self, key: str):
        """Slot index of a live entry with this key, or None."""
        cap = self._capacity
        idx = self._home(key)
        for _ in range(cap):
            entry = self._table[idx]
            if entry is _EMPTY:
                return None
            if entry is not _TOMBSTONE and entry[0] == key:
                return idx
            idx = (idx + 1) % cap
        return None

    def put(self, key, value) -> None:
        self._check_key(key)
        cap = self._capacity
        idx = self._home(key)
        first_tomb = None
        for _ in range(cap):
            entry = self._table[idx]
            if entry is _EMPTY:
                break
            if entry is _TOMBSTONE:
                if first_tomb is None:
                    first_tomb = idx
            elif entry[0] == key:
                self._table[idx] = (key, value)
                return None
            idx = (idx + 1) % cap
        else:
            # Table full of live keys/tombstones: unreachable in practice
            # because growth keeps load below 0.7.
            raise RuntimeError("hash table is full")
        target = first_tomb if first_tomb is not None else idx
        self._table[target] = (key, value)
        self._size += 1
        if self._size * 10 > self._capacity * 7:
            self._grow()
        return None

    def get(self, key):
        self._check_key(key)
        idx = self._find(key)
        if idx is None:
            raise KeyError(key)
        return self._table[idx][1]

    def delete(self, key) -> None:
        self._check_key(key)
        idx = self._find(key)
        if idx is None:
            raise KeyError(key)
        self._table[idx] = _TOMBSTONE
        self._size -= 1
        return None

    def __contains__(self, key) -> bool:
        if not isinstance(key, str):
            return False
        return self._find(key) is not None

    def probe_sequence(self, key) -> list:
        """Slot indices from home slot up to the match or the first empty
        slot (inclusive).  Tombstones are skipped but counted in the
        sequence."""
        self._check_key(key)
        cap = self._capacity
        idx = self._home(key)
        seq = []
        for _ in range(cap):
            entry = self._table[idx]
            seq.append(idx)
            if entry is _EMPTY:
                break
            if entry is not _TOMBSTONE and entry[0] == key:
                break
            idx = (idx + 1) % cap
        return seq

    def _grow(self) -> None:
        """Double capacity, rehashing live items in old slot order."""
        old = self._table
        self._capacity *= 2
        self._table = [_EMPTY] * self._capacity
        for entry in old:
            if entry is _EMPTY or entry is _TOMBSTONE:
                continue
            key, value = entry
            idx = self._home(key)
            while self._table[idx] is not _EMPTY:
                idx = (idx + 1) % self._capacity
            self._table[idx] = (key, value)
