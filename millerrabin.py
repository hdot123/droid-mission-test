"""millerrabin: 确定性 Miller-Rabin 素性判定（n < 2^32）。

本模块只做单个大整数的素性判定，与素数筛（sieve，枚举生成）和素数计数
（primepi）函数全异。对 n < 2^32 的判定是确定性的：基 {2, 7, 61} 对
n < 4,759,123,141 完备，本题域完全落在其中，不使用随机基、不做概率性
近似。强伪素数 3215031751 能骗过基 2/3/5/7，但必被基 61 判伪。

入参约定：n < 0 或 n >= 2**32 抛 ValueError；非 int（含 bool）抛
TypeError；n < 2 返回 False。
"""

__all__ = ["is_prime"]

_BASES = (2, 7, 61)
_LIMIT = 1 << 32  # 4294967296，判定域上界（不含）


def _is_prime_trial(n):
    """试除法，仅给 < 2 的快速分支和测试参照用。"""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def _miller_rabin_witness(n, a):
    """单基 a 对奇数 n > 2 做强伪素数检测，返回 True 表示 a 是合成见证。"""
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(r - 1):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True


def is_prime(n: int) -> bool:
    """对 0 <= n < 2**32 做确定性 Miller-Rabin 素性判定。

    基 {2, 7, 61} 对 n < 4,759,123,141 完备，故本域内判定确定无误。
    n < 2 返回 False；n < 0 或 n >= 2**32 抛 ValueError；非 int
    （含 bool）抛 TypeError。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int, got %r" % (type(n).__name__,))
    if n < 0 or n >= _LIMIT:
        raise ValueError("n out of range [0, 2**32): %d" % n)
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    if n < 4:
        return True  # n == 3（已排除偶数和 n < 2）
    for a in _BASES:
        if n % a == 0:
            # a 本身整除 n；n 为奇数且 n > a 不可能（a ∈ {2,7,61}，n > 61 时
            # n % a == 0 即合成；n == a 时是素数）。
            return n == a
        if _miller_rabin_witness(n, a):
            return False
    return True
