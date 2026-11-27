# Handoff: millerrabin（sub-issue #964，工作单 #953 第59轮 C 单）

## 要求（Requested）

实现独立组件 `millerrabin.py` 与 `tests/test_millerrabin.py`（只新增、不改任何存量文件；仅标准库；不 import 兄弟模块）：

- `is_prime(n: int) -> bool`：对 0 ≤ n < 2^32 的**确定性** Miller–Rabin 素性判定，基集 {2, 7, 61}（对 n < 4,759,123,141 完备，覆盖本域）；n < 2 返回 False。
- 入参约定：n < 0 或 n ≥ 2^32 抛 ValueError；非 int（含 bool）抛 TypeError。
- 强伪素数 3215031751 是钉死项：能骗过基 2/3/5/7，必须被基 61 判伪；不得用随机基或缩减基集。
- 每条验收要点都要有对应测试。

## 做了什么（Did）

- 新增 `millerrabin.py`：`is_prime` 用固定基 (2, 7, 61) 逐基做强伪素数检测（`pow(a, d, n)` 平方乘，Python 内建模幂）；先做类型检查（bool 拒绝）→ 范围检查（ValueError）→ n < 2 → False → 偶数分支 → n % a == 0 时返回 `n == a`（n 等于基本身为素数，否则合成）。无随机性，判定确定。
- 新增 `tests/test_millerrabin.py`（18 个测试）：
  - 边界：0/1 为 False、2 为 True、2147483647、4294967291、999999937、104729 为 True、4294967295 为 False；
  - 伪素数锚 parametrize：561 / 1105 / 1729 / 2047 / 41041 / 825265 / 3215031751 均为 False；
  - 专项钉死测试：同一文件内独立重写强伪素数判定，断言 3215031751 对基 2/3/5/7 全部"通过"、对基 61 不通过；
  - 性质一：[0, 3000] 全域与本地试除法逐个一致；
  - 性质二：固定种子 `random.Random(20261127)` 生成 500 个 [0, 10^7) 随机数，与试除法**及**手写平方乘 Miller–Rabin 两路逐个一致（双路交叉）；
  - 入参约定：`is_prime(-3)`、`is_prime(2**32)` 抛 ValueError；`is_prime(7.0)`、`is_prime(True)` 抛 TypeError。

## 没做什么（Not done）

- 未触碰 zarray、abacheck 或任何存量文件；未新增/修改工作单六个文件之外的仓库文件。
- 未 commit / push（按工作单由工作流统一提交）。
- 无概率性路径：不使用随机基、不做多次采样。

## 检查（Checks）

1. `python3 -m pytest tests/test_millerrabin.py -q` → **18 passed in 0.04s**（exit 0）
2. `python3 -m pytest tests/ -q` → **360 passed, 2 skipped in 21.50s**（exit 0）

（2 skipped 为存量 skip，与本单无关。）

## 验证器须注意（Validator notes）

- 基集钉死为 (2, 7, 61) 顺序执行；`3215031751` 的判定路径依赖基 61 —— 若有人把基集缩到 {2, 3, 5, 7} 或改随机基，`test_pseudoprime_anchors_are_composite[3215031751]` 与 `test_3215031751_fools_base_2_3_5_7_but_not_61` 会红。
- `is_prime(4)` 返回 False（走偶数分支），`is_prime(3)` 返回 True（n < 4 分支），已在全域 [0, 3000] 一致性测试覆盖。
- TypeError 先于 ValueError 检查：非 int 输入不会因范围检查而漏判；bool 显式拒绝。
- 测试只用标准库 + pytest；`_miller_rabin_witness`/`_is_prime_trial` 是模块内私有辅助，不被任何兄弟模块引用。
