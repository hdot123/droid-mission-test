"""错排数（子阶乘）derangement counts !n.

Only the Python standard library is used; this module imports nothing from
bearing.py or paritybit.py (or any other project module).
"""

from __future__ import annotations

__all__ = ["subfactorial", "derangements_upto"]


def _validate_n(n: int) -> int:
    """入参约定（两函数同）：非 int（含 bool）抛 TypeError；n < 0 抛 ValueError。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    return n


def subfactorial(n: int) -> int:
    """Return the derangement count !n (子阶乘), the number of permutations of
    n elements with no fixed point.

    !0 = 1, !1 = 0. Computed with the exact integer recurrence
    !n = (n - 1) * (!(n-1) + !(n-2)) — no floating-point arithmetic anywhere,
    so results are exact integers even for large n.

    Raises:
        TypeError: if n is not an int (bool counts as non-int).
        ValueError: if n < 0.
    """
    _validate_n(n)
    if n <= 1:
        return 1 if n == 0 else 0
    prev_prev, prev = 1, 0  # !0, !1
    for k in range(2, n + 1):
        prev_prev, prev = prev, (k - 1) * (prev + prev_prev)
    return prev


def derangements_upto(n: int) -> list[int]:
    """Return the list [!0, !1, ..., !n], i.e. exactly n + 1 items.

    Shares the exact-integer recurrence and the input contract of
    :func:`subfactorial`.

    Raises:
        TypeError: if n is not an int (bool counts as non-int).
        ValueError: if n < 0.
    """
    _validate_n(n)
    values = [1]  # !0
    if n == 0:
        return values
    values.append(0)  # !1
    for k in range(2, n + 1):
        values.append((k - 1) * (values[k - 1] + values[k - 2]))
    return values
