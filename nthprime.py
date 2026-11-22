"""nthprime: 第 n 个素数（1 起计数，第 1 个素数是 2）。

只用标准库。校验规则：n 必须是 int（bool 拒），非 int 抛 TypeError；n < 1 抛 ValueError。
"""


def nth_prime(n: int) -> int:
    """返回第 n 个素数（1-based，第 1 个素数是 2）。

    n 须为 int（bool 拒）；非 int 抛 TypeError；n < 1 抛 ValueError。
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be int, got %s" % type(n).__name__)
    if n < 1:
        raise ValueError("n must be >= 1, got %r" % (n,))
    primes = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes[-1]
