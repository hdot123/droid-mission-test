# 领班制 API 墙 · 零逃逸收口计划

| 字段 | 值 |
|---|---|
| 文档性质 | **可执行施工计划**（下一轮改 #505 实现，非原则重申） |
| 唯一契约 | `ForemanRun` / `foreman-run.v1`（见 `docs/领班制-整面API墙方案.md`） |
| 对照实现 | PR [#505](https://github.com/hdot123/droid-mission-test/pull/505)（`team.yml` v2.7.0） |
| 对照审计 | PR [#506](https://github.com/hdot123/droid-mission-test/pull/506) · `docs/领班制-整面API墙-实现对抗审.md` §8 必改 **I1–I8** |
| 本交付 | **仅增本文档**；不改 workflow / scripts / tests / schema；不 `@team-droid`、不 merge、不开会触发 `team.yml` 的 issue |

---

## 1. 目标与完成定义（DoD）

### 1.1 用户目标

**硬性 API 墙，不允许逃逸**：整条领班链上只有 `ForemanRun` 一种运行状态真相；编排、采认、收口、写板、评论的权威读写字段均在墙上，禁止第二权威（`needs.*.result` 选路径、legacy 工件目录、`steps.*.outcome` 假绿、评论代偿板面、`init_wall` 静默覆盖 L0 等）。

### 1.2 宣称「零逃逸 / 硬性墙」的合入门槛（对 #505 及其后续补丁）

同时具备以下 **全部** 条件后，方可在文档、PR 描述或 release note 中宣称 **硬性 API 墙、不允许逃逸**（并允许 merge 到被视为「墙已生效」的默认分支——**本次计划 PR 不 merge**）：

| # | 门槛 |
|---|---|
| G1 | **I1–I8 全部关闭**（逐项满足本文 §3 完成判据，代码 + 测试 + lint 可查） |
| G2 | **活验 I8 四类场景全部通过**，工件摘要归档于 `docs/` 或 PR 附件（含 run id、关键墙字段快照） |
| G3 | **独立实现对抗审结论为「通过」**（不得为「有条件通过」；复审 PR **仅文档**亦可，须由非实现作者出具） |
| G4 | `pytest tests/test_foreman_wall_contract.py` 全绿；`lint_workflow_foreman.py` 全绿；`foreman-run.v1.schema.json` 与契约一致 |

**未达 G1–G4 任一条**：#506 总判仍成立——对 #505 等同 **驳回级验收**（至多「有条件通过」），**不得** merge 后对外宣称零逃逸。

### 1.3 本计划与 #505 的关系

- 施工对象：**在 #505 分支语义上叠补丁**（可同一 PR 续写或子 PR），**禁止**新建并列 API / 第二契约类型。
- 蓝图不变：`docs/领班制-整面API墙方案.md` 为设计权威；本文把 #506 的 I1–I8 **落地为文件级任务**。

---

## 2. 施工阶段总览

| 阶段 | 范围 | 退出标准 |
|---|---|---|
| **P0** | I1 + I2 + I5 | prep/prep2 门读墙；assemble pick 单轨；validate/validate2 无 adopt/derive 假绿；契约测试扩展覆盖上述三点 |
| **P1** | I3 + I4 + I7 | 墙下载 fail-closed；lead/replan 硬评论 + `closeout.comments` 回写；收口文案去掉板面代偿双轨 |
| **P2** | I6 | 生产 Mission 仓机器门：`foreman_mode=prod` 强制或 CI 拒绝无显式 prod 的宽口径 plan |
| **P3** | I8 | 四类活验 run 完成，证据入库 |
| **P4** | 独立对抗审复审 | 新/更新的 `docs/领班制-整面API墙-实现对抗审.md`（或续篇）总判 **通过** |

**依赖顺序**：P0 → P1 → P2 可部分并行；**P3 必须在 P0–P2 合并候选之后**；P4 在 P3 之后。

---

## 3. 必改项 I1–I8（逐条施工单）

### I1 · prep / prep2 门读墙 `completed_pids`（P1-5 / W1）

| 项 | 内容 |
|---|---|
| **现状（#506）** | `foreman_run_lib.prep_should_run()` 与 `tests/test_foreman_wall_contract.py::test_prep_gate_completed_pids` **已有**；`team.yml` **prep** job `if` 仍绑 `needs.worker.result == success \|\| failure`（约 L768–771），**未**读 `workers.completed_pids`。matrix 全 cancelled 而 merge job 已写 `completed_pids` 时，prep **错误 skip**。#506 §8 I1。 |
| **要改什么** | 1. **prep**、**prep2** 的 **job 级 `if` 无法直接读 JSON**，须在 `needs` 中增加 **墙投影 job** 或 **merge job 的 output**（推荐：扩展 `workers-wall-merge` / `workers2-wall-merge` 尾步，调用 `prep_should_run` 写 `outputs.should_run`）。2. prep job `if` 改为：`!cancelled() && needs.lead.outputs.duplicate != 'true' && needs.workers-wall-merge.outputs.prep_should_run == 'true'`（prep2 对称用 `workers2-wall-merge` + replan 成功门）。3. **禁止**用 `needs.worker.result` 作为 prep 是否运行的唯一条件。 |
| **涉及文件** | `.github/workflows/team.yml`：`workers-wall-merge`（L722 一带）、`prep`（L765–771）、`workers2-wall-merge`（L2149）、`prep2`（L2183–2188）；`scripts/team/foreman_run_lib.py`（`prep_should_run`，L266–268）；`scripts/team/merge_worker_deltas.py`（保证 `completed_pids` 并集）。 |
| **机器门 / 测试** | 扩展 `test_prep_gate_completed_pids`；新增 workflow 结构测试或 snapshot：grep 确认 prep `if` 不含裸 `needs.worker.result` 作为唯一门；可选 `scripts/team/lint_workflow_foreman.py` 规则。 |
| **完成判据** | 墙内 `workers.completed_pids` 非空且 lead 未 duplicate → prep **started**；全 cancelled → prep **skipped**；与 #506 I1 一致。活验场景「45B 单 worker cancelled」见 I8。 |
| **回归风险** | 过早跑 prep（completed 误判）→ validate 无证据；过晚 skip → 与现网相同。merge job 必须先于 prep 且墙 artifact 必达。 |

---

### I2 · assemble 仅以 `foreman-run.json` 为权威（W1 / 蓝图 §4）

| 项 | 内容 |
|---|---|
| **现状（#506）** | assemble **Download ForemanRun wall** `continue-on-error: true`（L2967–2971）；**Pick final verdict**（L2973–3066）**优先**扫描 `dl/team-verdict2-*`、`team-verdict-*` 目录找 `verdict.json`，墙仅在 **无 verdict 文件** 时参与 `chain_facts` fallback；仍注入 `needs.*_RESULT`（L2976–2983）。pick 无 verdict 时 chain 与墙 `chain` **可能不一致**。#506 §8 I2、§3 同一产物。 |
| **要改什么** | 1. assemble **下载墙**：去掉 `continue-on-error`；无 `foreman-run.json` → **job fail**（与 I3 同改）。2. 新增或改写 pick 步：**主路径**读墙 `validation`（round1/round2）、`replan_gate`、`artifacts.*.complete`、`round2` 子树，决定 `picked_round`、`overall`、证据 tar 路径（来自墙上记录的 artifact 名或规范路径）；**禁止**在墙完整且 `artifacts.team-verdict-* .complete==true` 时仍仅信 `dl/` 扫描。3. legacy 目录扫描 **仅**作墙字段缺失时的 **显式 degrade**（写 `closeout.run_must_fail` + 固定文案），且须 lint 禁止生产路径依赖。4. `needs.*_RESULT` **仅**用于 GitHub 展示或 `chain_facts` 审计镜像，**不得**改变 verdict 业务结论。 |
| **涉及文件** | `.github/workflows/team.yml` assemble job（L2950 起）；`scripts/team/assemble_chain_facts.py`；可选新脚本 `scripts/team/pick_verdict_from_wall.py`（**patch 墙，不新开契约**）。 |
| **机器门 / 测试** | 单测：给定墙 JSON + 空 `dl/` → pick 输出与墙 `validation.overall` 一致；契约测试：半套 artifact `complete=false` 不得 pick 出 pass。 |
| **完成判据** | 墙完整时 pick **不读** `team-verdict-*` 文件名决策；无墙 → assemble **红**；与蓝图 §4「唯一产物」一致。 |
| **回归风险** | round2 边界；evidence tar 与 verdict round 不一致（现 L3017–3025 逻辑须迁入墙字段）。 |

---

### I3 · 缺 foreman-run 禁止 `init_wall` 重建（W1）

| 项 | 内容 |
|---|---|
| **现状（#506）** | validate（L1429–1430）、validate2（L2882 一带）、worker 路径（L750）等在下载失败后 **`init_wall` 重建**，**丢掉 L0 `env`** 等切片。#506 §8 I3。 |
| **要改什么** | 1. 所有 job 内「下载墙 → 若无则 init_wall」shell 分支改为：**下载失败或文件不存在 → `exit 1`**（fail-closed）。2. **唯一允许** `init_wall` 的 job：**env-check**（L0 写入 `env`）及 lead 起跑经 `foreman_ok` 后的首轮创建（若蓝图如此规定）；其余 job **只 merge/patch**。3. `download-artifact` **去掉** `continue-on-error: true`（prep L783–785、assemble L2967、validate 相关步等，逐 job 清点 grep）。 |
| **涉及文件** | `.github/workflows/team.yml`（grep `init_wall` | `continue-on-error` + `foreman-run`）；`scripts/team/env_check_wall.py`（L0 合法 init）。 |
| **机器门 / 测试** | `lint_workflow_foreman.py` 增加：禁止 `validate`/`assemble`/`prep` 内出现 `init_wall` fallback 模式；契约测试可选。 |
| **完成判据** | 任一中间 job 在 foreman-run artifact 缺失时 **job 失败**；墙上 `env.hard_fail_count` 等 L0 字段 **不被**中间 job 静默清空。 |
| **回归风险** | artifact 上传偶发失败导致链式红——属 **预期 fail-closed**，非逃逸。 |

---

### I4 · lead 派单、replan 评论硬失败 + 写回 `closeout.comments`（W2 / B4）

| 项 | 内容 |
|---|---|
| **现状（#506）** | lead **plan-comment** 裸 `gh issue comment`（L368），含「状态代偿记录」文案（L364）；replan 双评论裸 `gh`（L1838–1839）。`post_comment_hard.py` 支持 `--hard-required` 与 `--wall-patch` 参数（L15），但 **未实现 patch 写墙**；lead/replan **未接**。#506 §8 I4。 |
| **要改什么** | 1. lead 派单、replan 通知改为 `post_comment_hard.py --hard-required`（母单 + 计划单 replan 同理 assemble）。2. **实现** `--wall-patch`：`post_comment_hard.py` 在成功后 `load_wall` → patch `closeout.comments.<key>.posted=true/false` → `save_wall`（key：`plan_dispatch` / `replan_notice` 等，对齐 schema §2.3.7）。3. 失败时 exit 1 → lead/replan job 红。4. 各 job 尾步继续 upload `foreman-run-${{ github.run_id }}`。 |
| **涉及文件** | `.github/workflows/team.yml` lead（L364–368）、replan（L1834–1839）；`scripts/team/post_comment_hard.py`；`schemas/foreman-run.v1.schema.json` `closeout.comments`（若缺 key 则扩展枚举，**仍属 ForemanRun 单 schema**）。 |
| **机器门 / 测试** | 单测 mock `gh` 失败 → exit 1；成功 → 墙 `closeout.comments.*.posted==true`。 |
| **完成判据** | 派单/再计划评论失败 **不**继续绿跑；墙上可追溯 `posted` 状态。 |
| **回归风险** | PAT 权限临时失败 → run 红（符合 B4）。 |

---

### I5 · 去掉 adopt / derive 的 `|| true`（W4 / B2）

| 项 | 内容 |
|---|---|
| **现状（#506）** | validate round1：`adopt_verdict.py`（L1435–1436）、`compute_validate_conclusion.py`（L1460–1461）带 **`|| true`**；round2（L2890–2892、L2907–2908）同构。尾步另有 **无** `|| true` 的 `compute_validate_conclusion`（L1498、L2946），但 **steps.adopt.outcome 恒 success** 仍削弱 upload 门耦合。#506 §8 I5。 |
| **要改什么** | 1. **删除**采认步与 derive 步上的 `|| true`（或改为 `set -e` 管道）。2. upload verdict 的 `if` **改读墙**：`validation.adoption_status`、`artifacts.team-verdict-*.complete`（已有 `assert_artifact_complete.py`），**不**依赖 `steps.adopt.outcome == success`。3. 采认失败路径已由 `adopt_verdict.py` / `derive` 写 `human_stop`（`tests/test_adoption_failed_sets_human_stop`）——须保证 job 结论与墙一致。 |
| **涉及文件** | `.github/workflows/team.yml` validate / validate2 jobs；`scripts/team/adopt_verdict.py`、`compute_validate_conclusion.py`、`assert_artifact_complete.py`。 |
| **机器门 / 测试** | 现有契约测试 + 新增：derive 失败时 upload 条件为 false；lint 禁止 `adopt_verdict.*\|\| true`。 |
| **完成判据** | 采认/derive 非零退出 → validate job **红** 且墙上 `adoption_status=failed`；无 steps 假绿。 |
| **回归风险** | 与 validate 尾步重复 derive 的交互须保留 **单一** 权威尾步。 |

---

### I6 · `foreman_mode` 生产宽口径机器门（Y3 / L6）

| 项 | 内容 |
|---|---|
| **现状（#506）** | `vars.FOREMAN_MODE \|\| 'test'`（L62、L389）；`validate_foreman_mode.py` **仅**在 `mode==prod` 时限制 `max_processes>3`（L17–19），**不**阻止生产仓隐式 test 宽口径。#506 §8 I6、蓝图 §12.2。 |
| **要改什么** | 1. **本试验仓**可保持默认 `test`。**Factory Mission 生产仓**（或 repo 级 `vars.FOREMAN_REQUIRE_PROD=true`）：lead 内 `validate_foreman_mode.py` 扩展——若生产 profile 且 plan/墙 `foreman_mode!=prod` → **exit 1**。2. plan JSON **必填** `foreman_mode`（prod 仓）或 workflow env **显式** `FOREMAN_MODE=prod`（禁止仅靠默认）。3. 墙上 `foreman_mode` 与 plan 一致校验（patch lead 步）。 |
| **涉及文件** | `scripts/team/validate_foreman_mode.py`；`.github/workflows/team.yml` lead Validate foreman_mode（L378–383）；文档 `docs/领班制-整面API墙方案.md` §12.2（运维约定）。 |
| **机器门 / 测试** | 单测：prod gate + 6 工序 → 1；prod gate + mode test → 1（当 `FOREMAN_REQUIRE_PROD=1`）。 |
| **完成判据** | 生产配置下 **无法** 在未声明 `prod` 时落盘 4+ 工序宽 plan。 |
| **回归风险** | 试验仓 CI 须显式关 `FOREMAN_REQUIRE_PROD` 以免破坏压测。 |

---

### I7 · 收口卡去掉「评论代偿板面」双轨叙述（§8 清存量）

| 项 | 内容 |
|---|---|
| **现状（#506）** | assemble 成功/阻塞 Markdown 仍含「**状态代偿记录**」（L3153、L3197）；全局说明 L3231「Projects 板面字段由 workflow **以评论代偿记录**」。PAT 写板已接 `project_state_write.py`（L3068–3079），但文案仍暗示评论为板面权威。#506 §8 I7。 |
| **要改什么** | 1. 收口卡、lead plan-comment **删除或改写**「状态代偿记录」为 **「审计镜像（只读）」**，且仅当 `closeout.project_state_written==true` 时允许附带镜像句。2. 写板失败 → **job 红**（已有 board_write 门）；文案 **不得**写「字段直写待令牌」作为并行权威。3. lead L364 派单评论同改。 |
| **涉及文件** | `.github/workflows/team.yml` assemble Python/heredoc 文案块（L3150–L3231）、lead plan-comment（L364）；与 I4 评论 patch 协调 `closeout.comments` 语义。 |
| **机器门 / 测试** | grep/lint：`状态代偿记录` 在 assemble/lead 中出现次数为 0 或仅出现在「审计镜像」注释；`test_foreman_wall_contract` 无变即可。 |
| **完成判据** | 代理读本 run 评论 **不能**合理推断「评论即板面真相」；板面真相仅 `closeout.project_state_*` + Projects #33。 |
| **回归风险** | 低；纯文案 + 与写板顺序一致。 |

---

### I8 · 活验四类场景（四步法 ③）

**声明**：#506 已标 **本轮未拉 Actions 工件**；下列 **均未**在仓内归档通过证据，施工 **不得**假装已跑过。

| 场景 | 怎么跑 | 什么算过（墙 + 行为） |
|---|---|---|
| **A 采认失败** | 试验工单 + 人为让 validator droid timeout（124）或缺草稿；或本地 replay + 上传工件 | `validation.adoption_status=failed`；`human_stop=true`；`artifacts.team-verdict-*.complete` 为 false **或** verdict 为失败态 schema 合法；**无** stream-only 半套；validate job **红**；replan **不**触发 |
| **B 评论硬失败** | staging：mock `gh` 失败（`GH_TOKEN` 只读）或 `--hard-required` 路径；跑完整链至 assemble/lead | 对应 job **exit 1**；`closeout.comments.<key>.posted=false`（I4 落地后）；run **红** |
| **C PAT 缺失** | 临时清空 `PROJECTS_STATE_PAT` / env-check 注入失败 | `env.hard_fail_count>0`，`secrets_required.PROJECTS_STATE_PAT` false；**lead skipped**（`foreman_ok`）；不得起跑领班 |
| **D 半套 artifact** | 打断 assert 或采认中途失败，使 upload 不应发生 | 墙上 `artifacts.*.complete=false`；replan/assemble **不**把 `validator-stream.jsonl` 当 verdict；无 `team-verdict-*` 可下载完整成员 |

**归档要求**：每类至少 **1 个 `github.run_id`**，附件含 `foreman-run.json` 摘录、job 结论截图或 `gh run view` 摘要；入仓路径建议 `docs/evidence/zero-escape-live/<run_id>-<scene>.md`（**P3 施工 PR 增**，非本文档回合）。

**完成判据**：四类均有归档且满足上表；对抗审 P4 可引用。

---

## 4. 文件与职责速查（避免再发明接口）

| 路径 | 职责（零逃逸收口中的角色） |
|---|---|
| `schemas/foreman-run.v1.schema.json` | 唯一 JSON Schema；I4/I7 仅扩展 `closeout` 子字段 |
| `scripts/team/foreman_run_lib.py` | `init_wall`（仅 L0）、`prep_should_run`、schema 校验、`human_stop` 规则 |
| `scripts/team/env_check_wall.py` | L0 `env` 切片写入墙 |
| `scripts/team/merge_worker_deltas.py` | matrix delta → `workers.completed_pids` 并集（I1 上游） |
| `scripts/team/adopt_verdict.py` | 采认写 `validation.*`（I5 失败必传播） |
| `scripts/team/compute_validate_conclusion.py` | job 结论派生 + `human_stop`（I5） |
| `scripts/team/compute_replan_gate.py` | `replan_gate.should_replan` 唯一计算 |
| `scripts/team/assert_artifact_complete.py` | upload 前门（I5/D 场景） |
| `scripts/team/post_comment_hard.py` | B4 硬评论 + I4 wall patch |
| `scripts/team/project_state_write.py` | PAT 写 Projects #33（I7 板面权威） |
| `scripts/team/assemble_chain_facts.py` | 无 verdict 时 chain_facts（I2 降级路径须收窄） |
| `scripts/team/validate_foreman_mode.py` | I6 工序宽口径 |
| `scripts/team/lint_workflow_foreman.py` | PR 机器门：禁 legacy replan 字符串、禁 `init_wall` fallback 等 |
| `tests/test_foreman_wall_contract.py` | 契约测试 11+ 用例；每阶段 P0–P2 须增补 |
| `.github/workflows/team.yml` | 编排 **只**读墙投影 outputs / 墙脚本；I1–I7 主战场 |
| `.github/workflows/env-check.yml` | L0 PAT/硬失败（I8-C 场景上游） |

**禁止**：新增 `TeamGate*.json`、独立 `adopt-verdict` action 契约、第二套 artifact 命名约定。

---

## 5. 非目标

- 不修改 `@team-droid` 触发、concurrency、计一致脚本（计一致与 B5 标题 **仍待联审**，零逃逸宣称 **不依赖**计一致已证）。
- 不实现蓝图 §3「foreman-run-session」统一 droid 包装（属后续 L2+；非 I1–I8 阻塞）。
- 不回溯 v2.6.x 历史 run / artifact。
- 本计划文档 PR：**不** merge #505、**不**触发领班 workflow。

---

## 6. 运维依赖（未配置则无法完成 G2/G4）

| 依赖 | 用途 | 缺省时的行为（已部分硬化） |
|---|---|---|
| `secrets.PROJECTS_STATE_PAT` | Projects #33 字段写入 | env-check HARD FAIL；lead 不跑（I8-C） |
| 工单挂 Projects **#33** | `project_state_write.py` 目标板 | 写板失败 → assemble 红 |
| 板字段名与脚本一致 | 六态枚举映射 | 写板失败 → assemble 红（非逃逸） |
| `vars.FOREMAN_MODE` / 生产 `FOREMAN_REQUIRE_PROD` | I6 | 仅影响宽口径；缺省 test |

---

## 7. 仍不能称为「完成」的条件（即使 #505 已 merge）

- 仅 merge #505 **未**做 I1–I8 → **有条件通过**，非零逃逸。
- 仅本地 pytest 通过、**无** I8 四类活验 → **不得**宣称零逃逸。
- 实现对抗审仍为「有条件通过」→ **不得**对外硬性墙口径。
- `main` 仍为 v2.6.5 时（#505 未合入）→ 对抗审对现网 **驳回**（#506 §7.1）。

---

## 8. 与 PR 栈关系

| PR | 关系 |
|---|---|
| #505 | 被收口实现基线 |
| #506 | 实现对抗审；I1–I8 来源 |
| 本计划 PR | 仅 `docs/领班制-API墙零逃逸收口计划.md`，**stack 于 #506** |
| 预期后续 | 按 P0→P4 改 #505 实现 → 新 PR stack 于 #505 或收口分支 → P4 审阅 PR |

---

*计划作者：Cloud Agent · 零逃逸收口 · 不触发 team workflow*