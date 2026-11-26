# Handoff: stirling2（子单 #883，工单 #877 B 单）

## 被要求做什么

实现 `stirling2.py` 与 `tests/test_stirling2.py` 两个新文件（只新增，不改任何存量文件）：

- `stirling2(n: int, k: int) -> int`：第二类 Stirling 数 S(n, k)；S(0,0)=1，S(n,0)=0（n>0），k>n 返回 0。
- `stirling2_row(n: int) -> list[int]`：返回 `[S(n,0), …, S(n,n)]` 共 n+1 项。
- 入参约定（两函数同）：n<0 或 k<0 抛 ValueError；非 int（含 bool）抛 TypeError。
- 约束：只用标准库、不 import 其他项目模块、不碰 segdist/htmlescape/任何存量文件；每个验收要点都要有对应测试；逐项比对每个 S(n, k)，不得用行和（Bell 数）凑数捷径。

## 做了什么

- 新建 `stirling2.py`：用递推 `S(i, j) = j * S(i-1, j) + S(i-1, j-1)` 逐行推进（列表从右向左原地更新），`stirling2` 与 `stirling2_row` 共用同一行构造逻辑；`_check_int` 统一做类型（拒绝 bool）与负数校验。
- 新建 `tests/test_stirling2.py`：27 个用例，覆盖全部验收要点——
  - 20 条 `EXACT_VALUES` 参数化逐项断言（含 `stirling2(15,5) == 210766920` 且 `isinstance(..., int)`）；
  - 边界四例（S(0,0)/S(5,0)/S(0,3)/S(3,5)）单列；
  - `stirling2_row(0) == [1]`、`stirling2_row(4) == [0,1,7,6,1]`；
  - 交叉校验：n=0..11 每行逐项与 `stirling2(n,k)` 独立结果比对（不是行和比对）；
  - ValueError 三例、TypeError 三例（含 `stirling2(3, True)`）。

## 没做什么

- 未触碰 `segdist.py`、`htmlescape.py` 及其测试（B 单另外两件由其他进程负责）。
- 未修改任何存量文件；未 commit / push。
- 未在实现里提供或依赖任何 bell/行和捷径接口。

## 跑过的检查与结果

均在仓库根目录执行，全部通过：

1. `python3 -m pytest tests/test_stirling2.py -q` → `27 passed in 0.04s`
2. `python3 -m pytest tests/ -q` → `369 passed, 2 skipped in 21.85s`（EXIT=0；2 个 skip 为存量跳过）

测试运行后仓库根未出现 `verdict.json` / `verdict.md`（已确认并检查）。

## 校验人需注意

- 验收要求"逐项比对、不得用行和捷径"：测试文件中 `test_stirling2_row_matches_individual_values` 是逐项交叉断言，`EXACT_VALUES` 参数化也是逐值断言，无任何行和断言。
- `stirling2(3, True)` 抛 TypeError 依赖 `isinstance(value, bool)` 显式拦截，注意不要"简化"掉。
- `stirling2(0, 0) == 1` 与 `k > n → 0` 两个分支的判断顺序：先 `k > n` 再 `k == 0`，`stirling2(0, 3)` 走前者返回 0，两者均在测试覆盖内。
- 只新增两个交付文件加本单的两个 team 文件，其余文件零改动。
