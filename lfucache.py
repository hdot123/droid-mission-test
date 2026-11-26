"""lfucache: 最不经常使用（LFU）缓存组件（第五十七轮 D 单）。

淘汰口径（两级钉死）：满容时淘汰**频率最低**者；同频时淘汰**最近最少使用**者。
``get`` 与 ``put``（含更新已有键）均计一次使用（频率 +1 并刷新最近使用时刻），
``in``（``__contains__``）只查在否、不计使用、不改序。
"""

__all__ = ["LFUCache"]


class LFUCache:
    """容量有限的 LFU 缓存。

    - ``capacity < 1`` 抛 ``ValueError``；非 ``int``（含 ``bool``）抛 ``TypeError``。
    - ``get(key)`` 命中返回其值、未命中返回 -1。
    - ``put(key, value)`` 插入或更新；两者均计一次使用。
    - 满容淘汰：频率最低者优先淘汰，同频淘汰最近最少使用者。
    - ``__len__`` 返回现存键数；``__contains__`` 不计使用、不改序。
    """

    def __init__(self, capacity: int):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be int, got %r" % (type(capacity).__name__,))
        if capacity < 1:
            raise ValueError("capacity must be >= 1, got %r" % (capacity,))
        self._capacity = capacity
        # key -> [value, frequency, last_used_tick]
        self._store = {}
        self._tick = 0

    def _touch(self, key) -> None:
        """计一次使用：频率 +1 并刷新最近使用时刻。"""
        self._tick += 1
        entry = self._store[key]
        entry[1] += 1
        entry[2] = self._tick

    def _evict(self) -> None:
        """淘汰频率最低者；同频淘汰最近最少使用者。"""
        victim = None
        victim_freq = None
        victim_tick = None
        for key, (_value, freq, tick) in self._store.items():
            if (
                victim is None
                or freq < victim_freq
                or (freq == victim_freq and tick < victim_tick)
            ):
                victim = key
                victim_freq = freq
                victim_tick = tick
        del self._store[victim]

    def get(self, key):
        """命中返回其值并计一次使用；未命中返回 -1。"""
        if key in self._store:
            self._touch(key)
            return self._store[key][0]
        return -1

    def put(self, key, value) -> None:
        """插入或更新；计一次使用。满容时先淘汰频率最低（同频取最久未用）者。"""
        if key in self._store:
            self._store[key][0] = value
            self._touch(key)
            return
        if len(self._store) >= self._capacity:
            self._evict()
        self._tick += 1
        self._store[key] = [value, 1, self._tick]

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key) -> bool:
        """只查在否：不计使用、不改频率、不改最近序。"""
        return key in self._store
