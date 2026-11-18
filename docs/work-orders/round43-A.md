## 目标
实现三个独立的哈希与编解码小组件（第四十三轮 · 并发 A 单：领班制 v2.6.5）。三件彼此独立、无依赖。

## 交付物
fnv1a.py、base58.py、verhoeff.py 与 tests/test_fnv1a.py、tests/test_base58.py、tests/test_verhoeff.py（只新增，不改任何存量文件）。

## 验收标准
验收以合并后全量测试为准；逐模块规格、验收要点与 checks 如下，逐字为准。

一、fnv1a.py —— FNV-1a 32 位哈希
- `fnv1a32(data: bytes) -> int`：FNV-1a 32 位（offset basis 2166136261、prime 16777619、无终末异或），返回 0–4294967295 的整数。非 bytes 输入抛 TypeError。
- 验收要点：`fnv1a32(b"") == 2166136261`；`fnv1a32(b"hello") == 1335831723`；`fnv1a32(b"foobar") == 3214735720`；`fnv1a32(b"123456789") == 3146166556`；`fnv1a32(b"a" * 1000) == 500786573`；`fnv1a32("x")` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_fnv1a.py -q`、`python3 -m pytest tests/ -q`

二、base58.py —— Base58 编解码（字节）
- 字母表（Bitcoin 风格，去 0/O/I/l）：`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz`。
- `b58encode(data: bytes) -> str`：大端字节序转 base58；leading `0x00` 字节各编码为一个前导字符 `1`；空字节串返回空串。
- `b58decode(text: str) -> bytes`：逆运算；空串返回空字节串；含字母表外字符抛 ValueError。
- 验收要点：`b58encode(b"") == ""`；`b58encode(b"\x00") == "1"`；`b58encode(b"hello") == "Cn8eVZg"`；`b58encode(b"\x00\x00\x0f") == "11G"`；`b58decode("Cn8eVZg") == b"hello"`；`b58decode("") == b""`；`b58decode("11G") == b"\x00\x00\x0f"`；`b58decode("0OIl!")` 抛 ValueError；对 `b"hello"`、`b"\x00\x00\x0f"` 做往返恒等。
- checks（逐字）：`python3 -m pytest tests/test_base58.py -q`、`python3 -m pytest tests/ -q`

三、verhoeff.py —— Verhoeff 校验位
- `checksum(digits: str) -> int`：对仅含 `0`–`9` 的十进制串（不含校验位）计算 Verhoeff 校验数字 0–9；空串抛 ValueError；非数字字符抛 ValueError。
- `validate(digits: str) -> bool`：整串（含末位校验位）通过 Verhoeff 校验返回 True，否则 False；空串或非数字字符抛 ValueError。
- 验收要点：`checksum("236") == 3`；`checksum("12345") == 1`；`checksum("042") == 8`；`validate("2363") == True`；`validate("2364") == False`；`validate("123451") == True`；`checksum("")`、`checksum("12a")` 抛 ValueError；`validate("")` 抛 ValueError。
- checks（逐字）：`python3 -m pytest tests/test_verhoeff.py -q`、`python3 -m pytest tests/ -q`

## 约束
只新增上述六个文件；不改任何存量文件；三件实现只用标准库、不互相 import；每个验收要点都要有对应测试用例。