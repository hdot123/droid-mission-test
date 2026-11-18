## 目标
实现三个独立的古典密码小组件（第四十三轮 · 并发 B 单：领班制 v2.6.5）。三件彼此独立、无依赖。

## 交付物
beaufort.py、affine.py、polybius.py 与 tests/test_beaufort.py、tests/test_affine.py、tests/test_polybius.py（只新增，不改任何存量文件）。

## 验收标准
验收以合并后全量测试为准；逐模块规格、验收要点与 checks 如下，逐字为准。

一、beaufort.py —— Beaufort 密码
- `beaufort(text: str, key: str) -> str`：对字母按 Beaufort 规则 `(key_letter - plain_letter) mod 26` 加密（key 循环、大小写不敏感）；保留原文大小写，非字母原样保留；key 为空串抛 ValueError。
- 验收要点：`beaufort("Hello", "key") == "Danzq"`；`beaufort("ATTACK AT DAWN", "lemon") == "LLTOLB ET LNPR"`；`beaufort("", "k") == ""`；`beaufort("123", "k") == "123"`；`beaufort("Hello, World!", "key") == "Danzq, Cwnnh!"`；对 `"Hello, World!"` 与 key `"key"` 做往返恒等（Beaufort 自逆）；`beaufort("Hi", "")` 抛 ValueError。
- checks（逐字）：`python3 -m pytest tests/test_beaufort.py -q`、`python3 -m pytest tests/ -q`

二、affine.py ——仿射密码（模 26）
- `encode(text: str, a: int, b: int) -> str`：`E(x)=(ax+b) mod 26` 作用于字母；`decode(text: str, a: int, b: int) -> str` 为逆运算；保留大小写，非字母原样；`a` 与 26 不互素时 encode/decode 均抛 ValueError。
- 验收要点：`encode("Affine", 5, 8) == "Ihhwvc"`；`decode("Ihhwvc", 5, 8) == "Affine"`；`encode("abc", 1, 0) == "abc"`；`encode("Hello", 25, 3) == "Ahccl"`；`decode("Ahccl", 25, 3) == "Hello"`；`encode("Hi", 2, 0)` 抛 ValueError；`decode("Hi", 2, 0)` 抛 ValueError；对 `"Secret message"`、`a=7`、`b=11` 做往返恒等。
- checks（逐字）：`python3 -m pytest tests/test_affine.py -q`、`python3 -m pytest tests/ -q`

三、polybius.py —— Polybius 方格（关键字 MONARCHY）
- 5×5 方格由关键字 `MONARCHY` 先填（`J` 视作 `I`），余下字母 `A–Z`（无 `J`）按字母序填满；坐标为 `(行, 列)`，均从 1 起。
- `encode(text: str) -> str`：仅处理字母（大小写不敏感，`J`→`I`），输出坐标对，格式为 `RC`（两位数字）且各对之间以一个空格分隔；无字母时返回空串。
- `decode(text: str) -> str`：由坐标对序列还原为大写字母串；非法数字、奇数长度、坐标出界抛 ValueError。
- 验收要点：`encode("hello") == "22 31 41 41 12"`；`decode("22 31 41 41 12") == "HELLO"`；`encode("Jupiter") == "34 51 42 34 45 31 15"`（`J` 与 `I` 同格）；`encode("") == ""`；`encode("123") == ""`；`decode("99")` 抛 ValueError；对 `"POLYBIUS"` 做往返恒等（`encode` 为 `42 12 41 23 24 34 51 44`）。
- checks（逐字）：`python3 -m pytest tests/test_polybius.py -q`、`python3 -m pytest tests/ -q`

## 约束
只新增上述六个文件；不改任何存量文件；三件实现只用标准库、不互相 import；每个验收要点都要有对应测试用例。