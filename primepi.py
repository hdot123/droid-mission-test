"""primepi: 素数计数 π(x) 与第 n 个素数（标准库实现）。"""

import math

__all__ = ["primepi", "nthprime"]


def _sieve(limit: int) -> list:
    """返回不超过 limit 的全部素数（埃拉托斯特尼筛法）。"""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            start = i * i
            step = i
            count = (limit - start) // step + 1
            sieve[start : limit + 1 : step] = bytearray(count)
    return [i for i in range(2, limit + 1) if sieve[i]]


def _require_int(value, name: str) -> int:
    """校验入参是非 bool 的整数，否则抛 ValueError。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("%s must be an integer, got %r" % (name, value))
    return value


def primepi(x: int) -> int:
    """返回不超过 x 的素数个数 π(x)。

    x 须为非负整数，否则抛 ValueError（含负数与非整数，如 2.5）。
    """
    _require_int(x, "x")
    if x < 0:
        raise ValueError("x must be non-negative, got %r" % (x,))
    if x < 2:
        return 0
    return len(_sieve(x))


def nthprime(n: int) -> int:
    """返回第 n 个素数（1 起数，nthprime(1) == 2）。

    n 须为正整数，否则抛 ValueError（含 n == 0）。
    """
    _require_int(n, "n")
    if n < 1:
        raise ValueError("n must be a positive integer, got %r" % (n,))
    if n < 6:
        limit = 15
    else:
        log_n = math.log(n)
        limit = int(n * (log_n + math.log(log_n))) + 3
    while True:
        primes = _sieve(limit)
        if len(primes) >= n:
            return primes[n - 1]
        limit *= 2
