## 目标
实现三个独立的数论小组件（第四十三轮 · 并发 C 单：领班制 v2.6.5）。三件彼此独立、无依赖。

## 交付物
catalan.py、totient.py、factorize.py 与 tests/test_catalan.py、tests/test_totient.py、tests/test_factorize.py（只新增，不改任何存量文件）。

## 验收标准
验收以合并后全量测试为准；逐模块规格、验收要点与 checks 如下，逐字为准。

一、catalan.py —— 卡特兰数
- `catalan(n: int) -> int`：第 n 个卡特兰数 Cₙ（C₀＝1）；n 为负数抛 ValueError。
- 验收要点：`catalan(0) == 1`；`catalan(1) == 1`；`catalan(2) == 2`；`catalan(3) == 5`；`catalan(4) == 14`；`catalan(5) == 42`；`catalan(10) == 16796`；`catalan(15) == 9694845`；`catalan(-1)` 抛 ValueError。
- checks（逐字）：`python3 -m pytest tests/test_catalan.py -q`、`python3 -m pytest tests/ -q`

二、totient.py —— 欧拉函数 φ
- `totient(n: int) -> int`：欧拉 totient φ(n)；n 小于 1 抛 ValueError。
- 验收要点：`totient(1) == 1`；`totient(9) == 6`；`totient(12) == 4`；`totient(97) == 96`；`totient(100) == 40`；`totient(1_000_000) == 400000`；`totient(0)`、`totient(-5)` 抛 ValueError。
- checks（逐字）：`python3 -m pytest tests/test_totient.py -q`、`python3 -m pytest tests/ -q`

三、factorize.py —— 素因数分解
- `prime_factors(n: int) -> list[int]`：n 的素因数升序列表（含重复）；n 小于 2 抛 ValueError。
- `factor_count(n: int) -> int`：素因数个数（计重，即 `len(prime_factors(n))`）；n 小于 2 抛 ValueError。
- 验收要点：`prime_factors(2) == [2]`；`prime_factors(12) == [2, 2, 3]`；`prime_factors(97) == [97]`；`prime_factors(360) == [2, 2, 2, 3, 3, 5]`；`factor_count(12) == 3`；`factor_count(97) == 1`；`factor_count(360) == 6`；`prime_factors(1)`、`prime_factors(-10)` 抛 ValueError。
- checks（逐字）：`python3 -m pytest tests/test_factorize.py -q`、`python3 -m pytest tests/ -q`

## 约束
只新增上述六个文件；不改任何存量文件；三件实现只用标准库、不互相 import；每个验收要点都要有对应测试用例。