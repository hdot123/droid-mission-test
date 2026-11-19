"""bloom: 固定长度布隆过滤器（确定性双散列）。

散列函数按题面钉死：h1 为 FNV-1a 32 位，h2 为 djb2 32 位，均按 UTF-8
字节计算；禁用内置 hash()。第 i 个位置为 (h1 + i*h2) % size。
"""

_FNV_OFFSET_BASIS = 2166136261
_FNV_PRIME = 16777619
_DJB2_INITIAL = 5381
_MASK32 = 0xFFFFFFFF


def _fnv1a_32(data: bytes) -> int:
    """FNV-1a 32 位散列：逐字节异或后乘素数，全程 32 位回绕。"""
    h = _FNV_OFFSET_BASIS
    for byte in data:
        h ^= byte
        h = (h * _FNV_PRIME) & _MASK32
    return h


def _djb2_32(data: bytes) -> int:
    """djb2 32 位散列：h = h*33 + byte，32 位回绕。"""
    h = _DJB2_INITIAL
    for byte in data:
        h = ((h * 33) + byte) & _MASK32
    return h


class BloomFilter:
    """定长布隆过滤器。size、k 必须为正 int。"""

    def __init__(self, size: int, k: int):
        if not isinstance(size, int) or isinstance(size, bool):
            raise TypeError("size must be an int")
        if not isinstance(k, int) or isinstance(k, bool):
            raise TypeError("k must be an int")
        if size <= 0:
            raise ValueError("size must be positive")
        if k <= 0:
            raise ValueError("k must be positive")
        self.size = size
        self.k = k
        self._bits = bytearray(size)

    def bit_positions(self, item: str) -> list:
        """返回该字符串去重后排序的位置列表。"""
        if not isinstance(item, str):
            raise TypeError("item must be a str")
        data = item.encode("utf-8")
        h1 = _fnv1a_32(data)
        h2 = _djb2_32(data)
        positions = [(h1 + i * h2) % self.size for i in range(self.k)]
        return sorted(set(positions))

    def add(self, item: str) -> None:
        """将该项的全部位置置位。"""
        for position in self.bit_positions(item):
            self._bits[position] = 1

    def __contains__(self, item: str) -> bool:
        """全部位置均置位返回 True，否则 False。"""
        if not isinstance(item, str):
            raise TypeError("item must be a str")
        return all(self._bits[p] for p in self.bit_positions(item))

    def set_bits(self) -> list:
        """返回全部已置位的位置排序列表。"""
        return sorted(i for i, bit in enumerate(self._bits) if bit)
