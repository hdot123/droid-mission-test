# Handoff: kmpsearch（子进程卡 #932）

## 请求（work order #927 第58轮 B 单）

实现 KMP 子串搜索组件：`kmpsearch.py` 提供 `find_all(text: str, pattern: str) -> list[int]`，
返回 pattern 在 text 中全部出现的起始下标，**升序、含重叠出现**。模式必须非空，
任一非 str 入参抛 TypeError，空 pattern 抛 ValueError。算法用 KMP（前缀函数 / LPS 表），
不用 `re` 做匹配语义。只新增 `kmpsearch.py` 与 `tests/test_kmpsearch.py` 两个文件，
不改任何存量文件，标准库 only，不 import farey / lensarea。

## 做了什么

- `kmpsearch.py`：实现了 `_lps(pattern)`（经典前缀函数构造 LPS 表）与
  `find_all(text, pattern)`（KMP 扫描）。命中后用 `lps[j-1]` 回退以捕获**重叠**出现
  （例如 `"aaaa"` 找 `"aa"` 返回 `[0, 1, 2]`）。先做入参类型校验（TypeError）、
  再做空 pattern 校验（ValueError），最后 `m > n` 短路返回 `[]`。
- `tests/test_kmpsearch.py`：16 个测试，逐条覆盖验收要点：
  - 重叠出现：`find_all("ababab", "abab") == [0, 2]`、`find_all("aaaa", "aa") == [0, 1, 2]`
  - 常规：`"abcabc"/"abc" == [0, 3]`、`"mississippi"/"issi" == [1, 4]`
  - 边界：无匹配 `[]`、空 text `[]`、单字符 `[0]`、pattern 长于 text `[]`
  - 升序不重复性质
  - 性质测试：2 字母 / 3 字母 / 4 字母随机语料（text 长 0–25、pattern 长 1–5），
    与朴素逐位扫描（`_naive`，含重叠）结果逐个一致
  - 入参契约：空 pattern 抛 ValueError；`find_all(123, "a")`、`find_all("abc", None)`
    及其他非 str 入参抛 TypeError

## 没做什么

- 未触碰 `farey.py`、`lensarea.py` 或任何存量文件（`roman.py`、`legacy_stringkit.py`、
  `README.md`、既有 tests、docs、scripts 等均未改动）。
- 未做任何跨模块 import；仅标准库。
- 未 commit / push（交由 workflow）。
- 未实现词法切分 / 通配匹配语义（本题明确要求全部出现含重叠，与 lexer/glob 不同）。

## 检查（checks）

| 命令 | 结果 |
| --- | --- |
| `python3 -m pytest tests/test_kmpsearch.py -q` | **16 passed** in 0.02s |
| `python3 -m pytest tests/ -q` | **358 passed, 2 skipped** in 19.27s |

全量基线（合并前 main）为 342 passed + 2 skipped；本次新增 16 个测试，
342 + 16 = 358 passed，与观察结果一致。仓库根目录未产生 `verdict.json` / `verdict.md`
等 by-product（已检查，无需清理）。

## 验证者需注意

1. **重叠是硬要求**：`find_all("aaaa", "aa")` 必须为 `[0, 1, 2]`；
   若实现漏掉重叠（如命中后只 `i += m`）验收必不过。
2. **入参顺序**：先校验类型（TypeError），再校验空 pattern（ValueError）。
   `find_all("abc", "")` 应抛 ValueError 而非 TypeError。
3. **返回类型**：始终为 `list[int]`，升序，无重复下标。
4. 性质测试用固定 seed（20261126 / 5858 / 932），可复现。
5. 算法为标准 KMP，未用 `re`；测试对照用朴素扫描 `_naive` 独立实现，
   两者独立，互为交叉验证。
