"""daycount360: 30/360 US（NASD）日计数。

days360(start, end) 按 30/360 US（NASD）惯例返回起止日之间的天数。
输入必须是 datetime.date；end < start 抛 ValueError。
调整规则按序钉死（d1、d2 为起止日的日，m、y 同理）：
  ① 若 start 是 2 月的最后一天（平年 2 月 28 日、闰年 2 月 29 日），d1 = 30；
  ② 若 end 是 2 月的最后一天且 start 也是 2 月的最后一天，d2 = 30；
  ③ 若 d1 == 31，d1 = 30；
  ④ 若 d2 == 31 且（经前三条调整后的）d1 == 30，d2 = 30。
天数 = (y2 − y1) × 360 + (m2 − m1) × 30 + (d2 − d1)。
"""

import calendar
from datetime import date


def days360(start, end):
    """返回 start 到 end 的 30/360 US（NASD）天数。

    start、end 须为 datetime.date，非 date 抛 TypeError；end < start 抛 ValueError。
    """
    if not isinstance(start, date) or not isinstance(end, date):
        raise TypeError(
            "days360() arguments must be datetime.date, got %r and %r"
            % (type(start).__name__, type(end).__name__)
        )
    if end < start:
        raise ValueError("end must not be earlier than start: %r < %r" % (end, start))

    y1, m1, d1 = start.year, start.month, start.day
    y2, m2, d2 = end.year, end.month, end.day

    def is_february_end(y, m, d):
        return m == 2 and d == calendar.monthrange(y, 2)[1]

    start_feb_end = is_february_end(y1, m1, d1)
    end_feb_end = is_february_end(y2, m2, d2)

    # ① start 是 2 月最后一天 -> d1 = 30
    if start_feb_end:
        d1 = 30
    # ② end 是 2 月最后一天且 start 也是 2 月最后一天 -> d2 = 30
    if end_feb_end and start_feb_end:
        d2 = 30
    # ③ d1 == 31 -> d1 = 30
    if d1 == 31:
        d1 = 30
    # ④ d2 == 31 且调整后 d1 == 30 -> d2 = 30
    if d2 == 31 and d1 == 30:
        d2 = 30

    return (y2 - y1) * 360 + (m2 - m1) * 30 + (d2 - d1)
