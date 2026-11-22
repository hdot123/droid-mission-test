"""factorize: 素因数分解工具（第四十三轮 · 并发 C 单）。

只用标准库，不依赖仓库内其它模块。
"""


def prime_factors(n: int) -> list[int]:
    """返回 n 的素因数升序列表（含重复）；n < 2 抛 ValueError。"""
    if n < 2:
        raise ValueError("n must be >= 2: %r" % (n,))
    factors: list[int] = []
    rest = n
    divisor = 2
    while divisor * divisor <= rest:
        while rest % divisor == 0:
            factors.append(divisor)
            rest //= divisor
        divisor += 1
    if rest > 1:
        factors.append(rest)
    return factors


def factor_count(n: int) -> int:
    """返回 n 的素因数个数（计重），即 len(prime_factors(n))；n < 2 抛 ValueError。"""
    return len(prime_factors(n))
