"""Open-addressing hash table: linear probing with tombstones and growth.

Keys must be ``str``.  Hashing is pinned to djb2 (32-bit): the initial value
is 5381 and each UTF-8 byte updates the running hash as
``h = (h * 33 + byte) mod 2**32``.  The builtin ``hash()`` is never used.
The home slot of a key is ``h mod capacity`` and collisions are resolved
with linear probing (step 1, wrapping around the table).

Standard library only; this module imports nothing from the project.
"""

_MASK32 = 0xFFFFFFFF
_DJB2_INIT = 5381

# Sentinel marking a deleted slot: probing skips it but keeps going.
_TOMBSTONE = object()


def djb2(key: str) -> int:
    """Return the pinned 32-bit djb2 hash of *key* over its UTF-8 bytes."""
    if not isinstance(key, str):
        raise TypeError("key must be str, got %s" % type(key).__name__)
    h = _DJB2_INIT
    for byte in key.encode("utf-8"):
        h = (h * 33 + byte) & _MASK32
    return h


class HashTable:
    """Open-addressing hash table (linear probing + tombstones + growth).

    ``capacity`` is the current slot count (starts at 8), ``size`` counts
    live keys, and ``len(table)`` equals ``size``.
    """

    def __init__(self) -> None:
        self.capacity = 8
        self.size = 0
        self._slots = [None] * self.capacity  # None | _TOMBSTONE | (key, value)

    # -- helpers ---------------------------------------------------------

    @staticmethod
    def _check_key(key) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be str, got %s" % type(key).__name__)

    def _home(self, key: str) -> int:
        return djb2(key) % self.capacity

    @staticmethod
    def _is_live(slot) -> bool:
        return slot is not None and slot is not _TOMBSTONE

    def _rehash(self, new_capacity: int) -> None:
        """Double-and-rehash: reinsert every live item in ascending old slot
        order; tombstones are dropped."""
        live = sorted(
            (
                (idx, slot)
                for idx, slot in enumerate(self._slots)
                if self._is_live(slot)
            ),
            key=lambda item: item[0],
        )
        self._slots = [None] * new_capacity
        self.capacity = new_capacity
        for _, (key, value) in live:
            idx = djb2(key) % new_capacity
            while self._slots[idx] is not None:
                idx = (idx + 1) % new_capacity
            self._slots[idx] = (key, value)

    # -- public API ------------------------------------------------------

    def put(self, key, value) -> None:
        """Insert or update *key*.  Grows (x2) once size*10 > capacity*7."""
        self._check_key(key)
        while True:
            cap = self.capacity
            idx = self._home(key)
            first_tombstone = None
            insert_at = None
            steps = 0
            # Probe to the first empty slot or a matching key, remembering
            # the first tombstone seen on the way.
            while steps < cap:
                slot = self._slots[idx]
                if slot is None:
                    insert_at = (
                        first_tombstone if first_tombstone is not None else idx
                    )
                    break
                if slot is _TOMBSTONE:
                    if first_tombstone is None:
                        first_tombstone = idx
                elif slot[0] == key:
                    self._slots[idx] = (key, value)  # update: size unchanged
                    return
                idx = (idx + 1) % cap
                steps += 1
            if insert_at is None:
                # Full cycle with no empty slot (only reachable through heavy
                # delete churn): rehash to drop tombstones, then retry.
                self._rehash(self.capacity * 2)
                continue
            self._slots[insert_at] = (key, value)
            self.size += 1
            if self.size * 10 > self.capacity * 7:
                self._rehash(self.capacity * 2)
            return

    def get(self, key):
        """Return the value for *key*; raise ``KeyError`` if absent."""
        self._check_key(key)
        cap = self.capacity
        idx = self._home(key)
        steps = 0
        while steps < cap:
            slot = self._slots[idx]
            if slot is None:
                raise KeyError(key)
            if self._is_live(slot) and slot[0] == key:
                return slot[1]
            idx = (idx + 1) % cap  # tombstones are skipped, not stops
            steps += 1
        raise KeyError(key)

    def delete(self, key) -> None:
        """Tombstone *key*'s slot and decrement size; ``KeyError`` if absent."""
        self._check_key(key)
        cap = self.capacity
        idx = self._home(key)
        steps = 0
        while steps < cap:
            slot = self._slots[idx]
            if slot is None:
                raise KeyError(key)
            if self._is_live(slot) and slot[0] == key:
                self._slots[idx] = _TOMBSTONE
                self.size -= 1
                return
            idx = (idx + 1) % cap
            steps += 1
        raise KeyError(key)

    def __contains__(self, key) -> bool:
        if not isinstance(key, str):
            return False
        try:
            self.get(key)
        except KeyError:
            return False
        return True

    def __len__(self) -> int:
        return self.size

    def probe_sequence(self, key) -> list:
        """Slots probed for *key*: from its home slot up to and including the
        matching key or the first empty slot.  Tombstones are included in the
        sequence but do not end the search."""
        self._check_key(key)
        cap = self.capacity
        idx = self._home(key)
        sequence = []
        steps = 0
        while steps < cap:
            sequence.append(idx)
            slot = self._slots[idx]
            if slot is None:
                break
            if self._is_live(slot) and slot[0] == key:
                break
            idx = (idx + 1) % cap
            steps += 1
        return sequence
