# 领班制 API 硬化修改方案

| 字段 | 值 |
|---|---|
| 目标仓 | `hdot123/droid-mission-test` |
| 对齐工作流 | `Droid Team v2.6.5`（`.github/workflows/team.yml`） |
| 对齐板面 | GitHub Projects **#33**（试验线）；定版 live v50 见 Notion，本方案以仓内契约为准 |
| 文档性质 | **仅设计方案**，本次不修改 `.github/workflows/`、测试与业务代码 |
| 方法论 | Lauren Tan（SpaceXAI / Grok Bot）**API 硬化**：把最短路径做成唯一正确路径；禁止用注释/文档当控制面 |
| 计数前提 | 停止条件仍为**连续 4 轮计一致**；第 45 轮清零后，第 46 轮起为战役第三轮、固定 4 路并发 |

---

## 0. 适用范围与制度边界

### 0.1 试验线 vs 生产正形

| 维度 | 试验仓（本仓） | 生产正形（Factory Mission） |
|---|---|---|
| 工单生命周期 | pass 母工单可故意 Open；PR 常不合并；失败单可不关单 | 按 Mission 收口纪律 |
| 领班能力 | 可有「领班自拆」压测题型 | **只做工序化投影**：不得改工单目标、扩 Scope、凭空加活 |
| 规划层停止 | 与 Mission「只停规划层」一致 | 同左 |

方案中凡涉及「replan 改卡 / 领班写 team-plan-v2」的硬化，均标注 **试验 API**；生产侧应通过**能力裁剪**（禁止 `team-plan-v2` 含新工序 id）而非放宽 prompt。

### 0.2 现行 job 链（接口地图）

```
issue_comment(@team-droid)
  → env-check (reusable: env-check.yml, project_number=33)
  → lead (droid 600s, job 15m) → artifact team-plan-*
  → worker[matrix] (droid 900s, job 25m) → 分支 team/issue-<n>/<pid>
  → prep (脚本合并+pytest 600s, job 20m) → team-evidence-* / manifest_sha256
  → validate (droid 600s, 无 GH token) → team-verdict-* / outputs: overall, failed_processes, unattributed_failure
  → replan (条件: validate success 且 overall!=pass, droid 480s)
  → worker2 / prep2 / validate2（同上契约，artifact 后缀 2）
  → assemble (always 若 lead 非 duplicate) → 收口评论 + 可选 PR
```

**关键产出文件**

| Job | 必交付物 | 下游硬依赖 |
|---|---|---|
| prep | `evidence.tar.gz` 内 `manifest.json`（含 `pytest_exit`, `candidate_branch`, `packs`） | validate 的 `EXPECTED_MANIFEST_SHA` |
| validate | **`verdict.json`**（机器闸合并产物，非 `verdict-droid.json`） | replan 读 `dl/team-verdict-*/verdict.json`；assemble pick |
| validate | `verdict-droid.json`（仅智能体草稿，工作目录 `work/`） | 仅供 merge 步消费 |
| assemble | 工单评论「团队状态卡（收口）」 | 计一致 / 人裁 |

---

## 1. 硬化条目（按优先级）

> 每一条均按四步法书写：**① 为何能犯 → ② 改什么接口 → ③ 机器门 → ④ 存量清理 → ⑤ 活验判据**。

---

### P0-1 【补 18】验收采认链：`verdict-droid` 草稿 ≠ `verdict.json` 采认

#### ① 为何能犯（API/工作流给了什么缝）

- **双文件、单点合并**：智能体只被 prompt 要求写 `work/verdict-droid.json`；**唯一合法对外接口**是 merge 步写的根目录 `verdict.json`（`team.yml` validate → `Merge verdict, enforce gates`）。
- **失败仍上传半成品**：`Upload verdict artifact` 为 `if: always()`，path 列表同时包含 `verdict.json` 与 `work/validator-stream.jsonl`；merge 未跑成时，artifact 可**仅有 stream、无 verdict.json**。
- **下游假定采认已完成**：`replan` 无条件 `cp dl/team-verdict-*/verdict.json`；`assemble` 无 artifact 时走合成 `fallback_reason`，且 **replan 触发要求 `needs.validate.result == 'success'`**——validate job 红则整条改计划链跳过。
- **仓内对证**：
  - Run [`44374403734`](https://github.com/hdot123/droid-mission-test/actions/runs/44374403734)（第 43 轮 A）：`validator` job **failure**；下载 `team-verdict-issue-407-run-44374403734` **仅有** `work/validator-stream.jsonl`，**无** `verdict.json`。
  - Run [`44374448203`](https://github.com/hdot123/droid-mission-test/actions/runs/44374448203)（第 43 轮 B）：同上形态（validator failure + assemble failure）。

根因：把「智能体会话结束」和「采认链 completion」绑在同一 step 的 shell 退出码上，且允许 artifact 上传**未采认**状态。

#### ② 改什么接口（只允许什么）

引入 **`ValidatorCompletion` 契约**（v2.7+ 目标形态），对 `validate` / `validate2` 两类 job 相同：

| 阶段 | 新接口 | 允许 | 禁止 |
|---|---|---|---|
| `judge` | `droid exec` 子步 | 只写 `work/verdict-droid.json` + `work/verdict-droid.md` | 不得假定 job 已成功 |
| `adopt` | **独立 step** `adopt-verdict`（纯脚本，无 droid） | 读草稿 + manifest，写出**唯一** `verdict.json`、`verdict.md`；设置 job outputs | 草稿缺失时写 **`verdict.json` 失败态**（`overall=fail`, `adoption_error` 枚举），不得留空 |
| `publish` | `upload-verdict` | **仅当** `adopt-verdict` success 且根目录存在通过 schema 校验的 `verdict.json` | 禁止 `always()` 上传缺 `verdict.json` 的 artifact |
| `downstream` | `replan` / `assemble` | 只消费带 `verdict_schema_version` 且 `adoption_status=ok` 的 artifact | 禁止 `cp` 不存在的路径；禁止把 stream.jsonl 当 verdict |

`adoption_error` 建议枚举：`missing_draft` | `draft_timeout` | `coverage_mismatch` | `evidence_tampered` | `droid_step_failed`。

#### ③ 机器门（fail-closed）

1. `adopt-verdict` **始终运行**（`if: always()`，但在 precheck 之后），草稿缺失时仍 emit **结构化** `verdict.json`（`processes` 全覆盖，`overall=fail`）。
2. `upload-verdict`：`if: steps.adopt.outcome == 'success'`；合并失败则 validate job 红，但 artifact **要么完整要么不存在**（禁止半套）。
3. 新增 **artifact 契约门**（repo 内 `scripts/team/verify-verdict-artifact.py` + CI 工作流只读测试）：解压 artifact 必须含 `verdict.json` 且通过 JSON Schema。
4. `replan` if 改为：`validate.result in (success, failure) && file_exists(verdict.json) && verdict.adoption_status==ok`（或 `validate.outputs.verdict_adopted == 'true'`）；采认失败时走 **人类停单** 分支，不静默 skip。
5. `assemble`：**禁止**在无 `verdict.json` 时用 `fail_text` 瞎猜；改用 `verdict.adoption_error` 字段生成收口卡。

#### ④ 存量清理

- 删除「仅 stream 的 verdict artifact」作为 replan/assemble 的合法输入；文档与 agent prompt 中凡写「读 validator-stream 即可」一律改为「只认 `verdict.json`」。
- 历史 run artifact 不删；新门只约束 v2.7+ workflow 产生的工件。
- 收口评论模板增加一行：`采认：ok | <adoption_error>`。

#### ⑤ 活验判据

- 注入测试：validate job 在 `droid` step 人为 `exit 124`（600s 杀）时，`adopt-verdict` 仍产出 `verdict.json`，`adoption_error=draft_timeout`，**无**「仅有 stream 的 artifact」。
- 重放第 43 轮 A 类题面：pytest 可绿，但 replan 能读到失败采认 verdict 并给出明确停单理由，而非 `replan: skipped` + assemble 合成理由。

---

### P0-2 【补 10】600s 会话预算杀（K 型）：pytest 全绿却无 verdict / replan / 收口

#### ① 为何能犯

- **嵌套超时、语义不一**：`lead` / `validate` / `validate2` 在 **job `timeout-minutes: 15`** 内再套 `timeout … 600s droid exec`（`team.yml` L186、L1140、L2463）；`worker` 用 **900s droid** + **25m job**（L371、L461）。
- **K 型路径**：prep 脚本超时已标准化（exit 124，`PYTEST_FULL_TIMEOUT = 600`，L710），可出现 **prep success + pytest_exit=0**，同时 validate 的 droid 步被杀 → merge/adopt 未执行 → **无采认 verdict**（与补 18 叠加）。
- **replan 门过窄**：`if: needs.validate.result == 'success'`（L1283）——validate 红（含 droid 被杀）时 **replan 必 skip**，即使 `overall` output 未写出。
- **对证**：第 43 轮 A/B（上节 runs）；第 45 轮 A（run `44428440695`）validate **success** 因采认完成；对比 A/B 为 validate **failure** 且无 verdict.json。

根因：智能体预算与 **采认/编排** 共用同一 job 生死；超时被视为「整 job 失败」而非「可降级的采认失败」。

#### ② 改什么接口

| 组件 | 现行 | 硬化后 |
|---|---|---|
| 智能体调用 | shell 内联 `timeout 600s droid exec` | 抽出 **`TeamDroidSession` 复合 action**（或脚本）：输入 `role=lead\|validator\|replan`, `wall_budget_sec`, `output_contract` |
| 输出契约 | 文本 prompt「写某文件」 | `output_contract` **必填**枚举：`plan_json` \| `verdict_draft` \| `plan_v2_json`；action 结束必须报告 `completion_status` |
| 预算分层 | 600s 与 15m job 混用 | **规则**：`droid_wall + adopt_overhead + upload < job_timeout`；validator 默认 `droid_wall=480`，**adopt 纯脚本 ≤120s**，job wall **≥12min 专用于 adopt+upload** |
| pytest | prep 内 600s | 保持；validate **不得**再跑全量 pytest（已满足） |

禁止：validate job 在 droid 被杀时 **不产出** verdict 采认结果（须落 P0-1）。

#### ③ 机器门

1. `TeamDroidSession` 对 exit 124 写 `work/session-outcome.json`（`status=timeout`），`adopt-verdict` 读此文件填 `adoption_error=draft_timeout`。
2. workflow 静态校验（`scripts/team/lint-workflow-budgets.py`）：解析 `team.yml`，断言各 role 的 `job_timeout ≥ droid_wall + MIN_ADOPT_SEC`。
3. replan 触发改为基于 **`verdict.overall != pass` 且 `verdict.adoption_status==ok`**，与 validate job 红绿解耦（采认成功即可触发判层）。
4. lead/replan 超时同样走采认/落盘：`team-plan.json` / `team-plan-v2.json` 缺失时 **lead job 失败且禁止 worker 启动**（已有 plan gate，须加「超时未写出 plan」专用错误码）。

#### ④ 存量清理

- 去掉各 prompt 里「at most N tool calls」作为唯一效率约束；改为 **硬预算 + 采认 fallback**（prompt 保留但非控制面）。
- 文档统一：**600s 是智能体预算，不是验收通过条件**。

#### ⑤ 活验判据

- 故障注入：validator droid 强制 124 → 仍产出 `verdict.json` + `adoption_error`；assemble 展示「验收采认超时」而非「验收未产出判定（结构性失败）」泛化句。
- 回归：prep 故意延迟至 pytest 仍 0，validate 在预算内完成 adopt → replan 正常触发。

---

### P1-1 【§12 第 3 件】Projects 六态：评论代偿 → 板面 API

#### ① 为何能犯

- 现行仅在评论写「状态代偿记录：…」（`lead` L352、`assemble` L2871）；**无 Projects GraphQL 写字段**。
- `env-check` 对板面读失败只 **WARN**（`env-check.yml` L179–187），与需求「读不到应 FAIL」冲突；且注释写明 `GITHUB_TOKEN 无 Projects 权限`。
- 智能体/人读板面看不到六态，**只能抄评论**——下轮代理把评论当权威，板面与评论漂移。

#### ② 改什么接口

- 新增 **`ProjectStateWriter`**（仅 `assemble` / `lead` 计划落成步可调用）：
  - 输入：`issue_number`, `state_enum` ∈ `{已派单,施工中,待验收,已验收,阻塞,关闭}`，`run_id`, `evidence_url`
  - 凭据：**独立 secret** `PROJECTS_STATE_PAT`（classic PAT 或 GitHub App installation），**禁止**复用 worker 无 token 的 validate 面
- 评论降为 **只读镜像**：写入成功后才允许发「状态代偿记录」；写失败则 **assemble job 失败**（与 A4 一致）。

#### ③ 机器门

1. `env-check`：当 `project_number!=0` 时，用 **同一 PAT** probe `view`；失败 → **FAIL**（非 WARN）。Actions「可建 PR」已在 L122–137 为 FAIL，保持。
2. `assemble` closeout：先 `ProjectStateWriter`，后 `gh issue comment`； comment 失败吞掉时已有 `::warning::`（L2875）——改为 **exit 1**。
3. JSON Schema 校验 `state_enum`，非法值 workflow 编译期 rejection（lint 脚本扫描调用点）。

#### ④ 存量清理

- 从 prompt/文档删除「字段直写待令牌方案」作为**长期**说法；改为「试验线过渡期：评论仅镜像，以板面为准」。
- Projects #33 历史 issue 批量回填脚本（离线，非本 PR）：按最后一张收口卡解析态。

#### ⑤ 活验判据

- 故意撤销 PAT：`env-check` 硬失败，lead 不启动。
- 成功 run：Project 字段与收口卡一致；评论删除后板面仍正确。

---

### P1-2 【A4】assemble 必贴收口卡；关单/评论失败不可吞

#### ① 为何能犯

- `gh issue comment … || echo "::warning::"`（L2875）——评论失败 **不 fail job**。
- `Post minimal status card when pick failed` 同样 `|| echo warning`（L2895）。
- 计一致依赖「收口卡出现」；漏贴导致 **假阴性/计不一致**（#7 类）。

#### ② 改什么接口

- `CloseoutPublisher`：唯一入口 `(issue_number, body, required=true)` → 失败 **必须 exit 1**。
- assemble 步序固定：`pick` → `render` → **`publish`（硬）** → `fail-run-if-needed`。
- 子单/计划单 `gh issue close` 与 PR 创建保持现有 PR-first 逻辑（L2777–1797），但纳入同一 publisher 的 **事务语义**：PR 成功后才 close；任一步失败回滚 close（已部分实现，须统一错误码）。

#### ③ 机器门

- 删除所有 `gh … || echo warning` 于 assemble/lead 计划评论路径（检索清理）。
- 新增 job output `closeout_posted=true/false`；外层 workflow run summary 断言。
- 契约测试：mock `gh` 返回非 0 → job 必红且 **无**「团队状态卡」视为已贴（通过 API 查 comment）。

#### ④ 存量清理

- 文档明确：测试线「失败单不关单」仅指 **子单/issue close 策略**，不指 **母工单无收口卡**。

#### ⑤ 活验判据

- 模拟 comment 403：run 失败，工单无收口标题评论；计一致不计入 pass。

---

### P1-3 【F2】assemble 收口理由必须与真实 job 链一致

#### ① 为何能犯

- 无 verdict 时 `pick` 按固定 `chain_order` 取**第一个** `failure|cancelled`（L2691–2700）：`lead → worker → prep → validate → …`
- **未交叉验证** `needs.*.result`：worker matrix 任一片失败 → `needs.worker.result=failure`，即使 **prep success**，仍命中 `worker` 文案「备料未启动」（L2673）。
- 对证：逻辑上可构造「工人局部失败 + prep 已合并」（`prep` if 仅排除 `cancelled`，L653）；与 #72 类「误写备料未启动」一致。

#### ② 改什么接口

- `AssembleChainFacts`：输入为 **显式结构**  
  `{(job, result, started, produced_artifact: bool)}`  
  禁止从单一 `chain_order` 推断。
- `fallback_reason` 生成规则：
  1. 若存在 `team-verdict-*` 但 schema 非法 → `adoption_error`（P0-1）
  2. 否则按 **拓扑序** 找第一个「应运行且未产出下游必需 artifact」的 job（prep 需要 `team-evidence-*`；validate 需要 `verdict.json`）
  3. worker 失败但 `team-evidence-*` 存在 → 理由必须写「工人有失败工序，备料已完成」

#### ③ 机器门

- `pick` 步 Python 单测夹具：worker failure + prep success → 禁止出现「备料未启动」。
- CI：`scripts/team/test-assemble-fallback.py` 绑定 `chain_facts` JSON golden files。

#### ④ 存量清理

- 删除 `fail_text` / `cancel_text` 静态表；改为模板 + facts 渲染。
- 历史错误评论不改；新 run 不得再生成同类文案。

#### ⑤ 活验判据

- 重放 #72 拓扑（工人红、prep 绿、validate 红）：收口卡写明「备料完成，验收采认失败/未产出 verdict」。

---

### P1-4 env-check：Project 不可读 / 不可建 PR 必须 FAIL

#### ① 为何能犯

- 板面：`gh project view` 失败 → **WARN**（L185–186），`HARD_FAIL` 不置位（L208 仅看 `HARD_FAIL`）。
- 仓库 Actions 设置读不到时也是 WARN（L141）——与「应 FAIL」需求部分冲突（用户明确要求 Project + PR 能力）。
- `outputs.ok` 可为 true 同时含 WARN 板面 → **lead 照常启动**，后在 assemble 才发现板面不可写。

#### ② 改什么接口

- `env-check` 输出三分：`ok` | `hard_fail` | `soft_fail`（试验线可无 soft）。
- **硬失败集**（可配置 `project_number`）：工作流语法、team 权限块、**Secret 名单**、工单 OPEN+三段、**Projects 可读（用 PAT）**、**Actions 可建 PR**、默认 workflow 权限 write。
- WARN **仅**保留：并发队伍提示、模型通道（刻意不查）。

#### ③ 机器门

- `team.yml` `env-check` 门：`needs.env-check.outputs.ok == 'true'` 且 `hard_fail_count==0`。
- 独立 `workflow_dispatch` env-check 用于活验。

#### ④ 存量清理

- 报告模板删除「⚠ 不算通过」歧义句；WARN 与 FAIL 分列。
- 将 `PROJECTS_STATE_PAT` 纳入 secret 名单检查（与 P1-1）。

#### ⑤ 活验判据

- 板面 API 403 → env-check 红，run 仅 env-check job 执行。

---

### P1-5 【第 45 轮定型】worker job 25m 取消 → 整链「备料/验收」被 skip

#### ① 为何能犯

- `worker` **matrix 单叶 `timeout-minutes: 25`**（L371）；bstree 等重题可 **cancelled**（run `44428751046`：一 worker cancelled，**prep/validate/replan 全 skipped**，assemble failure）。
- `prep` if：`needs.worker.result != 'cancelled'`（L653）——**一票否决**：任一 matrix cancelled → prep 不跑。
- 与「失败单不关单、可局部失败」试验口径冲突：备料本可合并成功工序证据，却被 API 拒绝。

#### ② 改什么接口

- **`WorkerMatrixResult` 聚合 API**（job outputs）：
  - `any_cancelled`, `any_failed`, `all_success`, `completed_pids[]`, `cancelled_pids[]`
- `prep` 触发：`lead.success && !duplicate && completed_pids 非空`（**不要求** worker 全集 success）。
- prep 合并策略：仅合并 **completed** 分支；cancelled/failed 记 manifest `packs[pid].complete=false` → validate **blocked**（已有 L1036–1046）。

#### ③ 机器门

- worker job 增加汇总 step（`always()`）写 `team/worker-matrix-summary.json` artifact。
- prep 若无 summary artifact → **FAIL**（禁止猜 matrix 状态）。
- assemble 展示 per-pid：`cancelled_25m_timeout` 枚举。

#### ④ 存量清理

- 文档写明：25m 是 **工人 lease 上限**，不是 team run 上限；cancelled 工序不得拖死 prep。

#### ⑤ 活验判据

- 复现 45B：三 worker 中一 cancelled、两 success → prep 仍跑，validate 出 verdict（含 blocked），assemble 贴卡，**不得** prep skipped。

---

### P1-6 【补 20 / 编排门】replan 与 validate outputs 字符串契约

#### ① 为何能犯

- `needs.validate.outputs.failed_processes != '[]'`（L1283）依赖 **JSON 字符串化 output**；空格/序列化变化可误触发或漏触发。
- `fromJSON(needs.lead.outputs.processes)` 等无 schema 版本号，plan 形变时静默坏。

#### ② 改什么接口

- 所有跨 job 传递改用 **artifact 侧车** `team-gate-*.json`（含 `schema_version`, `failed_ids[]`, `unattributed_failure: bool`）。
- outputs 仅保留标量 `overall`；复杂结构禁止走 `GITHUB_OUTPUT` 字符串比较。

#### ③ 机器门

- `replan` if 读 artifact 中布尔/数组，**禁止**字符串 `'[]'` 比较。
- repo lint：`ripgrep "outputs\\.failed_processes != '\\[]'"` 为 CI 失败。

#### ④ 存量清理

- v2.6.x 历史 run 不回溯；v2.7 起重放 replan 触发单测。

#### ⑤ 活验判据

- failed_processes 空数组与 unattributed_failure true 同时存在 → replan 必触发（第 17 轮 C1 场景）。

---

### P2-1 领班「自拆」试验 API 与生产裁剪

#### ① 为何能犯

- `lead` prompt 允许 1–6 工序（L175）；试验压测可自拆，但 **无 `deployment_mode=test|prod` 开关**，生产代理可抄 6 工序宽口径。

#### ② 改什么接口

- workflow 输入 `foreman_mode: test | prod`（默认 test 于本仓）。
- `prod`：`max_processes=3`，禁止新增不在工单「交付物」枚举内的文件 pattern；`replan` 禁止 `revise` 引入新 `id`。

#### ③–⑤（简述）

- 机器门：plan validate 脚本读 `foreman_mode`。
- 清理：试验题目标注 `mode=test` front-matter。
- 活验：prod 模式下 4 工序 plan 硬拒绝。

---

## 2. 非目标（本次方案不施工）

- 不修改 `.github/workflows/team.yml` / `env-check.yml` / `droid.yml` 等。
- 不调整 `@team-droid` 触发、concurrency、计一致脚本。
- 不合并 PR、不 `@team-droid` 点火。
- 不改动审计分支 PR #404、考题 PR #405 历史。

---

## 3. 建议施工顺序（落地 v2.7 时）

| 阶段 | 内容 | 依赖 |
|---|---|---|
| **S1** | P0-1 采认链（`adopt-verdict` + artifact schema + replan/assemble 读采认） | 无 |
| **S2** | P0-2 预算复合 action + workflow budget lint | S1 |
| **S3** | P1-5 worker matrix 聚合 + prep if 改造 | S1 |
| **S4** | P1-4 env-check 硬 FAIL + `PROJECTS_STATE_PAT` | 可与 S1 并行 |
| **S5** | P1-1 Projects 写板 + P1-2 收口 publisher | S4 |
| **S6** | P1-3 assemble chain facts 单测 | S1 |
| **S7** | P1-6 gate artifact；P2-1 foreman_mode | S1 |

**建议版本号**：`v2.7.0` = S1+S2；`v2.7.1` = S3–S6；`v2.7.2` = P2。

---

## 4. 改动清单摘要（四步收口）

| ID | 主题 | ② API 核心 | ③ 机器门关键词 |
|---|---|---|---|
| P0-1 | 补 18 采认链 | `adopt-verdict` 唯一产出 `verdict.json` | 无采认不上传 artifact；replan 认 `adoption_status` |
| P0-2 | 补 10 K 型 | `TeamDroidSession` + 预算 lint | 124 → 结构化采认失败；replan 与 job 红绿解耦 |
| P1-1 | 自动写板 | `ProjectStateWriter` + PAT | env-check 板面 FAIL；写失败 assemble 红 |
| P1-2 | A4 收口 | `CloseoutPublisher` | 评论失败必 exit 1 |
| P1-3 | F2 理由 | `AssembleChainFacts` | 单测禁止「备料未启动」误报 |
| P1-4 | env-check | 硬失败集含 Project+PR | `ok` 与 WARN 脱钩 |
| P1-5 | 45B 工人超时 | `WorkerMatrixResult` | prep 不因单一 cancelled skip |
| P1-6 | 编排门 | `team-gate-*.json` | 禁字符串 `'[]'` 比较 |
| P2-1 | 试验/生产 | `foreman_mode` | plan 工序上限与 revise 约束 |

---

## 5. 参考证据索引

| 现象 | 仓内/Run 证据 |
|---|---|
| v2.6.5 头注与 600s/900s 超时 | `.github/workflows/team.yml` 文件头、L186、L461、L1140 |
| 补 18 无 verdict.json | Actions run `44374403734`, `44374448203`；artifact 仅 `validator-stream.jsonl` |
| 45A 工人失败仍走完 validate | run `44428440695` job 列表 |
| 45B worker 25m cancelled → prep skip | run `44428751046` |
| env-check 板面 WARN | `.github/workflows/env-check.yml` L179–187 |
| assemble 误报链 | `team.yml` L2666–2700 `chain_order` + `fail_text.worker` |
| 评论失败可吞 | `team.yml` L2875、L2895 |
| replan 依赖 validate success | `team.yml` L1283 |

---

*文档作者：Cloud Agent 设计回合；仅存在于 `docs/`，不触发 team workflow。*