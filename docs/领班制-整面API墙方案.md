# 领班制整面 API 墙方案（v2.7 施工蓝图）

> **施工状态（v2.7 实现 PR #505）**：L0–L6 主链已接 `foreman-run.json`；validate/validate2 采认+完整 upload；workers delta 合并（非 last-write）；assemble `chain_facts` 收口；PAT 写板 `project_state_write.py`；handoff/prep 硬评论。仍依赖运维配置 `PROJECTS_STATE_PAT` + 工单已挂 Projects #33；活验未拉 Actions 工件。
>
> **声明**：本文为 **v2.7 施工的权威蓝图**。它**取代** [PR #499](https://github.com/hdot123/droid-mission-test/pull/499) 中「按功能分墙」（`ValidatorCompletion` / `adopt-verdict` / `TeamDroidSession` / `ProjectStateWriter` / `CloseoutPublisher` / `AssembleChainFacts` / `WorkerMatrixResult` / `team-gate-*.json` / `foreman_mode` 各自独立接口）的旧稿写法，作为后续实现的**唯一设计依据**。  
> 输入材料：`docs/领班制-API硬化修改方案.md`、`docs/领班制-API硬化修改方案-对抗审.md`（**不删不改**）。  
> 对照工作流：**Droid Team v2.6.5**（`.github/workflows/team.yml`）、`env-check.yml`（行号以本仓当前 SHA 为准，下文已复核）。  
> **本次交付仅文档，不修改** workflow / 测试 / 业务代码；不 `@team-droid`、不 merge、不开 issue。

| 字段 | 值 |
|---|---|
| 目标仓 | `hdot123/droid-mission-test` |
| 契约名称 | **`ForemanRun`**（整面墙的唯一运行状态对象） |
| `schema_version` | `foreman-run.v1`（v2.7 首期冻结；子段 semver 见各 `*.schema_version`） |
| 文档性质 | 设计方案 + JSON Schema 等价字段表 + 机器门清单 |
| 方法论 | Lauren Tan **API 硬化四步法**：① 追为何能犯 → ② **改 API 拿掉错选项** → ③ 机器守住 → ④ 清存量 |

---

## 1. 墙的定义：什么算「一面墙」

### 1.1 定义

**一面墙** = 整条领班链（env-check → lead → worker[*] → prep → validate → replan? → worker2/prep2/validate2? → assemble）上，**唯一的运行契约** `ForemanRun`：

- **同一套入口**：所有角色（领班、工人、验收员、改计划）通过**同一 session 包装**读写墙，不把「写 plan」「写 verdict 草稿」「写 plan-v2」拆成互不关联的 HTTP/action 面。
- **同一套产物**：每个阶段向墙 **append / patch** 字段；对外 artifact（`team-plan-*`、`team-verdict-*`、gate 文件等）必须是 **`ForemanRun` 已通过 schema 的投影**，禁止半套上传。
- **同一套失败语义**：`adoption_status`、`overall`、`hard_fail`、各 job 的 `chain_facts` 均在**同一份 schema** 内枚举；禁止用 job 红绿代替采认、用评论代偿板面、用 `validator-stream.jsonl` 冒充 `verdict.json`、用 `outputs.failed_processes != '[]'` 字符串比较当编排门。

### 1.2 为何禁止「按功能分墙」（否定 PR #499 形态）

PR #499 为每条硬化项**单独命名接口**（采认一条 API、会话预算一条 API、写板一条 API……）。后果：

1. **编排条件漂移**：`replan` 触发在 P0-2 与 P1-6 各写一套（对抗审 **Y1**）。
2. **失败语义分裂**：`validate` job 结论 vs `adoption_status` 分工不清（对抗审 **B1**）。
3. **下游仍可走缝**：upload `if: always()`（`team.yml` L1269–L1277）+ 多 API 各管一段 → **stream-only artifact** 仍可存在。
4. **代理误读**：多个 action 名 = 多套「权威」；评论代偿、prompt 效率句继续当控制面。

用户要求形态：**整面墙**——采认、600s 预算、写板、收口、工人矩阵、编排门、test|prod **全是墙上的字段与门**，不是再开接口章。

### 1.3 与 Lauren Tan 四步法的关系

| 步 | 整面墙落点 |
|---|---|
| ① 为何能犯 | 各 P0/P1 根因保留于 §6 映射表「现 v2.6.5 死法」列；证据行号见 §11。 |
| ② 改 API | **只扩展 / 校验 `ForemanRun`**；workflow 步序变为「读墙 → 写墙 → 投影 artifact」；**禁止**新增并行契约类型。 |
| ③ 机器守 | §8：`foreman-run.schema.json`、契约测试、workflow lint、CI 禁 `'[]'` 字符串比较等。 |
| ④ 清存量 | §9：废弃半套 artifact 语义、评论当板面权威、长期「待令牌」文案等。 |

---

## 2. 唯一运行契约 `ForemanRun`

### 2.1 命名与版本

- **根对象**：`ForemanRun`
- **`schema_version`**（必填）：`foreman-run.v1`
- **实例 ID**：`run_id` = GitHub Actions `github.run_id`（字符串）
- **工单**：`issue_number`、`plan_issue_number`（可 null 至 lead 落成）

### 2.2 顶层字段一览

| 路径 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `schema_version` | string | ✓ | 固定 `foreman-run.v1` |
| `run_id` | string | ✓ | Actions run id |
| `issue_number` | integer | ✓ | 母工单 |
| `foreman_mode` | enum | ✓ | `test` \| `prod`（见 P2-1；**本仓默认 `test`**，生产正形须显式 `prod`） |
| `env` | object | ✓ | env-check 投影（P1-4 / B3） |
| `budgets` | object | ✓ | 各 role 的 wall 预算（P0-2） |
| `chain` | object | ✓ | 各 job 的 `result` + `chain_facts`（P1-3） |
| `plan` | object | ○ | lead 落成后必填 |
| `workers` | object | ○ | matrix 聚合（P1-5） |
| `prep` | object | ○ | 备料 manifest 摘要 |
| `validation` | object | ○ | 验收 + **采认**（P0-1） |
| `replan_gate` | object | ○ | **唯一** replan 触发状态（P0-2 + P1-6 + Y1） |
| `round2` | object | ○ | replan 后第二轮子树 |
| `closeout` | object | ○ | 收口 + 板面 + 评论发布状态（P1-1 / P1-2 / B4 / B5） |
| `artifacts` | object | ✓ | 各投影名 → `{ complete: bool, missing: string[] }` |

### 2.3 核心子结构（字段表 = JSON Schema 等价）

#### 2.3.1 `env`（env-check 硬门）

```json
{
  "schema_version": "env-slice.v1",
  "ok": true,
  "hard_fail_count": 0,
  "hard_fails": [],
  "soft_warns": [],
  "project_readable": true,
  "actions_can_create_pr": true,
  "secrets_required": {
    "FACTORY_API_KEY": true,
    "WORKER_CI_KEY": true,
    "PROJECTS_STATE_PAT": true
  }
}
```

| 枚举/规则 | 说明 |
|---|---|
| `hard_fail_count` | 非 0 → `env.ok` 必为 `false`（**B3**）；`team.yml` lead 门须读此字段，非仅 `env-check.result == success`（现 L49–50 **未**读 `hard_fail_count`） |
| `project_readable` | `project_number!=0` 时须用 **PAT** 探测；失败计入 `hard_fails`，**禁止**现 `env-check.yml` L185–186 的 WARN 占位 |
| 现 v2.6.5 | 板面失败 WARN + `ok=true`（`env-check.yml` L179–187、L208） |

#### 2.3.2 `budgets`（P0-2 会话预算）

```json
{
  "schema_version": "budget-slice.v1",
  "roles": {
    "lead": { "droid_wall_sec": 600, "job_wall_min": 15, "output_contract": "plan_json" },
    "validator": { "droid_wall_sec": 480, "adopt_reserve_sec": 120, "job_wall_min": 12, "output_contract": "verdict_draft" },
    "replan": { "droid_wall_sec": 480, "job_wall_min": 15, "output_contract": "plan_v2_json" },
    "worker": { "droid_wall_sec": 900, "job_wall_min": 25, "output_contract": "handoff_bundle" }
  },
  "session_outcome": {
    "role": "validator",
    "completion_status": "ok|timeout|droid_failed|missing_output",
    "exit_code": 0
  }
}
```

- **`output_contract`**：墙上的字段，**不是**独立 API 参数表；session 包装**只**接受墙内枚举。
- **规则**：`job_wall_min * 60 ≥ droid_wall_sec + adopt_reserve_sec`（validator）；kill 124 → `session_outcome.completion_status=timeout` → 驱动 `validation.adoption`（非「整 job 无 verdict」）。

#### 2.3.3 `chain`（P1-3 F2）

每个 job 键：`lead` | `worker` | `prep` | `validate` | `replan` | `worker2` | `prep2` | `validate2` | `assemble`

```json
{
  "worker": {
    "result": "success|failure|cancelled|skipped",
    "started": true,
    "produced_required_artifact": false,
    "downstream_blocker": null
  }
}
```

- **禁止** assemble 仅用 `chain_order` + 静态 `fail_text`（现 `team.yml` L2691–L2700）。
- `downstream_blocker`：拓扑推导「第一个应运行但未产出下游必需 artifact 的 job」。

#### 2.3.4 `workers`（P1-5）

```json
{
  "schema_version": "worker-matrix.v1",
  "any_cancelled": true,
  "any_failed": false,
  "completed_pids": ["p1", "p2"],
  "cancelled_pids": ["p3"],
  "cancel_reason_by_pid": { "p3": "job_wall_25m" }
}
```

- prep 门：`completed_pids.length > 0`，**不要求** `worker.result != cancelled`（对比现 L653）。

#### 2.3.5 `validation`（P0-1 采认链）

```json
{
  "schema_version": "validation-slice.v1",
  "round": 1,
  "draft_path": "work/verdict-droid.json",
  "verdict_path": "verdict.json",
  "adoption_status": "ok|failed",
  "adoption_error": null,
  "overall": "pass|fail",
  "failed_process_ids": [],
  "unattributed_failure": false,
  "pytest_exit": 0
}
```

| `adoption_error` 枚举 | 含义 |
|---|---|
| `missing_draft` | 无草稿 |
| `draft_timeout` | droid 124 / 预算杀 |
| `coverage_mismatch` | 工序未全覆盖 |
| `evidence_tampered` | manifest 不一致 |
| `droid_step_failed` | judge 步非 0 退出 |
| `merge_skipped` | 现 v2.6.5：judge 失败则 merge 不跑（L1095–L1142 区间） |

**B1 分工（写死）**：

| 情形 | `adoption_status` | `verdict.json` | validate **job** 红/绿 | replan（见 `replan_gate`） |
|---|---|---|---|---|
| 采认成功，`overall!=pass` | `ok` | schema 合法 | **可为绿**（若仅评判 fail） | **可触发**（Y1） |
| 采认成功，`overall=pass` | `ok` | schema 合法 | 绿 | 不触发 |
| 采认失败（含 timeout） | `failed` | **仍有**失败态 schema 合法 | **红** | **不触发**；assemble 走 `adoption_error` + **人类停单**文案 |
| 无 `verdict.json` 上传 | — | 不存在 | 红 | 不触发；**禁止** replan `cp` 缺路径（现 L1341） |

**禁止**：「采认成功仍 validate job failure → replan skip」（现 L1283 绑 `validate.result == success`）。

#### 2.3.6 `replan_gate`（P0-2 + P1-6 + **Y1 唯一触发**）

```json
{
  "schema_version": "replan-gate.v1",
  "should_replan": true,
  "reasons": ["overall_not_pass", "unattributed_failure"],
  "inputs_satisfied": {
    "adoption_status_ok": true,
    "verdict_artifact_complete": true,
    "not_cancelled": true
  },
  "forbidden_legacy": {
    "validate_job_success_only": false,
    "string_compare_failed_processes": false
  }
}
```

**触发布尔（墙内唯一真相）**：

```
should_replan =
  inputs_satisfied.adoption_status_ok
  && validation.overall != 'pass'
  && (validation.failed_process_ids.length > 0 || validation.unattributed_failure)
  && inputs_satisfied.not_cancelled
```

- workflow `if:` **只读** `ForemanRun.replan_gate.should_replan`（或等价 job output 由墙投影一步写出）。
- **禁止** `needs.validate.outputs.failed_processes != '[]'`（现 L1283）。

#### 2.3.7 `closeout`（P1-1 / P1-2 / B4 / B5）

```json
{
  "schema_version": "closeout-slice.v1",
  "project_state_written": true,
  "project_state_enum": "已验收",
  "comments": {
    "final_status_card": { "posted": true, "hard_required": true },
    "handoff": { "posted": true, "hard_required": true },
    "prep_report": { "posted": true, "hard_required": false },
    "replan_notice": { "posted": true, "hard_required": false },
    "fallback_card": { "posted": false, "title_allowed": false }
  },
  "pr": { "attempted": true, "created": true },
  "run_must_fail": false
}
```

- **B4**：凡 `hard_required: true` 的路径，GH API 非 0 → **job exit 1**（覆盖现 L2875 pass 路径假绿、L630/L989/L1618 等 `|| echo`）。
- **B5**：`fallback_card.title_allowed: false`；禁止标题含「收口」而正文写「未收口」（现 L2891「团队状态卡（收口·兜底）」）。兜底卡标题规范：**`团队状态卡（汇总异常·未收口）`**，且 `closeout.comments.fallback_card.posted` 为 true 时 **`run_must_fail` 必 true**。

#### 2.3.8 `artifacts`（B2 完整投影）

```json
{
  "team-verdict-issue-{n}-run-{id}": {
    "complete": true,
    "required_members": ["verdict.json", "verdict.md"],
    "forbidden_partial": ["work/validator-stream.jsonl"]
  }
}
```

- **`complete: true`** 当且仅当 `required_members` 全存在且 `validation.adoption_status` 已写入 `verdict.json`。
- upload 步：**pre-upload 断言** `artifacts.*.complete`，否则**不上传**（废除 validate upload `if: always()` 半套行为，L1269–L1277）。

### 2.4 完整 JSON Schema 锚点（施工时落盘路径）

施工期将等价 Schema 存为：

`schemas/foreman-run.v1.schema.json`

本文为字段表权威；施工 PR 须用 `ajv` / `check-jsonschema` 与 Python 契约测试双向校验。

---

## 3. 唯一入口：session 包装

### 3.1 原则

- **一个**复合入口（实现名可为一 action + 脚本，但**不**在文档中再列为第二契约）：`foreman-run-session`
- 输入：`role`、`run_id`、`foreman_mode`、**墙上** `budgets.roles[role]`、`output_contract`
- 输出：**patch** `ForemanRun` 的 `budgets.session_outcome` + 角色草稿文件（`team-plan.json` / `work/verdict-droid.json` / `team-plan-v2.json`）

### 3.2 角色与 `output_contract`（墙字段）

| role | output_contract | 草稿路径 | 下游采认步 |
|---|---|---|---|
| lead | `plan_json` | `team-plan.json` | plan gate 脚本 |
| worker | `handoff_bundle` | `team/status/*` | verify + marker |
| validator | `verdict_draft` | `work/verdict-droid.json` | **墙内** `validation.adoption`（非独立 `adopt-verdict` API） |
| replan | `plan_v2_json` | `team-plan-v2.json` | plan v2 gate |

验收员、领班、工人、改计划**不得**绕过 session 包装直写 artifact 名；CI lint 扫描 workflow 中裸露 `droid exec` 须带 `FOREMAN_RUN_PATCH=1` 环境约定。

---

## 4. 唯一产物规则

1. 任何 `actions/upload-artifact` 前：`scripts/team/assert-artifact-complete.py --wall foreman-run.json --name <artifact>`
2. **禁止**半套：`validator-stream.jsonl` **不得**单独构成 `team-verdict-*` 可下载单元（对证：runs `44374403734`、`44374448203`——**继承 #499 叙述，本轮未重拉工件**）。
3. 对齐现死法：`if: always()` upload（L1269–L1270）在 v2.7 **改为** `if: steps.publish-wall.outcome == success' && artifacts[...].complete`。
4. merge 步语义并入 **「投影 verdict」**：读墙 `validation` + 草稿 → 写 `verdict.json` → 回填墙 → 再允许 upload。

---

## 5. 唯一失败语义

### 5.1 枚举汇总

| 字段 | 取值 | 用途 |
|---|---|---|
| `validation.adoption_status` | `ok` \| `failed` | 采认链是否完成（**非** job 颜色） |
| `validation.overall` | `pass` \| `fail` | 业务评判 |
| `env.hard_fail_count` | ≥0 整数 | 起跑门 |
| `closeout.run_must_fail` | bool | 收口后是否强制 run 红 |
| `foreman_mode` | `test` \| `prod` | 工序宽口径 |

### 5.2 禁止代偿

| 禁止 | 现 v2.6.5 证据 |
|---|---|
| job 绿 = 采认完成 | validate failure → merge 不跑 |
| stream = verdict | upload path 含 stream（L1275–L1277） |
| 评论 = 板面 | L2871「状态代偿说明」 |
| `'[]'` 字符串门 | replan L1283 |
| validate 红 → replan 必 skip | L1283 `needs.validate.result == success'` |
| pass 且无收口评论仍绿 | L2875 `|| echo ::warning::`；L2877–2881 条件窄 |

---

## 6. 旧条目 → 墙上的字段与门（不开接口章）

| ID | 墙上位置 | 门 / 规则 | 现 v2.6.5 死法（仓内行号） |
|---|---|---|---|
| **P0-1** 采认链 | `validation.*` + `artifacts.team-verdict-*` | 采认步永远写 `verdict.json`；upload 仅 `complete` | upload `always()` L1269–1277；merge 依赖 judge 成功 |
| **P0-2** 600s K 型 | `budgets.*` + `validation.adoption_error=draft_timeout` | 124 仍产出采认失败态；`replan_gate` 读 `adoption_status` | lead/validate droid 600s（L186、L1140）；replan L1283 |
| **P1-1** 写板 | `closeout.project_state_*` | PAT 写板失败 → `run_must_fail` | 仅评论代偿 L2871、L352 |
| **P1-2** 收口卡 | `closeout.comments.final_status_card` | `hard_required` 失败必 exit 1 | L2875、L2895；PR 逻辑 L2777–2797（**B6 已改正 L2777–1797 笔误**） |
| **P1-3** F2 理由 | `chain.*.chain_facts` | 禁止 worker 失败+prep 成功 →「备料未启动」 | L2666–2700 `chain_order` |
| **P1-4** env-check | `env.*` | 板面/PR 不可 → `hard_fail_count++` | WARN L179–187；lead 仅 L49–50 |
| **P1-5** worker 25m | `workers.*` + prep 读 `completed_pids` | prep 不因单一 cancelled skip | worker 25m L371；prep L653 |
| **P1-6** 编排门 | `replan_gate` | 禁字符串 `'[]'` | L1283 |
| **P2-1** test\|prod | `foreman_mode` | 本仓默认 `test`；**生产**须 `prod` + `max_processes=3`（Y3） | lead 宽 1–6 工序无 mode |

### 6.1 对抗审必改 B1–B6 吸收

| ID | 整面墙落点 |
|---|---|
| **B1** | §2.3.5 表 + §5；`replan_gate.inputs_satisfied.adoption_status_ok` |
| **B2** | §2.3.8 + §4 pre-upload 断言 |
| **B3** | §2.3.1 `hard_fail_count`；lead `if` 读 `env.ok && hard_fail_count==0` |
| **B4** | §2.3.7 `comments.*.hard_required` 全覆盖 handoff/prep/replan/assemble |
| **B5** | §2.3.7 兜底标题规范 + `run_must_fail` |
| **B6** | PR 关闭逻辑引用 **L2777–2797**（已核对现文） |

### 6.2 应改 Y1

P0-2 与 P1-6 **合并**为 `replan_gate` 单对象（§2.3.6）；workflow 禁止第二处 replan 条件。

---

## 7. 机器门（v2.7 施工清单）

| 门 | 实现物 | 失败行为 |
|---|---|---|
| Schema | `schemas/foreman-run.v1.schema.json` + CI validate | PR 红 |
| 墙投影 | 每 job 尾步 `foreman-run-patch.py` | job 红 |
| Artifact | `assert-artifact-complete.py` | 禁止 upload |
| Budget lint | `lint-workflow-budgets.py` 解析 `team.yml` | PR 红 |
| Replan lint | `ripgrep "failed_processes != '\\[]'"` | PR 红 |
| Assemble facts | `test-assemble-fallback.py` golden | CI 红 |
| Verdict 契约 | `verify-verdict-artifact.py` | 红 |
| Closeout | 禁 `gh issue comment ... \|\| echo`（assemble/lead 硬路径） | review grep |

---

## 8. 存量清理

| 清理项 | 动作 |
|---|---|
| 「只读 validator-stream 即可」prompt/文档 | 删除或标 v2.6 废弃 |
| 「字段直写待令牌」作为长期方案 | 改为「PAT + 墙 `closeout.project_state_written`」 |
| 状态代偿评论当权威 | 评论降级为镜像；板面字段优先 |
| 半套 verdict artifact | 新 run 不可为 replan/assemble 输入 |
| `at most N tool calls` 作唯一效率约束 | 保留提示；**控制面**改 `budgets` |
| v2.6.x 历史 run / artifact | **不回溯**（对抗审 K3） |

---

## 9. 施工顺序：同一面墙分层落地（非 S1–S7 各做 API）

| 层 | 内容 | 墙上首次可读写字段 |
|---|---|---|
| **L0** | Schema 落盘 + 空墙初始化（env-check 写入 `env`） | `env`, `foreman_mode`, `artifacts` |
| **L1** | 采认 + upload 门 + `validation` slice | P0-1, B2 |
| **L2** | `budgets` + session 包装 + adopt 与 job 结论分工 | P0-2, B1 |
| **L3** | `workers` + prep if + `replan_gate` | P1-5, P1-6, Y1 |
| **L4** | `chain` assemble 渲染 + 禁止 synthetic `fail_text` | P1-3 |
| **L5** | `closeout` 硬发布 + 写板 PAT | P1-1, P1-2, B4, B5 |
| **L6** | `foreman_mode` plan 校验 script | P2-1, Y3 |

**版本建议**：`v2.7.0` = L0–L2；`v2.7.1` = L3–L5；`v2.7.2` = L6。

---

## 10. 活验判据（可证伪）

| 判据 | 注入 / 重放 | 期望（墙字段） |
|---|---|---|
| 采认 timeout | validator droid 124 | `adoption_error=draft_timeout`，artifact `complete=false` 或含失败态 `verdict.json`，**无** stream-only |
| K 型 prep 绿 validate 杀 | 延迟 pytest + kill validate | `replan_gate` 若 `adoption_status=ok` 且 `overall!=pass` → `should_replan=true` **即使** validate job 曾为红（修后） |
| 45B 单 worker cancelled | matrix 一片 25m cancel | `workers.completed_pids` 非空 → prep **started** |
| env 板面 403 | 撤销 PAT | `env.hard_fail_count>0`，lead **skipped** |
| A4 pass 无卡 | mock `gh comment` 失败 | `closeout.comments.final_status_card.posted=false` → job **exit 1** |
| F2 | worker fail + prep success | `chain.prep.produced_required_artifact=true` → 收口**不含**「备料未启动」 |
| B5 | pick 失败兜底 | 标题无「收口」；`run_must_fail=true` |
| 编排 C1 | unattributed only | `replan_gate.should_replan=true`，不依赖 `'[]'` 字符串 |

> Run 级断言（如 `44428440695` validate success）对抗审已标**证据不足（本地未拉工件）**；施工 PR 须用新门重放，本文不宣称已 live 核实。

---

## 11. 证据索引（复核行号）

| 现象 | 位置 |
|---|---|
| upload verdict `always()` | `team.yml` L1269–1277 |
| replan 绑 validate success + `'[]'` | L1283 |
| prep skip on worker cancelled | L653 |
| worker 25m / droid 900s | L371、L461 一带 |
| assemble `chain_order` / fail_text | L2666–2700 |
| 收口 `|| warning` | L2875 |
| 兜底「收口·兜底」 | L2891–L2895 |
| PR 后 close 子单 | L2777–2794 |
| env-check 板面 WARN | `env-check.yml` L179–187 |
| `ok` 仅 HARD_FAIL | `env-check.yml` L208 |
| lead 门 | `team.yml` L49–50 |

---

## 12. 非目标与试验线 / 生产边界

### 12.1 非目标（本次方案）

- 不修改 `.github/workflows/*`、测试、业务代码。
- 不调整 `@team-droid` 触发、concurrency、计一致脚本。
- 不 merge PR、不 `@team-droid`、不创建 issue。
- 不改动 #404 / #405 历史审计支（对齐 #499 §0）。

### 12.2 试验线 vs 生产（墙上 `foreman_mode`）

| 维度 | `foreman_mode=test`（本仓默认） | `foreman_mode=prod` |
|---|---|---|
| 母工单 Open | 允许（制度） | 按 Mission |
| 工序数 | 压测可至 6 | `max_processes=3` |
| replan revise | 可引新工序 id（试验） | 禁止新 id |
| 板面 | Projects #33 + PAT | 生产板 + 裁剪 |
| 领班自拆 | 允许 | **禁止**扩 scope |

**Y3 风险**：若生产仓未显式 `prod`，仍可能抄试验宽口径——L6 施工须在 Factory Mission 仓 **默认 `prod`** 或 CI 拒绝无 mode plan。

---

## 13. 与历史 PR 关系

| PR | 关系 |
|---|---|
| #499 | 按功能分墙旧稿；**施工蓝图以本文为准** |
| #501 | 对抗审 B1–B6、Y1 已写入本文；**不修改**对抗审文件 |
| 本 PR | 仅增 `docs/领班制-整面API墙方案.md` |

---

## 14. 剩余风险（未能完全合进墙或依赖运维）

| 风险 | 说明 |
|---|---|
| PAT 轮换 | `PROJECTS_STATE_PAT` 仍依赖运维（P1-1 / Y2） |
| K1 采认失败是否 replan | 本文倾向 **人类停单**；产品未裁 |
| K2 Actions 设置读不到 WARN | 用户诉求 FAIL；可与 `env.hard_fails` 扩展 |
| 计一致脚本是否只看标题 | B5 已设计标题规范；与计一致脚本 **联审仍必要**（对抗审证据不足） |
| 历史 prompt 段批量枚举 | Y4 需施工 PR 附删除列表，本文仅定原则 |

---

*文档作者：Cloud Agent 设计回合 · 整面墙 v2.7 蓝图 · 不触发 team workflow*