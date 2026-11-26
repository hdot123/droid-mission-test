"""decibel: 分贝换算（功率比与振幅比）。

功率量用 10·log10、振幅量用 20·log10，两常数不得混用。
所有入参须为数值（bool 不算数值）；ratio ≤ 0 抛 ValueError。
"""

import math

__all__ = [
    "power_ratio_to_db",
    "db_to_power_ratio",
    "amplitude_ratio_to_db",
    "db_to_amplitude_ratio",
]


def _require_number(value, name):
    """校验入参为数值（拒绝 bool）；否则抛 TypeError。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("%s must be a number, got %r" % (name, value))
    return float(value)


def _require_positive(value, name):
    """校验入参为正数值：非数值抛 TypeError，≤ 0 抛 ValueError。"""
    number = _require_number(value, name)
    if number <= 0:
        raise ValueError("%s must be > 0, got %r" % (name, value))
    return number


def power_ratio_to_db(ratio):
    """功率比转分贝：10·log10(ratio)。ratio ≤ 0 抛 ValueError。"""
    ratio = _require_positive(ratio, "ratio")
    return 10.0 * math.log10(ratio)


def db_to_power_ratio(db):
    """分贝转功率比：10^(db/10)。非数值抛 TypeError。"""
    db = _require_number(db, "db")
    return 10.0 ** (db / 10.0)


def amplitude_ratio_to_db(ratio):
    """振幅比转分贝：20·log10(ratio)。ratio ≤ 0 抛 ValueError。"""
    ratio = _require_positive(ratio, "ratio")
    return 20.0 * math.log10(ratio)


def db_to_amplitude_ratio(db):
    """分贝转振幅比：10^(db/20)。非数值抛 TypeError。"""
    db = _require_number(db, "db")
    return 10.0 ** (db / 20.0)
