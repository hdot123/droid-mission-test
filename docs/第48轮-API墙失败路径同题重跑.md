# 第四十八轮 · API 墙失败路径同题活验（准备稿）

> **状态**：考题已落 issue，**未点火**。指挥在 main 含 [PR #654](https://github.com/hdot123/droid-mission-test/pull/654)（merge `0fa4987764cfeb95ea04a71dd57341c15cb35b87`）后择机 comment 触发领班。
>
> **禁止**：在本轮计划 / 考题 issue 上评论 `@team-droid`；备考 agent 不得触发 `team.yml`。

## 1. 本轮目的

第 47 轮是 API 墙 v2.7.0 **首轮活验**，四路并发全部未形成可采纳的战役结论，主因是失败路径缺陷 **W-1–W-4**（工人能力与题目难度次之）。上述缺陷已由 PR #654 合入 main；**第 48 轮是同题场景的修复后首轮活验**：

- 场景与第 47 轮 A/B/C/D **对齐**（同一套模块规格与验收要点）；
- 对照第 47 轮 run / PR / issue，验证写板、链同步、工人账本、fail-closed 是否在 **活链** 上闭合；
- 不故意编排工人失败；题目仍是真实的三模块开发任务。

修复说明见 [docs/第47轮-API墙失败路径修复.md](./第47轮-API墙失败路径修复.md)。

## 2. 对照第 47 轮

| 路 | 第 47 轮工单 | 活验 run | 战役 PR | 第 47 轮主要墙观测 |
|----|-------------|----------|---------|-------------------|
| A | [#630](https://github.com/hdot123/droid-mission-test/issues/630) | [44532706766](https://github.com/hdot123/droid-mission-test/actions/runs/44532706766) | [#651](https://github.com/hdot123/droid-mission-test/pull/651) | assemble **写板** 失败（W-1 item 解析 + W-2 closeout schema） |
| B | [#631](https://github.com/hdot123/droid-mission-test/issues/631) | [44532754302](https://github.com/hdot123/droid-mission-test/actions/runs/44532754302) | — | 工人超时零输出；delta **误记 success**（W-4）；链 **summary_code 词汇**（W-3） |
| C | [#632](https://github.com/hdot123/droid-mission-test/issues/632) | [44532812733](https://github.com/hdot123/droid-mission-test/actions/runs/44532812733) | — | 验收 `draft_timeout`；墙 **fail-closed 正确**（对照组，修复未改此路径） |
| D | [#633](https://github.com/hdot123/droid-mission-test/issues/633) | [44532866411](https://github.com/hdot123/droid-mission-test/actions/runs/44532866411) | [#650](https://github.com/hdot123/droid-mission-test/pull/650) | 与 A 类似，死在写板 |

第 47 轮计划：[#629](https://github.com/hdot123/droid-mission-test/issues/629)（**保持打开**，本轮不复用、不关闭）。

## 3. 第 48 轮工单（新 issue）

| 路 | 模块组合 | 第 48 轮工单 | 对照第 47 轮 |
|----|----------|--------------|--------------|
| — | 总计划 | [#655](https://github.com/hdot123/droid-mission-test/issues/655) | [#629](https://github.com/hdot123/droid-mission-test/issues/629) |
| A | trifid／mobius／gasmark | [#656](https://github.com/hdot123/droid-mission-test/issues/656) | #630 |
| B | hashtable／eliasgamma／truncate | [#657](https://github.com/hdot123/droid-mission-test/issues/657) | #631 |
| C | partitions／bifid／rotate2d | [#658](https://github.com/hdot123/droid-mission-test/issues/658) | #632 |
| D | unionfind／bizdays／djb2hash | [#659](https://github.com/hdot123/droid-mission-test/issues/659) | #633 |

## 4. 四路场景与墙观察点

### 4.1 共同前提

- 领班制 **v2.7.0+**（含 #654 失败路径修复）。
- 考题 issue **须挂接 [Projects #33](https://github.com/users/hdot123/projects/33)**（写板前置；字段设计勿改）。
- 唯一墙产物 `foreman-run.json` 贯穿 env-check → lead/workers → validate → assemble。
- **没料不验收**；每路独立 issue，互不替代。

### 4.2 A / D 路（写板 W-1、W-2）

**开发任务**：与第 47 轮 A/D 相同（见各工单正文）。

**活验观察点**：

1. `gh project item-list` 能解析已挂板 item（W-1）；assemble **写板步成功**或失败时 closeout **无非法 null enum**（W-2）。
2. `closeout.project_state_*` / `board_write.outcome` 与 Projects #33 板面一致或为合法失败收口。
3. 若工人交付合并 PR，全量 pytest 绿；墙不得因写板误解析报「未挂板」。

### 4.3 B 路（链同步 W-3、工人账本 W-4）

**开发任务**：与第 47 轮 B 相同。

**活验观察点**：

1. 任一 worker job 为 `failure` / 超时 / 零产出时，`worker-delta.json` 的 `result` **不得为 success**（W-4）。
2. merge 后 `workers.any_failed` 与事实一致；prep 门不被假绿穿透。
3. 链 job `failure` 汇入墙后，`chain_facts.summary_code == failed`（非 GitHub 原生 `failure` 直抄导致 schema 崩，W-3）。

### 4.4 C 路（fail-closed 对照）

**开发任务**：与第 47 轮 C 相同。

**活验观察点**：

1. 若验收器 `draft_timeout` 或等价硬失败，整链 **fail-closed**（lead 不假跑、不采认假绿）。
2. 行为应与第 47 轮 C run 一致或更严，**不得**因 #654 放宽 validator 门。

## 5. 验收标准（战役层）

| 维度 | 通过判据 |
|------|----------|
| 开发 | 各工单正文 checks 全绿；仅新增规定文件 |
| 墙 happy path | 四路均可产出合法 `foreman-run.json` 并 upload；采认链闭合 |
| 墙失败 path | 若再现写板/工人/链失败，W-1–W-4 行为符合 #654 与单测 `test_foreman_wall_failure_paths.py` |
| C 对照 | fail-closed 保持 |
| 运维 | 未动 `PROJECTS_STATE_PAT` / 仓库 secret 定义；未改 Project 字段 |

收官惯例（同第 47 轮计划）：成功单逐单关闭；失败单标注不关单；**本计划 issue 保持打开**。

## 6. 注意事项

1. **不点火**：备考 agent 不评论 `@team-droid`，不启动 `team.yml`。
2. **不污染第 47 轮**：不改 #629–#633；不合并/改写战役结果 PR #498、#500、#650、#651。
3. **并发**：固定 4 路并发；计数从 0/4 起；并发基线仍冻结于第 37/39/41 轮。
4. **证据**：活验后 run id、foreman-run 工件、板面截图写入 `docs/evidence/`（点火后由裁决席补）。

## 7. 建议点火顺序（仅建议，本次不执行）

1. **C** — 最短对照 fail-closed，确认 #654 未误伤 validator 路径。
2. **A** — 写板 happy path（W-1/W-2），模块难度中等。
3. **D** — 与 A 同观察点，复验写板。
4. **B** — 工人与链同步（W-3/W-4），历史上易超时，放末路便于独占排障。

或指挥一次性 **四路并发**（与第 47 轮一致），判读时仍按上表分路对照 W-1–W-4。