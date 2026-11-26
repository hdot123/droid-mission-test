# Handoff: justify（子单 #907，工作单 #901 第57轮 A 单之三）

## 请求内容（What was requested）

实现文本两端对齐小组件 `justify.py`，仅新增两个文件：`justify.py` 与 `tests/test_justify.py`。规格（逐字为准）：

- `justify_text(text: str, width: int) -> list[str]`：按空白切词、贪心（first-fit）分行；非末行多词行两端对齐至恰 `width`（空格先均分词间间隙、余数自左逐隙 +1，不得自右或轮转）；末行单空格连接不补齐；仅一词的行不对齐；超长单词独占一行原样保留；空/纯空白文本返回 `[]`。
- 入参：`width < 1` 抛 `ValueError`；非 str 文本／非 int（含 bool）宽度抛 `TypeError`。
- 每条验收要点都要有对应测试用例。
- 只用标准库，不 import 其他项目模块，不碰 contfrac / papersize / 任何存量文件。

## 所做工作（What I did）

1. 新建 `justify.py`：
   - `_check_args`：类型校验（bool 按非 int 拒绝）＋ `width < 1` 抛 `ValueError`；
   - `_distribute`：均分后余数自左逐隙 +1（`divmod`，余数给下标小的间隙）；
   - `_join_justified`：多词行按分配数插空格，恒等于恰 `width`；
   - `justify_text`：split 切词 → 贪心 first-fit 分行（`len(" ".join(current)) + 1 + len(word) <= width`）→ 末行单空格、单词行原样、其余两端对齐。
2. 新建 `tests/test_justify.py`：16 个测试，覆盖全部逐字验收要点：
   - 逐字示例：`16 宽经典例`、`""→[]`、`"   "→[]`、`"hello"`、`"a b c"/3`、超长词 `aaa bbbbbbbbbb cc/5`；
   - 性质：词序保持（多宽度扫描）、非末多词行长度恰 == width（多宽度扫描）、末行单空格（无双空格且等于原词尾拼接）、余数自左 +1（`aa bb cc dd/9 → "aa  bb cc"`）、均分无余数（`ab cd ef longword/16 → "ab     cd     ef"`）；
   - 入参：`width 0/-1 → ValueError`；`text=12`、`width=2.5`、`width=True → TypeError`。

## 未做（What I did not do）

- 未动 `contfrac.py`、`papersize.py`（由并发单负责）。
- 未修改任何存量文件（`git status` 仅显示新增 `justify.py`、`tests/test_justify.py`，另有会话前已存在的 `worker-prompt.txt` / `worker-stream.jsonl` 未动）。
- 未创建 `team-plan.json`；未 commit / push。

## 检查（Checks ran and results）

- `python3 -m pytest tests/test_justify.py -q` → **16 passed**（exit 0）。
- `python3 -m pytest tests/ -q` → **358 passed, 2 skipped**（exit 0；skip 为存量用例，与本单无关）。
- 测试产生的根目录 `verdict.json` / `verdict.md` 已删除（管线副产物，非交付物）。

## 验证者需注意（Validator attention）

- 余数空格方向是本题易错点：`justify_text("aa bb cc dd", 9) == ["aa  bb cc", "dd"]` 证明余数给最左隙（`[2,1]` 而非 `[1,2]`）。
- 分行是贪心 first-fit，不是最优断行；`justify_text("aaa bbbbbbbbbb cc", 5)` 中超长词独占一行且原样保留。
- `isinstance(width, bool)` 必须先于 `isinstance(width, int)` 拒绝，否则 `width=True` 会误过。
- 实现零 import（纯标准库、无项目内 import），符合三件互不依赖约束。
