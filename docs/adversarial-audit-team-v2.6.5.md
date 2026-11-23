# 领班制试验场对抗式体检报告（droid-mission-test · team v2.6.5）

- **仓库**：<https://github.com/hdot123/droid-mission-test>
- **正式流水线**：`.github/workflows/team.yml`（`Droid Team v2.6.5 (foreman pattern test)`）
- **门控**：`.github/workflows/env-check.yml`（`project_number: 33`）
- **对照通道**：`.github/workflows/droid.yml`（`@droid` 单体）
- **审计时间**：2026-11-18（UTC）
- **审计方式**：只读；基于 GitHub Issues / Comments / Actions Runs / 仓库工作流源码；**未**修改任何工作流或测试行为
- **官方流程定版（权威依据）**：[《开发领班制 · 流程定版》](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e)（空间 live v45，抽屉双写；定版日 2026-11-17；§1–§14 + 第 1–41 轮轮次卡；用户同步核验 71,410 字符完整）。本报告 [§9](#9-对照官方定版的评价2026-11-18) 以该页为裁定口径。
- **Project 33（droid-mission-test-board）**：审计主体（`cursor[bot]` / `GITHUB_TOKEN`）**无法**读取用户级 Project V2（见 [证据 A1](#a1-project-33-与板面字段无法被自动化核对)）；板面结论以工单评论「状态代偿」+ 出题人记账 + 定版 §14「视图层／事实本体」规则交叉验证

---

## 1. 总裁定

这套领班制流水线在约 40+ 轮压测后，**主干能力**（env-check 硬门、领班落计划与子工单、工人并行与证据包、验收员 JSON 裁定、至多一次改计划、收口卡与 PR 闸门）已形成可核对证据链；v2.6.2–v2.6.5 注释中的多项修复在**新 run** 上能看到对应行为。

仍有几类**已用 GitHub 证据坐实**的结构性缺口：

1. **板面与自动化脱节**：workflow 只写评论代偿、不写 Project 字段；env-check 对板面只能 WARN，无法证明 Project #33 与 run 一致（[A1](#a1-project-33-与板面字段无法被自动化核对)）。
2. **母工单 pass 仍 open**：与定版 §13 多轮收口口径一致（「主工单按设计保持 Open，等 PR 合并」），**不是缺陷**；若板面示「已验收」而母工单 open，按定版 §14 层级口径 **错在板面视图**（[A2'](#a2-pass-工单长期-open-与设计一致但板面易误判)）。
3. **验收员 / 工人「会话硬超时」与改计划断路**：`droid exec` 600s 杀进程时 `validate` job 结构性失败，`replan` 因 `needs.validate.result == 'success'` **不触发**，出现「工人与备料全绿、全量 pytest 0，但无裁定、无 PR」的假阴性（[F1](#f1-验收员会话超时-改计划不回退)）。
4. **并发加压下的「死亡账」**：第四十轮五路并发中多笔 failure 与出题人记账「代码全绿、死因在预算」一致（[F1](#f1-验收员会话超时-改计划不回退)、[T1](#t1-第四十轮并发五路)）。
5. **收口卡兜底文案可误导**：工人失败但 prep 已运行时，assemble 合成理由仍写「备料未启动」（[F2](#f2-assemble-兜底理由与真实-job-链不一致)）。
6. **早期 / 中断单证据缺口**：如 [#7](https://github.com/hdot123/droid-mission-test/issues/7) `replan` 失败后**无** `团队状态卡（收口）` 评论（[F3](#f3-工单-7-无收口卡-replan-失败)）。
7. **出题合规机械门禁不足**：与定版 §14 登记表 **A8＝C8**、**补20**（段标题格式门）同源——env-check 只验 `##` 标题行，不验语义与编排合规；第三十五轮首批四 run 曾因无段标题被门拒（[env-check 作废批](https://github.com/hdot123/droid-mission-test/issues/277)）已在定版记账，但 **编排侧 grep 自检尚未 workflow 化**（见 [§9.3](#93-定版写了-github-侧尚未覆盖或仍打架)）。

**测试方案**（定版 §13）已系统覆盖至第 41 轮并建立网关基线、一致计数、并发阶梯；本 Agent 体检侧重 GitHub 可复核链，与定版轮次叙述 **大体一致**，差异见 [§9](#9-对照官方定版的评价2026-11-18)。第 42 轮 GitHub 证据见 [#379–#383](https://github.com/hdot123/droid-mission-test/issues/379)，定版页随 live v45 落档（用户称 **六处起落档同步**；本轮 MCP 回读含 §14 第四十一轮卡与「下轮第四十二轮 4 路」预告，42 轮全文以 Notion 页为准）。

---

## 2. 发现清单（按严重度）

### P0 — 导致误判或证据链断裂

#### F1. 验收员会话超时 → 改计划不回退 {#f1-验收员会话超时-改计划不回退}

| 项 | 内容 |
|---|---|
| 现象 | 工人成功、备料 `pytest` 0，`validator` job `failure` 且未产出 `verdict.json`；`replan` / 二轮链 **skipped**；收口卡 `总判定：**fail**`，说明「验收未产出判定（validate job 结构性失败）」。 |
| 根因（代码） | `validate`/`replan` 条件：`replan` 要求 `needs.validate.result == 'success'`（[team.yml L1283](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L1283)）；`droid exec` 600s 超时（[L1140](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L1140)）。结构性失败 ≠ 业务 `overall!=pass`，改计划不启动。 |
| 证据 | 工单 [#348](https://github.com/hdot123/droid-mission-test/issues/348)；run [44316831033](https://github.com/hdot123/droid-mission-test/actions/runs/44316831033)（jobs：`validator` **failure**，`replan` **skipped**）；收口评论 [issuecomment-6981182938](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6981182938)；出题人记账 [issuecomment-6984203875](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6984203875)（「42 passed…死因在会话级预算」）。并行样本 [#344](https://github.com/hdot123/droid-mission-test/issues/344) run [44316654176](https://github.com/hdot123/droid-mission-test/actions/runs/44316654176) [issuecomment-6984188557](https://github.com/hdot123/droid-mission-test/issues/344#issuecomment-6984188557)。 |

#### A1. Project 33 与板面字段无法被自动化核对 {#a1-project-33-与板面字段无法被自动化核对}

| 项 | 内容 |
|---|---|
| 现象 | env-check 对 `project_number: 33` 持续 ⚠「项目板读不到」；审计侧 `gh project view` / GraphQL `user.projectV2` 均 `NOT_FOUND`。 |
| 影响 | 无法用本次审计自动化验证你曾见的「施工中/阻塞/失败」等 **Project 字段**是否与 run 一致；只能依赖评论「状态代偿」与 [hdot123](https://github.com/hdot123) 手工记账。 |
| 证据 | [#380 env-check](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6986820971) 板面行；[env-check.yml L179–187](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/env-check.yml#L179-L187)；[team.yml 状态代偿说明 L2871](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L2871)。 |

#### F3. 工单 #7 无收口卡（replan 失败） {#f3-工单-7-无收口卡-replan-失败}

| 项 | 内容 |
|---|---|
| 现象 | 第四轮工单 [#7](https://github.com/hdot123/droid-mission-test/issues/7) 仍 `open`；评论有 env-check、派单、备料，但**无** `## 团队状态卡（收口）` bot 评论。 |
| run 链 | [43998961143](https://github.com/hdot123/droid-mission-test/actions/runs/43998961143)：`validate` **success** → `replan` **failure** → `assemble` **failure**；子工单 [#8–#11](https://github.com/hdot123/droid-mission-test/issues/8) 仍 open。 |
| 归因 | 部分失败 run 未向工单帖收口卡（或 assemble 在帖卡前失败），板面/工单列表与终态 run **脱节**。 |
| 证据 | [run jobs](https://github.com/hdot123/droid-mission-test/actions/runs/43998961143)；`gh issue view 7` 无「总判定」命中。 |

### P1 — 误导性状态 / 闭环不全

#### F2. assemble 兜底理由与真实 job 链不一致 {#f2-assemble-兜底理由与真实-job-链不一致}

| 项 | 内容 |
|---|---|
| 现象 | [#72](https://github.com/hdot123/droid-mission-test/issues/72) 收口写「工人 job 失败，**备料未启动**」，但同 run 中 `prep` **success**、备料评论 pytest 0。 |
| 根因（代码） | 无 `verdict.json` 时按链上第一个 `failure` 套用固定文案 `worker → "工人 job 失败，备料未启动"`（[team.yml L2667–L2673](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L2667-L2673)），未考虑 v2.6.3 后「工人红仍备料」路径。 |
| 证据 | 收口 [issuecomment-6946868355](https://github.com/hdot123/droid-mission-test/issues/72#issuecomment-6946868355)；run [44074014028 jobs](https://github.com/hdot123/droid-mission-test/actions/runs/44074014028)；备料评论在同 run。 |
| 历史 | 该 run `head_sha`=`ab02c1d8`（早于 v2.6.3 合并后多次 workflow 重命名）；同 SHA 上 `validator` 为 **skipped**（R15 回归仅能从更新 SHA 证明，见 [V1](#v1-r15-工人失败后验收仍跑)）。 |

#### A2'. pass 工单长期 open（定版内设计，非流水线 bug） {#a2-pass-工单长期-open-与设计一致但板面易误判}

| 项 | 内容 |
|---|---|
| 现象 | 扫描 64 条含 bot「收口」工单：**43 pass / 21 fail**；其中 **25** 条 `总判定：pass` 且 issue 仍 **open**（如 [#380–#383](https://github.com/hdot123/droid-mission-test/issues/380) 第四十二轮）。 |
| 定版 | [§13 第 5–6 轮等](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) 明写「主工单按设计保持 Open」；[§14 2026-11-18 层级口径](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e)：**事实本体 = issue 谱系 + 工件**，板面是视图，对不上时 **错在板**。 |
| 代码 | `assemble` 仅在 PR 成功后关闭 **子工单 + [计划]**（[team.yml L2777–2794](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L2777-L2794)）。 |
| 证据 | [#380 收口 pass + PR #402](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6987056474)；母工单 [state=open](https://github.com/hdot123/droid-mission-test/issues/380)。 |

#### F4. 51 条 `[工序]` 子工单仍 open

| 项 | 内容 |
|---|---|
| 现象 | 含早期 [#9–#11](https://github.com/hdot123/droid-mission-test/issues/9)（工单 #7）、失败轮 [#354–#356](https://github.com/hdot123/droid-mission-test/issues/354)（#344）、[#366–#368](https://github.com/hdot123/droid-mission-test/issues/366)（#348）等。 |
| 归因 | fail 路径明确「子单保持打开」；pass 路径若 PR 成功应关闭——**部分早期/异常 run 未关单**。 |
| 证据 | API 统计 `open [工序]` count=51（审计时点）；对比 [#345 pass 子单 closed](https://github.com/hdot123/droid-mission-test/issues/345) vs [#348 fail 子单 open](https://github.com/hdot123/droid-mission-test/issues/366)。 |

### P2 — 测试与门禁盲区

#### G1. env-check 不验「出题语义合规」

| 项 | 内容 |
|---|---|
| 现象 | 仅检查 OPEN + `## 目标/交付物/验收标准` 标题行（[env-check.yml L154–168](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/env-check.yml#L154-L168)）。 |
| 缺口 | 不拦截：验收区间互斥、并发五路资源争用、工单自矛盾却未标 `CONFLICT`、归因禁令与存量文件冲突等。 |
| 证据 | 埋错轮 [#269](https://github.com/hdot123/droid-mission-test/issues/269) 题面含「归因禁令」— 首轮 lead 失败仍放行 env-check [run 44254645634](https://github.com/hdot123/droid-mission-test/actions/runs/44254645634)。 |

#### G2. 重复点名仅实测 1 次

| 项 | 内容 |
|---|---|
| 现象 | 全库搜索「重复点名」仅 [#18](https://github.com/hdot123/droid-mission-test/issues/18) [issuecomment-6938686986](https://github.com/hdot123/droid-mission-test/issues/18#issuecomment-6938686986)（pass 后二次 `@team-droid` 被挡）。 |
| 缺口 | `duplicate` 检测仅认 **pass** 收口（[team.yml L85–88](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L85-L88)）；fail/blocked 工单重复点名行为未系统回归。 |

#### G3. 仓库 Actions 设置不可见（403）

| 项 | 内容 |
|---|---|
| 证据 | [#380 env-check](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6986820971) ⚠「默认工作流权限 / PR 创建开关」读不到。 |
| 风险 | 若仓级禁止 Actions 开 PR，流水线只能在 run 末期失败，env-check **无法预先 FAIL**。 |

### P3 — 早期历史 / 已部分修复

| ID | 摘要 | 证据 |
|---|---|---|
| H1 | [#1](https://github.com/hdot123/droid-mission-test/issues/1) 组织策略拦模型 + 旧 `|| true` 假绿（出题人记账） | [issuecomment-6915148486](https://github.com/hdot123/droid-mission-test/issues/1#issuecomment-6915148486) |
| H2 | [#2](https://github.com/hdot123/droid-mission-test/issues/2) 备料环境无 pytest → 人工 PASS 机器 FAIL | [issuecomment-6936141308](https://github.com/hdot123/droid-mission-test/issues/2#issuecomment-6936141308) |
| H3 | [#3](https://github.com/hdot123/droid-mission-test/issues/3) 子工序人工记账 PASS、母单 FAIL（pytest） | [issuecomment 人工记账](https://github.com/hdot123/droid-mission-test/issues/3#issuecomment-6936135620)（第三轮根因同 #2） |

---

## 3. 历史修复项核验（v2.6.2–v2.6.5）

| 版本 | 声称修复 | 核验结论 | GitHub 证据 |
|---|---|---|---|
| v2.6.2 R10 | 工人分支 `.../<pid>-r2` 避 ref 锁 | **已实现**（现网分支命名一致） | 代码路径 worker2 checkout；[run 269 改计划](https://github.com/hdot123/droid-mission-test/issues/269#issuecomment-6972168945) v2 链走通 |
| v2.6.3 R15 | 工人失败后 validate 仍跑 | **在新 SHA 上成立**；旧 SHA `ab02c1d8` run 仍见 validate skipped | [#72 @ ab02c1d8 skipped](https://github.com/hdot123/droid-mission-test/actions/runs/44074014028)；[#344 @ 72489aff validate 跑](https://github.com/hdot123/droid-mission-test/actions/runs/44316654176) |
| v2.6.3 | worker 红仍提交 marker 证据 | **已实现** | [team.yml worker 尾步 L640–647](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L640-L647) |
| v2.6.4 A | unattributed_failure → replan | **部分覆盖**；**结构性 validate 失败仍不触发** | [#348](https://github.com/hdot123/droid-mission-test/issues/348) 与 [F1](#f1-验收员会话超时-改计划不回退) |
| v2.6.4 B | 红 checks 不得判 pass | **见验收 JSON 硬规则**（源码）；[#88 改计划回路过](https://github.com/hdot123/droid-mission-test/issues/88) | [issue #88 收口 pass](https://github.com/hdot123/droid-mission-test/issues/88#issuecomment-6953341306) |
| v2.6.4 C | CONFLICT 上卡 | **题应出现**（#72 矛盾题）；收口未展示 conflicts 数组 | 工单 [#72](https://github.com/hdot123/droid-mission-test/issues/72)；收口无 `### 工单层冲突` |
| v2.6.4 D | flips 记录 | **未在本次抽样 fail 卡中看到 flips 行** | 需专轮复验 |
| v2.6.5 R19 | 剥离 `team/` 入 plan | **埋错轮 lead 仍可能失败**（非 team/ 原因未排除） | [44254645634 lead failure](https://github.com/hdot123/droid-mission-test/actions/runs/44254645634/job/134633361663) |
| v2.6.5 | 重复点名（pass） | **成立** | [#18 重复点名](https://github.com/hdot123/droid-mission-test/issues/18#issuecomment-6938686986) |

---

## 4. 各轮结果与证据对照

说明：

- **收口判定**取自 `github-actions[bot]` 的 `## 团队状态卡（收口）` → `总判定：**pass|fail**`（若无 bot 收口则标 **证据不足**）。
- **Run 链接**取自收口内 `candidate-<run_id>` 或计划标题中的 `run <id>`。
- **板面列**：本次 **无法** 直接读取 Project 33 字段（[A1](#a1-project-33-与板面字段无法被自动化核对)）；「不一致/可疑」来自工单 open 状态、子单滞留与出题人记账。

### 4.1 主轮次摘要（第四轮—第四十二轮代表工单）

| 轮次 | 工单 | 收口 | issue 状态 | Team run | 板面/闭环备注 |
|---|---|---|---|---|---|
| 4 | [#7](https://github.com/hdot123/droid-mission-test/issues/7) | **证据不足** | open | [43998961143](https://github.com/hdot123/droid-mission-test/actions/runs/43998961143) fail | replan 红；无收口卡 [F3](#f3-工单-7-无收口卡-replan-失败) |
| 5–28 | [#12](https://github.com/hdot123/droid-mission-test/issues/12)…[#196](https://github.com/hdot123/droid-mission-test/issues/196) | 多数 pass/fail 见工单 | 多 open | 各工单评论内 run | pass 母单多不关闭 [A2](#a2-pass-工单长期-open-与设计一致但板面易误判) |
| 15 矛盾 | [#72](https://github.com/hdot123/droid-mission-test/issues/72) | fail | open | [44074014028](https://github.com/hdot123/droid-mission-test/actions/runs/44074014028) | 兜底文案误导 [F2](#f2-assemble-兜底理由与真实-job-链不一致) |
| 18 探针 | [#88](https://github.com/hdot123/droid-mission-test/issues/88) | pass（v2 改计划） | open | [44117869929](https://github.com/hdot123/droid-mission-test/actions/runs/44117869929) | [改版评论](https://github.com/hdot123/droid-mission-test/issues/88#issuecomment-6953234478) |
| 18 复跑 | [#18](https://github.com/hdot123/droid-mission-test/issues/18) | pass + **重复点名** | open | 首次 pass 后二次 env-check | [重复点名](https://github.com/hdot123/droid-mission-test/issues/18#issuecomment-6938686986) |
| 34 埋错 | [#269](https://github.com/hdot123/droid-mission-test/issues/269) | fail→pass | closed | [44254645634](https://github.com/hdot123/droid-mission-test/actions/runs/44254645634) fail；[44257552040](https://github.com/hdot123/droid-mission-test/actions/runs/44257552040) pass | 首轮 lead 挂 |
| 35 并发×4 | [#277](https://github.com/hdot123/droid-mission-test/issues/277) 等 | A/C/D fail，B pass | 多 open | 见各工单 | 并发死亡样本 |
| 36 | [#299](https://github.com/hdot123/droid-mission-test/issues/299) | fail | open | [44273308109](https://github.com/hdot123/droid-mission-test/actions/runs/44273308109) | |
| 37 | [#305](https://github.com/hdot123/droid-mission-test/issues/305) | pass | closed | [44279960216](https://github.com/hdot123/droid-mission-test/actions/runs/44279960216) | |
| 38 并发×4 | [#312–315](https://github.com/hdot123/droid-mission-test/issues/312) | pass | closed | 各 run 见计划标题 | |
| 39 | [#337](https://github.com/hdot123/droid-mission-test/issues/337) | pass | closed | [44302079110](https://github.com/hdot123/droid-mission-test/actions/runs/44302079110) | |
| 40 并发×5 | [#344](https://github.com/hdot123/droid-mission-test/issues/344) / [#348](https://github.com/hdot123/droid-mission-test/issues/348) | fail | open | [44316654176](https://github.com/hdot123/droid-mission-test/actions/runs/44316654176)、[44316831033](https://github.com/hdot123/droid-mission-test/actions/runs/44316831033) | 出题人记账「工件全绿」[T1](#t1-第四十轮并发五路) |
| 41 | [#373](https://github.com/hdot123/droid-mission-test/issues/373) | pass | closed | [44348063659](https://github.com/hdot123/droid-mission-test/actions/runs/44348063659) | |
| 42 并发×4 | [#380–383](https://github.com/hdot123/droid-mission-test/issues/380) | pass | open | [44363177614](https://github.com/hdot123/droid-mission-test/actions/runs/44363177614) 等 | PR [#401–404](https://github.com/hdot123/droid-mission-test/pulls?q=is%3Apr+team%3A) |

#### T1. 第四十轮并发五路 {#t1-第四十轮并发五路}

| 工单 | 收口 | Run | 一致？ |
|---|---|---|---|
| [A #344](https://github.com/hdot123/droid-mission-test/issues/344) | fail | [44316654176](https://github.com/hdot123/droid-mission-test/actions/runs/44316654176) | 与 [记账](https://github.com/hdot123/droid-mission-test/issues/344#issuecomment-6984188557) 一致（超时） |
| [B #345](https://github.com/hdot123/droid-mission-test/issues/345) | pass | [44316685562](https://github.com/hdot123/droid-mission-test/actions/runs/44316685562) | PR 已开 |
| [C #346](https://github.com/hdot123/droid-mission-test/issues/346) | pass | [44316739517](https://github.com/hdot123/droid-mission-test/actions/runs/44316739517) | |
| [D #347](https://github.com/hdot123/droid-mission-test/issues/347) | pass | [44316784239](https://github.com/hdot123/droid-mission-test/actions/runs/44316784239) | |
| [E #348](https://github.com/hdot123/droid-mission-test/issues/348) | fail | [44316831033](https://github.com/hdot123/droid-mission-test/actions/runs/44316831033) | 与 [记账](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6984203875) 一致 |

### 4.2 早期工单 #1–#6（你提供的板面线索复核）

| Issue | 标题 | GitHub state | 与「板面线索」关系 | 证据 |
|---|---|---|---|---|
| [#1](https://github.com/hdot123/droid-mission-test/issues/1) | calc 小包 | open | 出题人记「阻塞」；非流水线逻辑 bug | [阻塞记账](https://github.com/hdot123/droid-mission-test/issues/1#issuecomment-6915148486) |
| [#2](https://github.com/hdot123/droid-mission-test/issues/2) | 文本工具（旧队） | open | 板面「阻塞」与 pytest 缺失误 FAIL 一致 | [记账](https://github.com/hdot123/droid-mission-test/issues/2#issuecomment-6936141308) |
| [#3](https://github.com/hdot123/droid-mission-test/issues/3) | slugify 子工序 | **closed** | 非「施工中」— 子单已关 | [人工记账](https://github.com/hdot123/droid-mission-test/issues/3#issuecomment-6936135620) |
| [#4](https://github.com/hdot123/droid-mission-test/issues/4) | 计划（#2） | open | 阻塞记账 | [issuecomment-6936147724](https://github.com/hdot123/droid-mission-test/issues/4#issuecomment-6936147724) |
| [#5](https://github.com/hdot123/droid-mission-test/issues/5) | wordcount 子工序 | **closed** | | |
| [#6](https://github.com/hdot123/droid-mission-test/issues/6) | textcase 子工序 | **closed** | | |

**结论**：#3/#5/#6 在 GitHub 上为 **closed**；若 Project 仍示「施工中」，属 **板面未更新** 或字段定义与 issue 状态不同步（**证据不足：缺 Project API**）。

### 4.3 Team workflow 近期结论分布（样本）

最近 100 条 `team.yml` completed runs（审计时点 API）：**success 41 / failure 28 / skipped 31**（含 env-check 失败、重复点名短路、并发下 cancel 等）。

---

## 5. 代表轮时间线（重建）

### 5.1 [#380 第四十二轮 A](https://github.com/hdot123/droid-mission-test/issues/380) — pass

1. 点名 `@team-droid` → workflow [team.yml@main](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml)
2. env-check → [评论](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6986820971)
3. 领班派单 → [计划 #385](https://github.com/hdot123/droid-mission-test/issues/385)；子工单 [#387–389](https://github.com/hdot123/droid-mission-test/issues/387)
4. run [44363177614](https://github.com/hdot123/droid-mission-test/actions/runs/44363177614) success
5. 收口 **pass** → [评论](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6987056474)；PR [#402](https://github.com/hdot123/droid-mission-test/pull/402)

### 5.2 [#348 第四十轮 E](https://github.com/hdot123/droid-mission-test/issues/348) — fail（基础设施）

1. env-check pass → [6980362201](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6980362201)
2. 派单 [计划 #365](https://github.com/hdot123/droid-mission-test/issues/365)；工人 / 备料全绿 → [备料评论](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6980553273)（同 issue 时间线）
3. validator 600s 失败 → run [44316831033](https://github.com/hdot123/droid-mission-test/actions/runs/44316831033)
4. 收口 fail「结构性失败」→ [6981182938](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6981182938)
5. 出题人裁定 **题非根因** → [6984203875](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6984203875)

### 5.3 [#269 第三十四轮埋错](https://github.com/hdot123/droid-mission-test/issues/269) — 回归 pass

1. 首轮 lead fail → [44254645634](https://github.com/hdot123/droid-mission-test/actions/runs/44254645634)；收口「计划未落成」[6971608910](https://github.com/hdot123/droid-mission-test/issues/269#issuecomment-6971608910)
2. 二次点名 → 改计划 v1→v2 [6972168945](https://github.com/hdot123/droid-mission-test/issues/269#issuecomment-6972168945)
3. 终局 pass → [44257552040](https://github.com/hdot123/droid-mission-test/actions/runs/44257552040) [6972303417](https://github.com/hdot123/droid-mission-test/issues/269#issuecomment-6972303417)

---

## 6. 拟议角色「法官cursor」缺口分析 {#6-拟议角色法官cursor-缺口分析}

**触发假设**：仅在评论点名 `法官cursor` 时运行；**审批出题人合规**，不接入领班/工人主链。

### 6.1 能补上的空白（有证据支撑）

| 空白 | 证据 |
|---|---|
| 区分 **pipeline fault vs 出题 fault**（如 #348 全绿但 fail） | [348 记账](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6984203875) |
| 工单模板以外语义：矛盾验收、并发互斥、归因可达性 | [#269 归因禁令](https://github.com/hdot123/droid-mission-test/issues/269)；env-check 不覆盖 [G1](#g1-env-check-不验出题语义合规) |
| 点名 `@team-droid` 之前的**硬门槛**（避免垃圾题消耗 4×worker+validator） | [44254645634 lead 浪费](https://github.com/hdot123/droid-mission-test/actions/runs/44254645634) |
| 为 Project 33 提供**与 run 对齐的裁定字段**（出题合规 Y/N、失败归类） | 板面自动化缺口 [A1](#a1-project-33-与板面字段无法被自动化核对) |
| 对「失败样本留档待裁」给出**结构化标签**（超时/真红/题错/板面陈旧） | [#344 记账](https://github.com/hdot123/droid-mission-test/issues/344#issuecomment-6984188557) |

### 6.2 解不了什么

- Factory 组织策略 / 网关白名单（[#1](https://github.com/hdot123/droid-mission-test/issues/1#issuecomment-6915148486)）
- `droid exec` 600s 硬超时与 validator 无输出（定版 §14 **补10** 已登记多例；修法属 team.yml，非法官角色）
- `GITHUB_TOKEN` 无 Project 写权限 → 法官若无 PAT 同样不能自动改板
- 工人代码质量、领班拆卡、合并 pytest 真红（法官不施工）
- 母工单不关闭（**定版既定**，非法官可改）

### 6.3 在官方定版中的位置（未单独立项）

定版**未**出现「法官cursor」工作流名称；近义机制已存在：

| 定版条目 | 链接锚点 | 与「法官cursor」关系 |
|---|---|---|
| env-check 第一工作流 | [§7](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | 只查 GitHub 侧；与领班/工人链 **硬隔离** |
| 补20 题面段标题格式门 | [§14 · 第三十五轮](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | **编排侧**出题自检，拟议法官的最接近落点 |
| 裁判席 / 对抗审计四席 | [§14 · 2026-11-18 对抗审计](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | 事后多席只读审计，**非** issue 评论点名触发 |
| 层级口径「错的一定是板」 | [§14](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | 法官若只做 **板面／出题合规裁定**，须服从此本体论 |

**结论**：拟议「法官cursor」= 定版 **补20 + A8/C8 编排扩展 + 失败归类评论** 的自动化壳；**不替代** env-check（ secrets/令牌）、**不替代** 裁判席（网关账 + 工件原物）。本次仍不实现。

---

## 7. 风险分类汇总

| 类型 | 含义 | 示例 |
|---|---|---|
| **已证据实现的问题** | 源码 + run/issue 交叉证实 | [F1](#f1-验收员会话超时-改计划不回退)、[F2](#f2-assemble-兜底理由与真实-job-链不一致)、[G1](#g1-env-check-不验出题语义合规)；[A1](#a1-project-33-与板面字段无法被自动化核对) 相对定版 §12(3) 为目标缺口 |
| **定版内设计，非缺陷** | 定版 §13/§14 明示 | [A2'](#a2-pass-工单长期-open-与设计一致但板面易误判) 母工单 open；失败不关单（[#344](https://github.com/hdot123/droid-mission-test/issues/344)） |
| **可能问题（证据不足）** | 推测合理但缺 Project/字段直证 | 自动化无法读 Project 33；早期 #3/#5/#6 **issue 已 closed**（[#3](https://github.com/hdot123/droid-mission-test/issues/3)），若板仍「施工中」则符合定版「错在板」、非本 Agent 可证 |
| **定版已记账、GitHub 仍缺口** | 定版 §14 挂账 / 未活验 | [§9.3](#93-定版写了-github-侧尚未覆盖或仍打架)：`workflow 自动写板面`（§12 第 3 件）、Merge `always()`（补18）、fail 工单重复点名、确定性剥离活验等 |

---

## 8. 附录

### 8.1 并发与 concurrency

- 同工单：`concurrency.group: team-issue-${{ github.event.issue.number }}`，`cancel-in-progress: false`（[team.yml L22–24](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L22-L24)）→ 同 issue 重复触发**排队**不杀旧 run。
- 异工单：env-check 警告在飞 run>1（[#380](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6986820971)）；第四十/四十二轮**多 issue 并行**实测。

### 8.2 受保护路径与 R19

- 计划门禁脚本剥离 `team/**`、拒绝 `.github/**`（[team.yml 注释 v2.6.5](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L3-L4)）；审计未逐卡抓取 strip 日志行，**以代码+埋错轮 lead 失败为间接证据**。

### 8.3 审计方法限制

- 未使用仓库外记账本；结论仅来自 GitHub 可访问对象。
- `cursor[bot]` 无法读取 `users/hdot123/projects/33`；**所有板面字段断言均降级为「可能问题」**，除非 issue 评论明示代偿状态。

---

## 9. 对照官方定版的评价（2026-11-18） {#9-对照官方定版的评价2026-11-18}

**依据**：[《开发领班制 · 流程定版》](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e)（MCP `notion-fetch` 于 2026-11-18T18:15Z 回读全文；用户同步声明 71,410 字符无删节）。**证据链**：定版条文用 Notion 链接；可执行事实仍用 GitHub issue/run/comment。

### 9.1 与原体检报告一致（定版背书）

| 原报告结论 | 定版对应 | GitHub 复核 |
|---|---|---|
| env-check 硬门 → 领班 → 工人 → prep → validate → replan(≤1) → assemble | [§6 工作流结构](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e)、[§8 修复回路](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | [#380 run 44363177614](https://github.com/hdot123/droid-mission-test/actions/runs/44363177614) success |
| 「没料不验收」、证据包五件 | [§8 验收](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | [#348 备料评论](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6980553273) 三工序料齐 |
| env-check 对板 33 / 仓 Actions 设置 ⚠ 边界 | [§7 板面配置](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e)、§14 挂账⑤ | [#380 env-check](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6986820971) |
| duplicate 仅 pass 后挡重复点名 | [§13 第 6 轮](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | [#18 重复点名](https://github.com/hdot123/droid-mission-test/issues/18#issuecomment-6938686986) |
| R15→v2.6.3 工人红仍备料/验收 | [§14 R15](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | [#83 run 44109665167](https://github.com/hdot123/droid-mission-test/actions/runs/44109665167) validate 真跑 |
| 改计划二轮链活验 | [§13 第 10、18 轮](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | [#88 v1→v2](https://github.com/hdot123/droid-mission-test/issues/88#issuecomment-6953234478) |
| 第四十轮 A/E 会话预算死、工件全绿 | [§13 第四十轮](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | [#348](https://github.com/hdot123/droid-mission-test/issues/348#issuecomment-6984203875)、[44316831033](https://github.com/hdot123/droid-mission-test/actions/runs/44316831033) |
| 失败单不关单、板置「失败」 | [§13 第 33、35、40 轮](https://app.notion.com/p/41cf9797e33381db87b5e416baac358e) | [#344](https://github.com/hdot123/droid-mission-test/issues/344) open + [记账](https://github.com/hdot123/droid-mission-test/issues/344#issuecomment-6984188557) |
| 第四十二轮四路并发 pass | 定版 live v45 落档（用户六处同步） | [#380–383 收口 pass](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6987056474)、PR [#401–404](https://github.com/hdot123/droid-mission-test/pull/402) |

### 9.2 被定版修正或补强的表述

| 原报告表述 | 定版修正 | 评价调整 |
|---|---|---|
| 「板面与自动化脱节」似缺陷 | §12 v2 第 3 件 **「workflow 自动写板面」为待落地**；现行 [team.yml 状态代偿评论](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L2871) 为 **过渡实现** | [A1](#a1-project-33-与板面字段无法被自动化核对) 仍为 **实现相对定版目标的缺口**，非「未经文档的意外」 |
| pass 母工单 open「易误判」 | §14：**母工单留 Open 是设计**；板面应对子单/计划/收口 | 降级为 [A2'](#a2-pass-工单长期-open-与设计一致但板面易误判) **运维视图问题**，不是 assemble bug |
| #1–#6 板面「施工中」线索 | §14：**板错 issue 对** | [#3 closed](https://github.com/hdot123/droid-mission-test/issues/3) vs 板面：若仍示施工中 → **板面 stale**（定版口径），非流水线故障 |
| F1「改计划应回退」 | 定版第三十六轮：**补18 采认链断点**——`validate` exec 被杀后 **Merge 步无 `always()`** 致无 `verdict.json`；replan 本就不该在 **结构性 fail** 上触发 | F1 主因应并列：**600s 预算杀（补10）** + **采认链断裂（补18）**；[team.yml L1283](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml#L1283) 条件与设计一致 |
| #72「备料未启动」误导 | 定版第十五轮、第四十轮：**收口合成文案可失实**（R15 历史；round40 记 A 路同错） | [F2](#f2-assemble-兜底理由与真实-job-链不一致) 与定版 **A4/B7 类** 登记一致，v2.6.3 只修了 **停单理由五分支** 未修 worker 首败文案 |
| 「40 轮未测 Project 写回」 | 定版明示 v2 五件中第 3 件 **未完工** | 从「测试遗漏」改为 **定版已知 backlog** |
| 出题合规 | 定版 **A8/C8、补20、补15、补19** 族谱 | [G1](#g1-env-check-不验出题语义合规) 与定版 **一致**，解法方向是 **编排前门** 而非扩大 env-check 语义 |

### 9.3 定版写了、GitHub 证据仍缺口或「打架」 {#93-定版写了-github-侧尚未覆盖或仍打架}

| 定版要求 / 挂账 | 状态 | GitHub / 代码证据 |
|---|---|---|
| §12(3) workflow **自动写** Project 六态 | **未实现** | 仅评论代偿：[#380 收口说明](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6987056474)；env-check 板面 ⚠ |
| §7 env-check 验板字段齐全 | **令牌读不到** | 与 [#380 env-check](https://github.com/hdot123/droid-mission-test/issues/380#issuecomment-6986820971) 一致 |
| §7 仓级「允许 Actions 建 PR」 | **403 不可见** | 同上 WARN；历史 [#1](https://github.com/hdot123/droid-mission-test/issues/1#issuecomment-6915148486) PR 失败 |
| §9 assemble **必贴**收口卡 | **仍有漏贴** | [#7](https://github.com/hdot123/droid-mission-test/issues/7) 无收口（[43998961143](https://github.com/hdot123/droid-mission-test/actions/runs/43998961143)）；定版第四轮已记 v2.3 checkout 修复后，**旧 run 未补卡** |
| 补18 Merge 步 `always()` | **未活验修复** | [#348](https://github.com/hdot123/droid-mission-test/issues/348)：validator fail、无 replan；与定版第三十六轮断点描述一致 |
| fail 工单 duplicate 闸 | **未活验** | 仅 [#18 pass 重复](https://github.com/hdot123/droid-mission-test/issues/18#issuecomment-6938686986) |
| 确定性剥离 team/（R19 v2.6.5） | **代码有、自然样本无** | 定版第二十三轮「零拒收」；埋错首轮 lead 杀：[44254645634](https://github.com/hdot123/droid-mission-test/actions/runs/44254645634) |
| 裁判一致计数 / 网关基线 | **定版内建** | 本 Agent **未**复算网关账；第四十轮一致计数清零与 [#344/#348](https://github.com/hdot123/droid-mission-test/issues/344) fail 一致 |
| 「状态记在 Projects 板面」一句话定义 | **与实现打架（已知过渡）** | 事实源 = issue + 工件（§14）；自动化写板 = backlog |

### 9.4 原报告总裁定 — 定版对照后的总评

1. **流水线本体**：定版 §6–§9 与 GitHub 第四十一、四十二轮样本 **对齐**；v2.6.5 为当前正式线（[team.yml 头注释](https://github.com/hdot123/droid-mission-test/blob/main/.github/workflows/team.yml)）。
2. **仍须工程处置的顶点**（定版已命名）：**补10 会话预算**（validator/lead/worker）、**补18 采认链**、**§12(3) 写板**、**A4 收口贴附可靠性**、**补20 编排前门 workflow 化**。
3. **测试线 vs 生产定版**：定版 §14 明示测试仓 PR 不合并、母工单常 open——**不得以生产板面习惯审计测试仓 issue 状态**。
4. **法官cursor**：见 [§6.3](#63-在官方定版中的位置未单独立项)；定版已有 env-check + 裁判席 + 补20，**缺口在编排时点单与板面自动写回**，非领班/worker 链内角色。

---

*本报告由 Cloud Agent 对抗式只读审计生成；§9 增补对照官方定版，未改动仓库运行中流程。*