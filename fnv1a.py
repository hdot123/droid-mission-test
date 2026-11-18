"""fnv1a: FNV-1a 32 位哈希（第四十三轮 · A 单）。

只使用标准库；本模块不依赖仓库内其他模块。
"""

__all__ = ["fnv1a32"]

_OFFSET_BASIS = 2166136261
_PRIME = 16777619
_MASK32 = 0xFFFFFFFF


def fnv1a32(data: bytes) -> int:
    """计算 FNV-1a 32 位哈希。

    offset basis 2166136261，prime 16777619，无终末异或；
    返回 0–4294967295 的整数。非 bytes 输入抛 TypeError。
    """
    if not isinstance(data, bytes):
        raise TypeError(
            "fnv1a32() expected bytes, got %s" % type(data).__name__
        )
    hash_ = _OFFSET_BASIS
    for byte in data:
        hash_ ^= byte
        hash_ = (hash_ * _PRIME) & _MASK32
    return hash_
