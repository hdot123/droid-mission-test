"""log_parser: 把日志行解析成结构化记录（本单的“解析”能力模块）。

支持且仅支持一种行格式：``2026-11-18 12:03:22 INFO service started``，
即「日期(YYYY-MM-DD) 时间(HH:MM:SS) 级别 消息」依次排开。级别只有
DEBUG、INFO、WARN、ERROR 四档。不兼容任何其他日志格式。

格式不对的行不被默默吞掉：解析结果要么是 :class:`LogRecord`，
要么是 :class:`ParseError`，调用方可以明确区分两者。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")
"""允许的日志级别，按顺序（由低到高）。"""

_LEVEL_SET = frozenset(LEVELS)


@dataclass(frozen=True)
class LogRecord:
    """一条格式正确的日志记录。

    Attributes:
        timestamp: 由日期与时间解析出的 ``datetime``。
        level: 日志级别，取值为 :data:`LEVELS` 中之一。
        message: 级别之后的全部文本（首尾空白已去除，内部空白保留）。
    """

    timestamp: datetime
    level: str
    message: str


@dataclass(frozen=True)
class ParseError:
    """解析失败的结果：行不满足要求的格式。

    Attributes:
        line: 原始行（未做任何改写）。
        reason: 失败原因的简短说明。
    """

    line: str
    reason: str


def parse_line(line: str) -> LogRecord | ParseError:
    """解析一行日志。

    成功时返回 :class:`LogRecord`（时间、级别、消息各归其位）；失败时返回
    :class:`ParseError` 并附带原因，绝不静默吞掉坏行。会被判定为
    :class:`ParseError` 的情况包括：

    - 字段数量不对（日期、时间、级别之后没有任何消息文本，或前三个字段不完整）；
    - 日期或时间形状不对（非 ``YYYY-MM-DD`` / ``HH:MM:SS``，或不是真实日期时间）；
    - 级别不是 DEBUG、INFO、WARN、ERROR 之一（如 FATAL、TRACE）。

    空白（如空行、纯空白行）同样视为格式不正确。
    """
    if not isinstance(line, str):
        return ParseError(line=repr(line), reason="line is not a str")

    raw = line.rstrip("\n\r")
    if not raw.strip():
        return ParseError(line=raw, reason="empty line")

    # 形如「日期 时间 级别 消息...」：前三个字段之后是消息（可能含空格）。
    fields = raw.split(None, 3)
    if len(fields) < 3:
        return ParseError(
            line=raw,
            reason="wrong field count: expected 'DATE TIME LEVEL MESSAGE'",
        )

    date_str, time_str, level = fields[0], fields[1], fields[2]
    message = fields[3] if len(fields) == 4 else ""

    try:
        timestamp = datetime.strptime(
            date_str + " " + time_str, "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return ParseError(
            line=raw,
            reason="bad date/time shape: expected YYYY-MM-DD HH:MM:SS",
        )

    if level not in _LEVEL_SET:
        return ParseError(
            line=raw,
            reason=f"unknown level: {level!r} (expected one of {', '.join(LEVELS)})",
        )

    if not message.strip():
        return ParseError(line=raw, reason="missing message after level")

    return LogRecord(timestamp=timestamp, level=level, message=message.strip())


def parse_lines(lines) -> list:
    """按顺序解析多行日志，返回 :class:`LogRecord` 与 :class:`ParseError` 混合的列表。

    ``lines`` 中的每一项都交给 :func:`parse_line`，结果按原顺序收集，
    任何一行都不被丢弃。
    """
    return [parse_line(line) for line in lines]
