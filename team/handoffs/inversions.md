# Handoff: inversions（子单 #936）

## 被要求做什么

执行进程卡 #936（工作单 #928 第58轮 C 单 · inversions 部分），只负责两个新文件：

- `inversions.py` —— 逆序对计数模块；
- `tests/test_inversions.py` —— 对应测试。

规格要点（逐字为准）：

- `count_inversions(seq) -> int`：返回满足 i < j 且 a[i] > a[j] 的下标对个数，**等值不计**（严格大于才计）。
- 入参为列表或元组，元素为 int／float；str、非序列形态、非数值元素（含 bool）一律抛 TypeError。
- 约束：只新增文件、不改任何存量文件、仅用标准库、不与 ipv6fmt／egyptian 互 import。

## 我做了什么

1. 新建 `inversions.py`：
   - 入参校验先行——str/bytes、非 list/tuple 抛 TypeError；元素 bool 或非 int/float 抛 TypeError。
   - 计数用归并排序分治（O(n log n)）：合并时仅当 `left[i] > right[j]` 才累加（代码里以 `left[i] <= right[j]` 走左支体现等值不计），与 O(n²) 逐对暴力计数语义一致。
   - 函数只读入参、不改动调用者列表（内部拷贝后原地归并）。
2. 新建 `tests/test_inversions.py`（18 个用例），覆盖：
   - 全部验收示例：`[]`→0、`[1]`→0、`[1,2,3]`→0、`[3,2,1]`→3、`[3,1,2]`→2、`[2,2,1]`→2（等值不计，断言非 3）、`[5,4,3,2,1]`→10、`[1.5,1.0]`→1（浮点）、`(2,1)`→1（元组）。
   - 全部 TypeError 用例：`'321'`、`321`、`[1,'a']`、`[1,True]`。
   - 性质用例：随机小列（长度 0–12、值 0–6，含列表与元组两种形态、浮点列）与 200 元大列，逐例对照测试文件内独立的 O(n²) 暴力计数 `_brute`，全部逐个一致。
   - 额外：输入不被修改的守护用例。

## 我没有做什么

- 未修改任何存量文件（仅新增上述两个实现/测试文件）。
- 未触碰 `ipv6fmt.py`、`egyptian.py` 及其测试（并发 C 单其他进程负责）。
- 未创建 `team/**` 之外的额外文件，未建 `.github/**`，未 commit/push。
- 未实现 radixsort／排序类功能——本题只计数，不排序。

## 我跑了哪些检查

| 命令 | 结果 |
| --- | --- |
| `python3 -m pytest tests/test_inversions.py -q` | **18 passed** in 0.04s |
| `python3 -m pytest tests/ -q` | **360 passed, 2 skipped** in 21.59s（全量绿；2 个 skip 为存量套件既有跳过，与本单无关） |

两次运行均未在仓库根产生 `verdict.json` / `verdict.md` 等副产物（如有会按要求清理，实际没有出现）。

## 验证者须注意

1. **等值不计是本单的生死线**：`count_inversions([2, 2, 1])` 必须等于 **2** 而非 3；测试 `test_equal_elements_not_counted` 与归并合并条件 `left[i] <= right[j]` 共同钉死该口径。若改成 `left[i] < right[j]` 走右支（即把等值计入），该用例会红。
2. **bool 是 TypeError 不是数值**：`[1, True]` 抛 TypeError（`isinstance(True, int)` 在 Python 为真，必须显式排除）。同理元素校验顺序：先查容器形态（str/非序列），再查元素。
3. **元组与列表同权**：`(2, 1)` → 1；测试同时覆盖两形态。
4. 归并实现会打乱内部拷贝顺序，但**入参列表本身不被修改**（有守护用例）。
5. 范围只含本卡两文件＋两 team 文件；请勿把并发 C 单的 ipv6fmt/egyptian 结果记到本单头上。
