# 第五十轮 · 并发四路工单（R48 顺延题池 · 翻修稿）

| 项 | 内容 |
|---|---|
| 轮次 | **第五十轮**（战役第十轮战役账之第七轮并发，固定 4 路） |
| 题池 | **R48 新题池**（原定第 48 轮；第 47–49 轮 API 墙同题复验占用顺延，本轮首次消耗） |
| 题面溯源 | 与 [第 45 轮计划 #454](https://github.com/hdot123/droid-mission-test/issues/454) 工单 [#455–#458](https://github.com/hdot123/droid-mission-test/issues/455) **验收段落逐字同**（仅轮次标识与流水线版本句改写） |
| 流水线 | `team` v2.7.0+，main 已含写板／失败留痕／预算批一–三（#685、#688、#693） |
| 性质 | **常规模块开发并发活验**（非 47–49 墙修复同题复验） |

## 计划工单草稿（GitHub）

新建计划 issue，建议标题：`[计划] 第五十轮（战役第七轮 · 4 路并发 · R48 题池首轮消耗）`

建议正文：

```markdown
第五十轮：10 轮 × 4 路并发战役的第七轮，固定 4 路。领班制 v2.7.0+。题面为顺延的 R48 新题池（原第 45 轮题面，逐字同）。

- A 单：playfair／crc64／swatchbeats
- B 单：bstree／aliquot／massconv
- C 单：easter／deltaenc／isogram
- D 单：convexhull／porta／primorial

收官后成功单逐单关闭、失败单标注不关单，本计划保持打开。
```

## 四路子工单正文（粘贴用）

| 路 | 建议 Issue 标题 | 正文文件 | 历史对照 |
|---|---|---|---|
| A | `[工单] 第五十轮 A 单：playfair／crc64／swatchbeats` | [round50-A.md](./round50-A.md) | [#455](https://github.com/hdot123/droid-mission-test/issues/455) |
| B | `[工单] 第五十轮 B 单：bstree／aliquot／massconv` | [round50-B.md](./round50-B.md) | [#456](https://github.com/hdot123/droid-mission-test/issues/456) |
| C | `[工单] 第五十轮 C 单：easter／deltaenc／isogram` | [round50-C.md](./round50-C.md) | [#457](https://github.com/hdot123/droid-mission-test/issues/457) |
| D | `[工单] 第五十轮 D 单：convexhull／porta／primorial` | [round50-D.md](./round50-D.md) | [#458](https://github.com/hdot123/droid-mission-test/issues/458) |

## 文件清单（每单 6 个新增文件）

- **A**：`playfair.py`、`crc64.py`、`swatchbeats.py`，`tests/test_playfair.py`、`tests/test_crc64.py`、`tests/test_swatchbeats.py`
- **B**：`bstree.py`、`aliquot.py`、`massconv.py`，`tests/test_bstree.py`、`tests/test_aliquot.py`、`tests/test_massconv.py`
- **C**：`easter.py`、`deltaenc.py`、`isogram.py`，`tests/test_easter.py`、`tests/test_deltaenc.py`、`tests/test_isogram.py`
- **D**：`convexhull.py`、`porta.py`、`primorial.py`，`tests/test_convexhull.py`、`tests/test_porta.py`、`tests/test_primorial.py`

## 合规自查

- 每单含 `## 目标`、`## 交付物`、`## 验收标准`、`## 约束`。
- 只新增文件；题面模块名与第 45 轮一致，与第 43–44 轮及墙活验 47–49 轮模块**无文件名冲突**（main 上尚无上表 12 模块实现文件）。
- 点火纪律：勿在子工单评论 `@team-droid`（由指挥统一点火）。

## 修订记录

- **2026-11-20（Asia/Shanghai）**：由 #455–#458 翻修为本目录 `round50-*.md`；对应轮次总结「R48 题池顺延至第 50 轮」。
