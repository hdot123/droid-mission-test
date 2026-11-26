# Handoff: egyptian（埃及分数贪心单位分数展开，难度 L）

## 请求（Requested）

子单 #935 / 工单 #928 第58轮 C 单（池外同构新题 R54，基线 380588c）。只负责三件中的 `egyptian`：

- 新增 `egyptian.py`：`egyptian(p: int, q: int) -> list[int]`，返回正有理数 p/q 的贪心（Sylvester）单位分数展开分母列；每步取 ≤ 当步余数的最大单位分数，减去后约分继续，直到余数为 0。未约分入参先约分（`egyptian(2, 6)` → 按 1/3 展开得 `[3]`）。
- 入参约定：`p < 1` 或 `q < 1` 抛 `ValueError`；非 int（含 `bool`）抛 `TypeError`。
- 约束：只新增 `egyptian.py` 与 `tests/test_egyptian.py` 两文件；不改任何存量文件；只用标准库；不与 `ipv6fmt`/`inversions` 互相 import；与 `fractionx` 等分数四则模块无关、不互引。
- 逐字 checks：`python3 -m pytest tests/test_egyptian.py -q`、`python3 -m pytest tests/ -q`。

## 做了什么（What I did）

- 新建 `egyptian.py`：`egyptian()` 先做 `bool`/`int` 类型校验（`TypeError`），再做 `p >= 1 and q >= 1` 校验（`ValueError`），然后用 `math.gcd` 约分，循环里用整数运算 `d = -(-q // p)`（即 `ceil(q/p)`）取最大单位分数分母，更新 `p, q = p*d - q, q*d` 并每步约分，直到 `p == 0`。纯整数运算，结果分母列由贪心唯一确定。
- 新建 `tests/test_egyptian.py`，覆盖全部验收要点：
  - 九条逐字示例（`1/1`、`1/7`、`2/3`、`3/7`、`4/13`、`5/4`、`7/15`、`3/4`、未约分 `2/6`）各一个断言。
  - ValueError 三例：`(0,3)`、`(1,0)`、`(-1,2)`。
  - TypeError 六例：`(1.5,2)`、`(1,True)`，另加 `(True,2)`、`(1,2.0)`、`("2",3)`、`(1,None)`（防 bool 混入 int 分支、防字符串/None）。
  - 返回类型断言：`list` 且元素为非 bool 的 `int`。
  - 性质扫描 `p ∈ [1,12] × q ∈ [1,30]`（360 组）：(a) `fractions.Fraction` 精确验单位分数之和 `== p/q`；(b) 每步单位分数 ≤ 当步余数且等于 `ceil(q/p)`（贪心最大步检查），最后余数归 0；(c) 与测试内独立的纯整数贪心参考实现 `_ref_greedy` 逐个一致。

## 没做什么（What I did not do）

- 未创建/未改 `ipv6fmt.py`、`inversions.py` 或其测试（属并发 C 单其他子单）。
- 未修改任何存量文件（只新增上述两文件；`egyptian.py` 与 `tests/test_egyptian.py` 是新建）。
- 未创建 `team/**` 之外的流程文件、未动 `.github/**`、未提交未推送（交给工作流）。
- 未做非贪心（任意）单位分数分解——严格按贪心 Sylvester 口径。

## 跑了哪些检查（Checks run）

- `python3 -m pytest tests/test_egyptian.py -q` → **6 passed in 0.03s**
- `python3 -m pytest tests/ -q` → **348 passed, 2 skipped in 21.73s**（两个 skip 是存量套件既有的，非本单引入）

## 验证者需注意（Validator attention）

1. 两个 checks 命令均以仓库根目录运行（`python3 -m pytest ...`，非 `python3 -m unittest`）。
2. 全量套件出现的 `verdict.json`/`verdict.md`（若由流水线测试副作用生成）不是本单交付物，属管道副产品。
3. `egyptian(1, True)` 必须抛 `TypeError`（`bool` 是 `int` 子类，故实现里显式 `isinstance(..., bool)` 拒收）；测试同时覆盖 `(True, 2)`。
4. 未约分入参（`egyptian(2, 6) == [3]`）先约分再展开，结果与 `egyptian(1, 3)` 相同。
5. 贪心唯一性：每步 `d = ceil(q_p)`（实现为 `-(-q // p)`），测试的 (b)(c) 两性质可独立复核贪心口径，非任意分解。
6. 模块只依赖标准库 `math.gcd`；测试依赖标准库 `math`、`fractions` 与 `pytest`。
