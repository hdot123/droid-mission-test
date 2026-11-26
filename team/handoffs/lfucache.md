# Handoff: lfucache（子单 #915 · 工单 #904 D 单之一）

## 要求（Requested）

实现第五十七轮 D 单中的 LFU 缓存组件，只新增两个文件：`lfucache.py` 与 `tests/test_lfucache.py`，不改任何存量文件。规格要点：

- 类 `LFUCache(capacity: int)`：`capacity < 1` 抛 `ValueError`；非 `int`（含 `bool`，即 `LFUCache(True)`）抛 `TypeError`（`LFUCache(2.0)` 同为 `TypeError`）。
- `get` 命中返回值、未命中返回 -1；`put` 插入或更新；**get 与 put（含更新已有键）均计一次使用**（频率 +1 并刷新最近时刻）。
- 满容淘汰：**频率最低者优先**，同频淘汰**最近最少使用者**（两级口径，是 LFU 不是 LRU）。
- `__len__` 返回现存键数；`__contains__` 只查在否，不计使用、不改序。
- 全部验收要点（官方脚本、同频破平探针、contains 不计使用探针、构造器错误用例）都要有对应测试；只用标准库；不 import asciitable/ngrams。

## 已做（Did）

- 新增 `lfucache.py`：`LFUCache` 实现。内部 `dict` 存 `[value, frequency, last_used_tick]`，单调 tick 做最近使用序；`get`/`put` 命中路径统一走 `_touch`（频率 +1、刷新 tick）；`put` 新键在满容时先 `_evict`（遍历取 freq 最小、同频取 tick 最小者）再插入（新键 freq=1, tick=+1）；`__contains__` 纯查表；构造器先判 `bool`/非 `int` → `TypeError`，再判 `< 1` → `ValueError`（保证 `LFUCache(True)` 是 TypeError、`LFUCache(0)` 是 ValueError）。仅标准库（实际零 import）。
- 新增 `tests/test_lfucache.py`：8 个测试，逐条覆盖全部验收要点——官方脚本全链路、同频破平（a 被淘汰）、contains 多次查不刷新频率/最近序、put 更新计使用、get 未命中无副作用、`__len__`、`LFUCache(0)`/`LFUCache(-2)` 抛 ValueError、`LFUCache(2.0)`/`LFUCache(True)` 抛 TypeError（均用 `pytest.raises`）。

## 未做（Not done）

- 未触碰 `asciitable.py`、`ngrams.py`（其他子单所有）。
- 未修改任何存量文件（`git status` 仅显示本单两个新增文件，另加流水线自带的 `worker-prompt.txt`/`worker-stream.jsonl` 非本单产物）。
- 未创建 `team/` 之外的任何流程文件；未 commit/push。
- 测试跑出的 `verdict.json`/`verdict.md` 若出现已清理（本次运行后未出现）。

## 检查（Checks）

| 命令 | 结果 |
| --- | --- |
| `python3 -m pytest tests/test_lfucache.py -q` | 8 passed in 0.03s |
| `python3 -m pytest tests/ -q` | 350 passed, 2 skipped in 22.13s（exit 0；2 skipped 为存量跳过项） |

## 验证者注意（Validator notes）

- 淘汰口径是两级：先频率、同频才看最近使用；纯 LRU 实现会在官方脚本与同频破平探针上翻车。
- `get` 与 `put`（含更新）都计使用——`test_put_counts_as_use_on_update` 即钉此语义。
- `__contains__` 必须零副作用；`test_contains_does_not_count_as_use` 连续 5 次 `in` 后仍淘汰 a。
- 构造器校验顺序：bool/float → TypeError，0/-2 → ValueError。
- 本单全量基线为 350 passed + 2 skipped（基线 380588c 之上只加了本单文件）。
