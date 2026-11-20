## 目标

实现三个独立的日期、编码与文本小组件（第五十轮 · 并发 C 单：领班制 v2.7.0+（API 墙 · 根治三批已合 main））。三件彼此独立、无依赖。

## 交付物

easter.py、deltaenc.py、isogram.py 与 tests/test_easter.py、tests/test_deltaenc.py、tests/test_isogram.py（只新增，不改任何存量文件）。

## 验收标准

验收以合并后全量测试为准；逐模块规格、验收要点与 checks 如下，逐字为准。

一、easter.py —— 公历复活节（Anonymous Gregorian computus）

- `easter_date(year: int) -> datetime.date`：按 Anonymous Gregorian computus（Meeus/Jones/Butcher 算法）返回该年复活节（周日）的日期。year 须为 1583–4099 的 int，否则超出范围抛 ValueError、非 int 抛 TypeError（bool 亦拒）。
- 验收要点：`easter_date(2024) == date(2024, 3, 31)`；`easter_date(2025) == date(2025, 4, 20)`；`easter_date(2026) == date(2026, 4, 5)`；`easter_date(2023) == date(2023, 4, 9)`；`easter_date(2000) == date(2000, 4, 23)`；`easter_date(1900) == date(1900, 4, 15)`；`easter_date(1999) == date(1999, 4, 4)`；`easter_date(2019) == date(2019, 4, 21)`；`easter_date(2030) == date(2030, 4, 21)`；`easter_date(2100) == date(2100, 3, 28)`；`easter_date(1583) == date(1583, 4, 10)`；`easter_date(4099) == date(4099, 4, 19)`；`easter_date(1582)`、`easter_date(4100)` 抛 ValueError；`easter_date(2026.0)`、`easter_date("2026")`、`easter_date(True)` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_easter.py -q`、`python3 -m pytest tests/ -q`

二、deltaenc.py —— 整数序列差分编码

- `delta_encode(nums: list[int]) -> list[int]`：首元原样、其后存与前一元之差；空表返回空表。nums 须为 list、元素须为 int，否则非 list 或元素非 int 抛 TypeError（bool 元素亦拒）。
- `delta_decode(deltas: list[int]) -> list[int]`：累加还原；空表返回空表。类型规则同上。
- 验收要点：`delta_encode([10, 12, 15, 15, 20]) == [10, 2, 3, 0, 5]`；`delta_decode([10, 2, 3, 0, 5]) == [10, 12, 15, 15, 20]`；`delta_encode([]) == []`；`delta_decode([]) == []`；`delta_encode([7]) == [7]`；`delta_decode([7]) == [7]`；`delta_encode([5, 3, 3, 10]) == [5, -2, 0, 7]`；`delta_decode([5, -2, 0, 7]) == [5, 3, 3, 10]`；`delta_encode([-5, -3, -10]) == [-5, 2, -7]`；`delta_decode([-5, 2, -7]) == [-5, -3, -10]`；`delta_encode([0, 0, 0]) == [0, 0, 0]`；`delta_encode([1000000, 999999, 1000001]) == [1000000, -1, 2]`；往返：`delta_decode(delta_encode(x)) == x`，x 取 [3, 1, 4, 1, 5, 9, 2, 6]、[0]、[-1, -2, -3]、[100, 200, 150, 150, 151]；`delta_encode((1, 2))`、`delta_encode([1, 2.5])`、`delta_encode([1, True])`、`delta_decode("abc")`、`delta_decode([1, 0.5])` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_deltaenc.py -q`、`python3 -m pytest tests/ -q`

三、isogram.py —— 等词判定

- `is_isogram(word: str) -> bool`：不区分大小写、只计 a–z 字母（非字母字符忽略），无重复字母为 True；空串为 True。非 str 输入抛 TypeError。
- `repeated_letters(word: str) -> list[str]`：返回出现多于一次的字母，按字母序排；无重复返回空表。规则与 is_isogram 同。
- 验收要点：`is_isogram("background") == True`；`is_isogram("isogram") == True`；`is_isogram("hello") == False`；`is_isogram("subdermatoglyphic") == True`；`is_isogram("") == True`；`is_isogram("a") == True`；`is_isogram("Apple") == False`；`is_isogram("uncopyrightable") == True`；`is_isogram("a-b") == True`；`is_isogram("abc def") == True`；`is_isogram("noon") == False`；`is_isogram("lumberjack") == True`；`is_isogram("AbC") == True`；`is_isogram("AbA") == False`；`repeated_letters("hello") == ["l"]`；`repeated_letters("banana") == ["a", "n"]`；`repeated_letters("abc") == []`；`repeated_letters("aabbcc") == ["a", "b", "c"]`；`repeated_letters("Mississippi") == ["i", "p", "s"]`；`repeated_letters("") == []`；`is_isogram(123)`、`repeated_letters(None)` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_isogram.py -q`、`python3 -m pytest tests/ -q`

## 约束

只新增上述六个文件；不改任何存量文件；三件实现只用标准库、不互相 import；每个验收要点都要有对应测试用例。
