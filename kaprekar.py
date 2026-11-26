"""kaprekar: 四位数 Kaprekar 例程（第五十六轮新增组件）。

每步把当前值的四位数字（中间值按 4 位补零参与排序，如 999 的数字按
0、9、9、9 参与排序）降序排成的数减去升序排成的数，直到得到 6174；
轨迹记录整数值（如 999 而非 "0999"）。本例程是数字排序减法，
与 collatz 的 3n+1 规则无关。
"""

_TARGET = 6174


def _check_input(n: int) -> None:
    """入参约定：非 int（含 bool）抛 TypeError；越界或四位全同抛 ValueError。"""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("expected int, got %s" % type(n).__name__)
    if not 1000 <= n <= 9999:
        raise ValueError("out of range: %r" % (n,))
    digits = sorted(str(n))
    if digits[0] == digits[-1]:
        raise ValueError("four identical digits: %r" % (n,))


def _step(n: int) -> int:
    """单步：四位补零后降序数减升序数。"""
    digits = sorted("%04d" % n)
    ascending = int("".join(digits))
    descending = int("".join(reversed(digits)))
    return descending - ascending


def _walk(n: int) -> list[int]:
    """从已校验的起点走到 6174，返回完整轨迹；若出现环抛 RuntimeError。"""
    trajectory = [n]
    seen = {n}
    while n != _TARGET:
        n = _step(n)
        if n in seen:
            raise RuntimeError("kaprekar cycle without reaching 6174: %r" % (n,))
        seen.add(n)
        trajectory.append(n)
    return trajectory


def kaprekar_steps(n: int) -> int:
    """四位数 Kaprekar 例程到达 6174 的步数；6174 本身为 0 步。"""
    _check_input(n)
    return len(_walk(n)) - 1


def kaprekar_trajectory(n: int) -> list[int]:
    """返回含起点与 6174 的全轨迹（记录整数值，如 999 而非 "0999"）。"""
    _check_input(n)
    return _walk(n)
