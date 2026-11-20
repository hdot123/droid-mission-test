## 目标

实现三个独立的数据结构、数论与单位小组件（第五十轮 · 并发 B 单：领班制 v2.7.0+（API 墙 · 根治三批已合 main））。三件彼此独立、无依赖。

## 交付物

bstree.py、aliquot.py、massconv.py 与 tests/test_bstree.py、tests/test_aliquot.py、tests/test_massconv.py（只新增，不改任何存量文件）。

## 验收标准

验收以合并后全量测试为准；逐模块规格、验收要点与 checks 如下，逐字为准。

一、bstree.py —— 二叉搜索树

- `class BSTree`：键为 int（bool 亦拒，非 int 抛 TypeError）。`insert(v)`：插入，重复键忽略（长度不变）。`search(v) -> bool`。`delete(v) -> bool`：删到返回 True、无此键返回 False；两子节点者用中序后继替换。`inorder() -> list[int]`：中序遍历（升序）。`__len__`：节点数。`minimum() -> int | None`、`maximum() -> int | None`：空树返回 None。
- 验收要点：依次 insert [5, 3, 8, 1, 4, 7, 9] 后 `inorder() == [1, 3, 4, 5, 7, 8, 9]`、`len == 7`、`minimum() == 1`、`maximum() == 9`、`search(4) == True`、`search(6) == False`；`delete(1) == True` 后 `inorder() == [3, 4, 5, 7, 8, 9]`；`delete(8) == True` 后 `inorder() == [3, 4, 5, 7, 9]`；`delete(5) == True` 后 `inorder() == [3, 4, 7, 9]`；`delete(42) == False`；此时 `len == 4`；再 insert(3) 后 `len` 仍为 4；`minimum() == 3`、`maximum() == 9`；空树 `inorder() == []`、`len == 0`、`minimum() is None`、`maximum() is None`、`search(1) == False`、`delete(1) == False`；单节点树 insert(10) 后 `delete(10) == True`、`inorder() == []`；`insert("a")`、`insert(1.5)`、`insert(True)`、`search("x")` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_bstree.py -q`、`python3 -m pytest tests/ -q`

二、aliquot.py —— 真约数和与亏盈分类

- `aliquot_sum(n: int) -> int`：真约数（不含 n 本身，含 1）之和；n 须为 ≥1 的 int，否则 n<1 抛 ValueError、非 int 抛 TypeError（bool 亦拒）。
- `classify(n: int) -> str`：真约数和等于 n 为 `"perfect"`、大于 n 为 `"abundant"`、小于 n 为 `"deficient"`。
- `aliquot_sequence(n: int, count: int) -> list[int]`：以 n 起始、逐项取真约数和的序列，共 count 项；若某项真约数和为 0 则序列提前结束（不含 0）。count 须为 ≥1 的 int，否则 count<1 抛 ValueError、非 int 抛 TypeError。
- 验收要点：`aliquot_sum(1) == 0`；`aliquot_sum(2) == 1`；`aliquot_sum(6) == 6`；`aliquot_sum(8) == 7`；`aliquot_sum(12) == 16`；`aliquot_sum(28) == 28`；`aliquot_sum(100) == 117`；`aliquot_sum(220) == 284`；`aliquot_sum(284) == 220`；`aliquot_sum(496) == 496`；`classify(6) == "perfect"`；`classify(28) == "perfect"`；`classify(12) == "abundant"`；`classify(8) == "deficient"`；`classify(1) == "deficient"`；`aliquot_sequence(12, 6) == [12, 16, 15, 9, 4, 3]`；`aliquot_sequence(6, 4) == [6, 6, 6, 6]`；`aliquot_sequence(220, 3) == [220, 284, 220]`；`aliquot_sequence(1, 3) == [1]`；`aliquot_sequence(25, 4) == [25, 6, 6, 6]`；`aliquot_sum(0)`、`aliquot_sum(-6)` 抛 ValueError；`aliquot_sum(6.0)`、`aliquot_sum(True)` 抛 TypeError；`aliquot_sequence(6, 0)` 抛 ValueError；`aliquot_sequence(6, 2.5)` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_aliquot.py -q`、`python3 -m pytest tests/ -q`

三、massconv.py —— 质量单位换算

- `mass_convert(value, from_unit: str, to_unit: str) -> float`：以千克为中介换算。单位与千克换算：mg=1e-6、g=1e-3、kg=1、t=1000、oz=0.028349523125、lb=0.45359237、st=6.35029318。浮点结果容差 1e-9。未知单位抛 ValueError；value 非数值抛 TypeError（bool 亦拒）。
- 验收要点：`mass_convert(1, "kg", "g") == 1000.0`；`mass_convert(1, "g", "mg") == 1000.0`（容差）；`mass_convert(1, "t", "kg") == 1000.0`；`mass_convert(1000, "mg", "g") == 1.0`（容差）；`mass_convert(1, "lb", "kg") == 0.45359237`（容差）；`mass_convert(16, "oz", "lb") == 1.0`（容差）；`mass_convert(1, "oz", "g") == 28.349523125`（容差）；`mass_convert(1, "st", "lb") == 14.0`；`mass_convert(1, "st", "kg") == 6.35029318`（容差）；`mass_convert(0, "t", "lb") == 0.0`；`mass_convert(2.5, "kg", "lb") == 5.511556554621939`（容差）；往返：`mass_convert(mass_convert(3.7, "lb", "kg"), "kg", "lb") == 3.7`（容差）；`mass_convert(mass_convert(2, "st", "g"), "g", "st") == 2.0`（容差）；`mass_convert(42, "kg", "kg") == 42.0`；`mass_convert(1, "kg", "slug")`、`mass_convert(1, "slug", "kg")` 抛 ValueError；`mass_convert("1", "kg", "g")`、`mass_convert(True, "kg", "g")` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_massconv.py -q`、`python3 -m pytest tests/ -q`

## 约束

只新增上述六个文件；不改任何存量文件；三件实现只用标准库、不互相 import；每个验收要点都要有对应测试用例。
