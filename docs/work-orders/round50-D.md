## 目标

实现三个独立的几何、密码与数论小组件（第五十轮 · 并发 D 单：领班制 v2.7.0+（API 墙 · 根治三批已合 main））。三件彼此独立、无依赖。

## 交付物

convexhull.py、porta.py、primorial.py 与 tests/test_convexhull.py、tests/test_porta.py、tests/test_primorial.py（只新增，不改任何存量文件）。

## 验收标准

验收以合并后全量测试为准；逐模块规格、验收要点与 checks 如下，逐字为准。

一、convexhull.py —— 二维凸包（单调链法）

- `convex_hull(points) -> list[tuple]`：points 为 (x, y) 数值对的 list/tuple；返回凸包顶点，按逆时针排列，起点为 x 最小（x 相同取 y 最小）的点；边上共线点只保留端点；重复点先去重。少于 3 个去重点返回去重排序后的点（0 个返回 []、1 个返回该点、2 个返回两点）。points 非 list/tuple 抛 TypeError；点不是二元组抛 ValueError；坐标非数值抛 TypeError（bool 亦拒）。
- 验收要点：`convex_hull([(0, 0), (1, 0), (1, 1), (0, 1)]) == [(0, 0), (1, 0), (1, 1), (0, 1)]`；`convex_hull([(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]) == [(0, 0), (1, 0), (1, 1), (0, 1)]`；`convex_hull([(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0)]) == [(0, 0), (1, 0), (1, 1), (0, 1)]`；`convex_hull([(0, 0), (2, 0), (1, 2)]) == [(0, 0), (2, 0), (1, 2)]`；`convex_hull([(0, 0), (1, 1), (2, 2), (3, 3)]) == [(0, 0), (3, 3)]`；`convex_hull([(0, 0), (0, 0), (1, 0), (1, 1), (0, 1)]) == [(0, 0), (1, 0), (1, 1), (0, 1)]`；`convex_hull([(0, 0), (2, 0), (3, 1), (1, 3), (-1, 1), (1, 1)]) == [(-1, 1), (0, 0), (2, 0), (3, 1), (1, 3)]`；`convex_hull([(5, 5)]) == [(5, 5)]`；`convex_hull([(1, 2), (3, 4)]) == [(1, 2), (3, 4)]`；`convex_hull([]) == []`；`convex_hull([(0.0, 0.0), (2.5, 0.0), (0.0, 2.5)]) == [(0.0, 0.0), (2.5, 0.0), (0.0, 2.5)]`；`convex_hull("abc")` 抛 TypeError；`convex_hull([(0, 0, 0)])` 抛 ValueError；`convex_hull([(0, "a")])`、`convex_hull([(0, True)])` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_convexhull.py -q`、`python3 -m pytest tests/ -q`

二、porta.py —— Porta 密码（互反表）

- `porta_encrypt(text: str, key: str) -> str`：13 组互反表，密钥字母按对选行：A/B→第 0 行、C/D→第 1 行……Y/Z→第 12 行；每行前半 A–M 映到后半 N–Z（行号 n：A+i → N+((i+n) mod 13)）、后半 N–Z 映回前半（N+i → A+((i-n) mod 13)）。密钥按字母重复使用、只在字母上推进（非字母不消耗密钥位）；明文大写输出、非字母原样保留。密钥须为非空字母，否则抛 ValueError；非 str 输入抛 TypeError。
- `porta_decrypt(text: str, key: str) -> str`：与加密相同（互反密码，加密即解密）。
- 验收要点：`porta_encrypt("HELLO", "A") == "URYYB"`；`porta_encrypt("HELLO", "B") == "URYYB"`；`porta_encrypt("HELLO", "C") == "VSZZA"`；`porta_encrypt("HELLO", "Z") == "TQXXC"`；`porta_encrypt("ATTACKATDAWN", "LEMON") == "SEAUVPPAXTEL"`；`porta_encrypt("THEQUICKBROWNFOX", "ZEBRA") == "HWRIHURXWECHANBL"`；`porta_encrypt("HELLO WORLD", "KEY") == "ZTXQM KJCXV"`；`porta_encrypt("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "M") == "TUVWXYZNOPQRSHIJKLMABCDEFG"`；`porta_decrypt("SEAUVPPAXTEL", "LEMON") == "ATTACKATDAWN"`；`porta_encrypt("", "KEY") == ""`；`porta_encrypt("ABC123", "A") == "NOP123"`；`porta_encrypt("HELLO", "a") == "URYYB"`；往返：`porta_decrypt(porta_encrypt(x, k), k) == x`，(x, k) 取 ("MEETMEATNOON", "SECRET")、("BALLOON", "ZEBRA")、("THE RAIN IN SPAIN", "MONARCHY")；`porta_encrypt("HELLO", "")`、`porta_encrypt("HELLO", "K3Y")` 抛 ValueError；`porta_encrypt(123, "KEY")`、`porta_encrypt("HELLO", 5)` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_porta.py -q`、`python3 -m pytest tests/ -q`

三、primorial.py —— 素数阶乘（前 n 个素数之积）

- `primorial(n: int) -> int`：前 n 个素数之积 p_n#；primorial(0) == 1（空积）。n 须为 ≥0 的 int，否则 n<0 抛 ValueError、非 int 抛 TypeError（bool 亦拒）。
- 验收要点：`primorial(0) == 1`；`primorial(1) == 2`；`primorial(2) == 6`；`primorial(3) == 30`；`primorial(4) == 210`；`primorial(5) == 2310`；`primorial(6) == 30030`；`primorial(7) == 510510`；`primorial(8) == 9699690`；`primorial(9) == 223092870`；`primorial(10) == 6469693230`；`primorial(6) // primorial(5) == 13`；`primorial(-1)` 抛 ValueError；`primorial(3.0)`、`primorial(True)` 抛 TypeError。
- checks（逐字）：`python3 -m pytest tests/test_primorial.py -q`、`python3 -m pytest tests/ -q`

## 约束

只新增上述六个文件；不改任何存量文件；三件实现只用标准库、不互相 import；每个验收要点都要有对应测试用例。
