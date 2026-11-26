# Handoff: squeeze（子单 #887，第56轮 C 单之一）

## 请求（Requested）

实现 `squeeze.py` 与 `tests/test_squeeze.py` 两个新文件，覆盖过程卡 #887 的重复段压缩规格：

- `squeeze_chars(text: str) -> str`：任意字符的连续重复段压为一个（大小写敏感）。
- `squeeze_spaces(text: str) -> str`：空白段（`str.isspace` 口径，含制表／换行等）压为单个 ASCII 空格；**不去首尾**——首尾空白段同样压为一个空格保留。
- 非 str 入参两函数均抛 `TypeError`。
- 只删重复、不产出计数（不是 run-length 编码，结果里不得出现计数）。
- 16 个验收要点逐条要有对应测试。

## 做了（Did）

- 新建 `squeeze.py`：两函数均用纯标准库逐字符扫描实现；`squeeze_chars` 用 prev 字符去重，`squeeze_spaces` 用 `str.isspace()` 判空白段并统一输出单个 `" "`，首尾空白照常压缩保留。类型检查在函数入口显式抛 `TypeError`（带函数名与类型名的清晰报错）。
- 新建 `tests/test_squeeze.py`：27 个用例，逐字覆盖 16 个验收要点——要点 1-7（squeeze_chars 各值）、8-13（squeeze_spaces 各值）、14（幂等：chars 7 个代表输入、spaces 8 个代表输入，含首尾空白边缘输入）、15（`squeeze_chars(5)` TypeError）、16（`squeeze_spaces(None)` TypeError）；另加参数化用例，证明两函数对 5 种非 str 输入（int/None/float/bytes/list）均抛 TypeError。
- 未修改任何存量文件；未碰 `team/**` 之外的他人文件（本文件与 `team/status/squeeze.json` 除外）；未 import `powerconv.py` / `kaprekar.py`；三件互不依赖。

## 没做（Did NOT do）

- 未实现 `powerconv.py` / `kaprekar.py`（属 A/B 单，非本单范围）。
- 未编辑、修改或删除任何既有仓库文件；未触碰 `team/**` 或 `.github/**` 中他人拥有的文件。
- 未产出 run-length 计数、未写任何计数进结果。
- 未 commit / push（按工作单要求留给流水线）。

## 检查（Checks）

从仓库根目录逐字运行：

1. `python3 -m pytest tests/test_squeeze.py -q` → **通过**：`27 passed in 0.03s`
2. `python3 -m pytest tests/ -q` → **通过**：`369 passed, 2 skipped in 19.96s`

两个跳过为仓库既有跳过，与本单无关。

## 验证者注意（Validator notes）

- `squeeze_spaces` 的首尾行为是规格明示的：`"  lead" -> " lead"`、`"trail  " -> "trail "`、`"    " -> " "`——**不是**去首尾版，勿按常规 strip 语义误判。
- `squeeze_chars` 大小写敏感：`"aAaA"` 压不动；`"111222111" -> "121"` 是纯去重非计数（RLE 会得 `1^3 2^3 1^3`，本单不得如此）。
- 空白判定用 `str.isspace()`，制表／换行等非 ASCII 空白也归段，段输出统一为 ASCII 空格 `0x20`。
- 幂等测试已含首尾空白边缘输入，若改动实现请保持该性质。
- 测试套件可能在仓库根目录留下 `verdict.json` / `verdict.md` 之类的流水线副产物，非交付物。
