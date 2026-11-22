"""decimaltime: 常规时间与十进制时间互转（第五十二轮并发 C 单新增组件）。

十进制时间定义（钉死）：一日 = 10 十进制时；每十进制时 = 100 十进制分；
每十进制分 = 100 十进制秒；全日 100000 十进制秒对应常规 86400 秒。
所有换算一律截断（向下取整），不四舍五入。

本模块只依赖标准库，不 import 其他组件。
"""

from fractions import Fraction

# 100000 / 86400 约分为 125 / 108（常规秒 -> 十进制秒）；
# 86400 / 100000 约分为 108 / 125（十进制秒 -> 常规秒）。
_TO_DECIMAL_NUM = 125
_TO_DECIMAL_DEN = 108
_FROM_DECIMAL_NUM = 108
_FROM_DECIMAL_DEN = 125


def _floor_scaled(value, numerator, denominator):
    """返回 value * numerator / denominator 的向下取整（有理数精确计算，避免浮点误差）。"""
    frac = value if isinstance(value, Fraction) else Fraction(value)
    return (frac.numerator * numerator) // (frac.denominator * denominator)


def _check_number(value, name):
    """校验入参为数值（int/float，bool 拒）；不满足抛 TypeError。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("%s must be int or float, got %s" % (name, type(value).__name__))


def _check_int(value, name):
    """校验入参为 int（bool 拒）；不满足抛 TypeError。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("%s must be int, got %s" % (name, type(value).__name__))


def to_decimal(h, m, s):
    """把常规 (时, 分, 秒) 换算为十进制 (时, 分, 秒)，截断返回。

    入参须为数值（int/float，bool 拒），非数值抛 TypeError；
    范围 0 <= h < 24、0 <= m < 60、0 <= s < 60，越界抛 ValueError。
    先把当日已过秒数按比例换算为十进制秒、截断，再拆成三段。
    """
    _check_number(h, "h")
    _check_number(m, "m")
    _check_number(s, "s")
    if not 0 <= h < 24:
        raise ValueError("h out of range [0, 24): %r" % (h,))
    if not 0 <= m < 60:
        raise ValueError("m out of range [0, 60): %r" % (m,))
    if not 0 <= s < 60:
        raise ValueError("s out of range [0, 60): %r" % (s,))
    elapsed = h * 3600 + m * 60 + s
    total = _floor_scaled(elapsed, _TO_DECIMAL_NUM, _TO_DECIMAL_DEN)
    decimal_hours, rest = divmod(total, 10000)
    decimal_minutes, decimal_seconds = divmod(rest, 100)
    return (decimal_hours, decimal_minutes, decimal_seconds)


def from_decimal(dh, dm, ds):
    """把十进制 (时, 分, 秒) 换算为常规 (时, 分, 秒)，截断返回。

    入参须为 int（bool 拒），非 int 抛 TypeError；
    范围 0 <= dh < 10、0 <= dm < 100、0 <= ds < 100，越界抛 ValueError。
    逆换算按比例换算为常规秒、截断，再拆成三段。
    """
    _check_int(dh, "dh")
    _check_int(dm, "dm")
    _check_int(ds, "ds")
    if not 0 <= dh < 10:
        raise ValueError("dh out of range [0, 10): %r" % (dh,))
    if not 0 <= dm < 100:
        raise ValueError("dm out of range [0, 100): %r" % (dm,))
    if not 0 <= ds < 100:
        raise ValueError("ds out of range [0, 100): %r" % (ds,))
    total = dh * 10000 + dm * 100 + ds
    seconds = (total * _FROM_DECIMAL_NUM) // _FROM_DECIMAL_DEN
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return (hours, minutes, secs)
