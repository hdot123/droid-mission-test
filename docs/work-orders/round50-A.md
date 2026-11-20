## 目标

实现三个独立的密码、校验与日期小组件（第五十轮 · 并发 A 单：领班制 v2.7.0+（API 墙 · 根治三批已合 main））。三件彼此独立、无依赖。

## 交付物

playfair.py、crc64.py、swatchbeats.py 与 tests/test_playfair.py、tests/test_crc64.py、tests/test_swatchbeats.py（只新增，不改任何存量文件）。

## 验收标准

验收以合并后全量测试为准；逐模块规格、验收要点与 checks 如下，逐字为准。

一、playfair.py —— Playfair 双字母密码

- `playfair_encrypt(text: str, keyword: str) -> str`：keyword 建 5×5 表——keyword 大写去重（J 并入 I），后接剩余字母（A–Z 去 J）按序排满；明文预处理为大写、J→I、去非字母；按双字母分组，同组字母相同时在第一字母后插 `X`，末尾落单补 `X`。加密规则：同行取右（绕回行首）、同列取下（绕回列首）、矩形对角互换列。空串返回空串。keyword 为空或含非字母抛 ValueError；非 str 输入抛 TypeError。
- `playfair_decrypt(cipher: str, keyword: str) -> str`：逆运算（同行取左、同列取上、矩形互换列）；返回含插入 `X` 与补位 `X` 的制备明文（不剥离）。密文奇数长度抛 ValueError；keyword 规则同上；空串返回空串。
- 验收要点：`playfair_encrypt("HIDETHEGOLDINTHETREESTUMP", "PLAYFAIREXAMPLE") == "BMODZBXDNABEKUDMUIXMMOUVIF"`；`playfair_decrypt("BMODZBXDNABEKUDMUIXMMOUVIF", "PLAYFAIREXAMPLE") == "HIDETHEGOLDINTHETREXESTUMP"`；`playfair_encrypt("INSTRUMENTS", "MONARCHY") == "GATLMZCLRQXA"`；`playfair_decrypt("GATLMZCLRQXA", "MONARCHY") == "INSTRUMENTSX"`；`playfair_encrypt("HELLO", "KEY") == "DBNVMI"`；`playfair_decrypt("DBNVMI", "KEY") == "HELXLO"`；`playfair_encrypt("", "KEY") == ""`；`playfair_decrypt("", "KEY") == ""`；`playfair_encrypt("JUMP", "KEY") == playfair_encrypt("IUMP", "KEY")`；`playfair_decrypt(playfair_encrypt("MEETMEATNOON", "SECRET"), "SECRET") == "MEETMEATNOON"`；`playfair_decrypt(playfair_encrypt("BALLOON", "ZEBRA"), "ZEBRA") == "BALXLOON"`；`playfair_encrypt("HI", "")`、`playfair_encrypt("HI", "K3Y")` 抛 ValueError；`playfair_decrypt("ABC", "KEY")` 抛 ValueError；`playfair_encrypt(123, "KEY")`、`playfair_encrypt("HI", 5)` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_playfair.py -q`、`python3 -m pytest tests/ -q`

二、crc64.py —— CRC-64/XZ（ECMA）

- `crc64(data: bytes) -> int`：CRC-64/XZ：反射多项式 0xC96C5795D7870F42、初值 0xFFFFFFFFFFFFFFFF、异或尾 0xFFFFFFFFFFFFFFFF；返回 0–18446744073709551615 的整数。非 bytes 输入抛 TypeError。
- 验收要点：`crc64(b"") == 0`；`crc64(b"123456789") == 0x995DC9BBDF1939FA`；`crc64(b"hello") == 0x9B1EDAE5DBB937B1`；`crc64(b"abc") == 0x2CD8094A1A277627`；`crc64(b"\x00") == 0x1FADA17364673F59`；`crc64(b"\xff" * 8) == 0xFFFFFFFFFFFFFFFF`；`crc64(b"The quick brown fox jumps over the lazy dog") == 0x5B5EB8C2E54AA1C4`；`crc64("hello")` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_crc64.py -q`、`python3 -m pytest tests/ -q`

三、swatchbeats.py —— Swatch 因特网时间

- `to_beats(hour: int, minute: int, second: int) -> float`：UTC 时分秒换算为 .beats：BMT = UTC+1 小时，beats = BMT 自午夜起秒数 / 86.4，结果保留 2 位小数（round 半偶舍入）。hour 须在 0–23、minute/second 在 0–59，否则抛 ValueError；非 int 输入抛 TypeError（bool 亦拒）。
- `from_beats(beats: float) -> tuple[int, int, int]`：beats 换回 UTC (时, 分, 秒)，秒向下取整。beats 须在 0–1000（不含 1000）内，否则抛 ValueError；非数值输入抛 TypeError。
- 验收要点：`to_beats(0, 0, 0) == 41.67`；`to_beats(12, 0, 0) == 541.67`；`to_beats(23, 0, 0) == 0.0`；`to_beats(6, 30, 0) == 312.5`；`to_beats(18, 0, 0) == 791.67`；`to_beats(23, 59, 59) == 41.66`；`to_beats(1, 0, 0) == 83.33`；`to_beats(9, 15, 30) == 427.43`；`from_beats(41.67) == (0, 0, 0)`；`from_beats(0.0) == (23, 0, 0)`；`from_beats(500.0) == (11, 0, 0)`；`from_beats(541.67) == (12, 0, 0)`；`from_beats(999.99) == (22, 59, 59)`；往返：`to_beats(*from_beats(to_beats(h, m, s)))` 与 `to_beats(h, m, s)` 之差在 0.02 内，(h, m, s) 取 (0, 0, 0)、(5, 45, 30)、(12, 0, 0)、(18, 20, 10)、(23, 59, 0)；`to_beats(24, 0, 0)`、`to_beats(0, 60, 0)`、`to_beats(0, 0, 60)`、`to_beats(-1, 0, 0)` 抛 ValueError；`to_beats(1.5, 0, 0)` 抛 TypeError；`from_beats(1000.0)`、`from_beats(-1.0)` 抛 ValueError；`from_beats("500")` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_swatchbeats.py -q`、`python3 -m pytest tests/ -q`

## 约束

只新增上述六个文件；不改任何存量文件；三件实现只用标准库、不互相 import；每个验收要点都要有对应测试用例。
