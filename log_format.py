"""log_format: 把处理后的日志记录格式化回统一的文本行输出。

本模块只负责格式化输出，不负责解析、过滤或统计。
输入的记录由解析模块产出（或测试中手工构造的同形桩对象），
只要求具备 ``timestamp``（``datetime.datetime``）、``level``（str）、
``message``（str）三个属性；本模块不 import 任何其他模块。

输出行格式与解析所用格式完全一致（互为逆操作）：
`2026-11-18 12:03:22 INFO service started`，即「日期 时间 级别 消息」，
级别为 DEBUG/INFO/WARN/ERROR 四档之一，时间戳精确到秒。
"""

from datetime import datetime

__all__ = ["format_record", "format_records"]


def format_record(record) -> str:
    """把单条日志记录格式化为统一格式的一行文本。

    行格式为 `YYYY-MM-DD HH:MM:SS LEVEL 消息`，即「日期 时间 级别 消息」
    依次排列、以单个空格分隔。时间取 ``record.timestamp`` 的年月日时分秒，
    ``record.level`` 与 ``record.message`` 原样拼接：消息中的空格与任何
    字符都逐字保留，不做截断或改写。

    对从格式良好的日志行解析得到的记录，本函数的输出与原始行完全一致
    （格式化是行格式的精确逆操作）。

    参数:
        record: 具备 ``timestamp``、``level``、``message`` 属性的日志记录。

    返回:
        与该记录对应的统一格式日志行（不含行尾换行符）。

    异常:
        AttributeError: 记录缺少上述任一属性。
        TypeError: ``record.timestamp`` 不是 ``datetime.datetime`` 实例。
    """
    if not isinstance(record.timestamp, datetime):
        raise TypeError(
            "record.timestamp must be a datetime.datetime, got "
            f"{type(record.timestamp).__name__}"
        )
    stamp = record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return f"{stamp} {record.level} {record.message}"


def format_records(records) -> list:
    """把一组日志记录批量格式化为日志行列表。

    对 ``records`` 中的每条记录依次调用 :func:`format_record`，
    按原顺序返回等长的行列表，顺序与输入一一对应、不重排、不丢弃。
    输入可以是任意可迭代对象（列表、生成器等）。

    参数:
        records: 可迭代的日志记录序列，每条记录同 :func:`format_record`。

    返回:
        ``list[str]``：与输入记录顺序一致的统一格式日志行列表。

    异常:
        AttributeError / TypeError: 由 :func:`format_record` 透传。
    """
    return [format_record(record) for record in records]
