# 领班制整面 API 墙 · 实现独立对抗审（PR #505）

| 字段 | 值 |
|---|---|
| 审计席 | 独立对抗审计（**非** #505 实现作者） |
| 审计对象 | [PR #505](https://github.com/hdot123/droid-mission-test/pull/505)（分支 `cursor/whole-api-wall-impl-1157`） |
| 对照蓝图 | `docs/领班制-整面API墙方案.md`、`docs/领班制-整面API墙方案-对抗审.md`（W1–W6） |
| 对照实现 | `.github/workflows/team.yml`、`env-check.yml`，`scripts/team/*`，`schemas/foreman-run.v1.schema.json`，`tests/test_foreman_wall_contract.py` |
| Actions 工件 | **本轮未拉取**；凡 run 级行为断言均标 **证据不足** |
| 本交付 | **仅增本文档**；未改 workflow / 测试 / 业务代码；未 `@team-droid`、未 merge |

---

## 1. 总判

| 维度 | 结论 |
|---|---|
| **现行 `main`（v2.6.5，#505 未合入）** | **驳回** — #503/#501 已列死法（`upload if: always()`、`replan` 绑 `validate.success`、assemble 静态 `fail_text`、评论 `|| warning`、prep 盯 `worker.cancelled` 等）**今日仍在 `main`**；本审不重复行号表，以方案 §11 为准。 |
| **按 #505 合入后的 v2.7.0 实现** | **有条件通过** — 主链已接 `foreman-run.json`、采认/upload 门、`replan_gate`、`env` PAT 硬失败、工人 delta 合并、`chain_facts` 收口、assemble 写板失败标红等，相对 v2.6.5 **实质硬化**；但 **仍有逃逸口与非零必改**，**不得**宣称「硬性 API 墙、不允许逃逸」。 |

**合一表述（用户三选一）**：**有条件通过**（针对 #505 实现语义）；若等同「已不允许任何逃逸」标准，则应视同 **驳回** 直至 §8 必改清零并经活验。

---

## 2. 用户标准符合度（一面墙 / 同一入口·产物·失败语义）

| 审度 | 结论 | 证据摘要 |
|---|---|---|
| 单一契约 `ForemanRun` | **大部分符合** | `foreman-run.v1.schema.json`、`foreman_run_lib.py`、`foreman-run-${{ github.run_id }}` 跨 job 上传；契约测试 11 用例（**本地未跑 pytest：环境无模块，以源码审阅为准**）。 |
| 同一入口（session 包装） | **未闭合** | 蓝图 §3 `foreman-run-session` 仍为 **workflow 内裸 `droid exec`**；lint **未**扫描「无 `FOREMAN_RUN_PATCH`」路径（仅 `lint_workflow_foreman.py` 禁 legacy 模式）。 |
| 同一产物 | **部分符合** | verdict upload 已改 **墙 `artifacts.*.complete` + assert**（非 `if: always()` 半套）；assemble **仍**以 `team-*` 工件目录扫描选 verdict，墙为 **可选**（`download-artifact` `continue-on-error: true`）。 |
| 同一失败语义 | **部分符合** | 采认 → `validation.*` + `job_conclusion_derived`；`human_stop` / `closeout.run_must_fail` 在采认失败路径写入 schema/脚本；但 **编排仍混用** `needs.*.result` 与 job outputs（如 prep、pick 兜底）。 |

---

## 3. W1–W6 / 逃逸口核对表

| ID | 蓝图要求 | #505 落地 | 逃逸是否仍在 |
|---|---|---|---|
| **W1** 墙唯一传递、禁双轨 | artifact 同名覆盖传递；matrix **delta 合并**（`merge_worker_deltas.py`） | **仍可能** | 多处 `download-artifact` **`continue-on-error: true`** 后 **`init_wall` 重建**（丢 `env` 等切片）；assemble **并行**信 `team-verdict-*` 与 `needs.*_RESULT`。 |
| **W2** B4 评论硬失败全覆盖 | handoff/prep/prep2、env-check 报告、assemble 主卡/兜底用 `post_comment_hard.py` | **仍可能** | **lead** 派单 `gh issue comment`（plan-comment，**无** `--hard-required`）；**replan** 双评论仍裸 `gh`；`post_comment_hard` **不写回** `closeout.comments.*`。 |
| **W3** PAT 缺失 = 硬失败 | `env-check` FAIL + `env_check_wall.py` 补 `PROJECTS_STATE_PAT` 行；`foreman_ok` 门 lead | **大部分闭合** | `Build ForemanRun wall` 步 `|| true` 可在 gate 已红时仍上传墙文件（lead 已被 `foreman_ok` 挡，**非**起跑逃逸）。 |
| **W4** validate 结论派生、禁 `validate.success` 绑 replan | `compute_validate_conclusion.py` + `lint_workflow_foreman.py`；replan `needs.validate.outputs.should_replan` | **主路径闭合** | `derive` 步 `compute_validate_conclusion \|\| true`；采认步 `adopt_verdict.py \|\| true` 使 **`steps.adopt.outcome` 恒 success**，削弱 upload 对 adopt 失败的耦合。 |
| **W5** `chain_facts` | `assemble_chain_facts.py` + schema 字段；禁 lint 静态「备料未启动」 | **已闭合（静态）** | pick 无 verdict 时仍用 **`needs.*_RESULT` 映射**补 `chain`（与墙 `chain` 可能不一致）— **证据不足**（未跑 live）。 |
| **W6** 采认失败机器门 | validate/validate2 尾步 `compute_validate_conclusion`（无 `\|\| true`）；墙 `human_stop` | **部分闭合** | assemble **不读** `human_stop` 强制停；仅依赖 validate job 红 + 收口逻辑。 |

---

## 4. 用户列举逃逸口 — 逐条

| 逃逸口 | v2.6.5 `main` 今可否 | #505 实现后 |
|---|---|---|
| `always()` / stream-only 半套 artifact | **可以** | **应堵** — upload 绑 `assert_*` + `artifacts.complete`；未上传 `validator-stream.jsonl` 为 verdict 工件。 |
| replan 回绑 `validate.result == success` 或 `'[]'` | **可以** | **应堵** — `compute_replan_gate.py` + lint 禁止；replan `if` 读 `should_replan`。 |
| validate2 与 round1 墙链不一致 | N/A | **大致镜像** — adopt2/derive2/assert2/upload2 同构；**无** round2 独立 `replan_gate`（设计允许）。 |
| 评论失败 run 仍绿 | **可以** | **部分** — 硬评论路径 assemble **fail 步未列** `closeout` 失败，但 **step 红 → job 红**（pass+评论失败应红，**活验证据不足**）；env-check 报告已 hard。 |
| 评论代偿写板；缺 PAT 不 hard_fail；写板失败不红 | **可以** | **PAT 起跑硬失败** + `project_state_write.py` 失败 → assemble `board_write.outcome == failure` → `exit 1`；收口卡 **仍写**「评论代偿记录」文案（**板面语义双轨**）。 |
| worker cancelled → prep 整段 skip | **可以** | **仍可能** — prep `if` 仍为 `worker.result` success/failure，**未**调用 `prep_should_run(wall)` / `completed_pids`（库与单测有，**workflow 未接**）。 |
| matrix last-write 互盖 | **可以** | **应堵** — delta + `workers-wall-merge`。 |
| 静态 fail_text「备料未启动」 | **可以** | **应堵** — lint + `chain_facts` 模板禁句。 |
| 采认失败无 `human_stop`/`run_must_fail` | **可以** | **脚本/schema 有**；validate job 尾步强制红。 |
| `foreman_mode` 默认 test | **可以** | **仍开放** — `vars.FOREMAN_MODE \|\| 'test'`；`validate_foreman_mode.py` 在 lead，**生产宽口径抄 test 仍可能**。 |
| 新旧产物双轨都算数 | N/A | **仍可能** — outputs `failed_processes`/`overall` 与墙并存；assemble pick **优先工件名**非墙。 |
| 兜底标题与「计一致」冲突 | **可以** | **标题已改** `汇总异常·未收口`（L3257）；与计一致脚本关系 **证据不足**（作者已承认未联审）。 |
| job 红绿代替 adoption/should_replan | **可以** | **replan 已读墙**；validate job 颜色 **派生自墙** 但 GitHub job 仍独立存在。 |

---

## 5. 已闭合项（相对 v2.6.5，实现作者主张可查）

1. **Y1 / W4**：`replan_gate.should_replan` 唯一编排；lint 禁 `needs.validate.result == 'success'` 与 `'[]'` 字符串比较。  
2. **P0-1 / B2**：`adopt_verdict.py` + `assert_artifact_complete.py` + 条件 upload（verdict/verdict2）。  
3. **W3**：`PROJECTS_STATE_PAT` 入 env 硬失败与墙 `secrets_required`。  
4. **P1-5（数据面）**：`merge_worker_deltas` 并集 `completed_pids` / `cancelled_pids`。  
5. **W5（静态）**：`assemble_chain_facts` 替代 `fail_text` 字典。  
6. **B4（子集）**：worker handoff、prep/prep2、env-check、assemble 主卡/兜底 hard 评论。  
7. **P1-1**：`project_state_write.py` + assemble 失败门。  
8. **B5（标题）**：兜底卡标题不含「收口·兜底」混称。

---

## 6. 仓内证据：说准 / 仍危险 / 证据不足

### 6.1 说准（已复核行号，#505 分支）

| 主张 | 位置 |
|---|---|
| lead 门 `foreman_ok` | `team.yml` L52–54 |
| verdict upload 非 bare `always()` | L1475–1478、L2923–2926 |
| replan `should_replan` | L1503 |
| prep 仍绑 `worker.result` | L768–771 |
| adopt / derive `\|\| true` | L1436、L1461、L2892、L2908 |
| assemble 写板失败标红 | L3240–3247 |
| env PAT FAIL | `env-check.yml` L200–203；`env_check_wall.py` L69–72 |
| 契约 lint 脚本 | `scripts/team/lint_workflow_foreman.py` |

### 6.2 作者自认 + 对抗席判定

| 项 | 作者承认 | 对抗席 |
|---|---|---|
| 未做 Actions 活验 | 是 | **维持** — 不得写「已核实 run 行为」。 |
| 写板依赖 secret/Project 字段 | 是 | env/assemble **有机器门**；工单未挂板/字段名不匹配 → **run 红**（合理），非逃逸。 |
| 计一致脚本未联审 | 是 | 标题修改 **不能** 等同计一致已闭合（**证据不足**）。 |

---

## 7. 两层结论（复述）

### 7.1 未合并 v2.6.5（`main`）

- **驳回**：#505 未合入前，错误路径 **全部仍在**。

### 7.2 #505 合入后 v2.7.0

- **升级**：从「无墙」到「墙 + 投影门」；核心 P0/Y1/B2/W3–W6 **有代码落点** 与契约测试。  
- **未达「不允许逃逸」**：§8 必改未清零；活验缺失；评论/编排/产物 **仍有第二权威**。

---

## 8. 必改清单（非零 → 不得宣称「不允许逃逸」）

| ID | 针对 | 要求 |
|---|---|---|
| **I1** | P1-5 / W1 | `prep` / `prep2` job `if` **改读墙** `workers.completed_pids`（`prep_should_run`），不得仅用 matrix `worker.result`（全 cancelled 仍 skip prep）。 |
| **I2** | W1 / §4 唯一产物 | assemble `pick` **以 `foreman-run.json` 为权威**（verdict 路径、`validation.*`、`replan_gate`）；**禁止**在墙完整时仍仅靠 `dl/team-verdict-*` + `needs.*_RESULT` 决策。 |
| **I3** | W1 | `foreman-run` 下载失败时 **fail job**，禁止 `init_wall` 静默重建（否则丢 L0 `env`）。 |
| **I4** | W2 / B4 | **lead 派单**、**replan** 评论改 `post_comment_hard.py --hard-required`；评论结果 **patch** `closeout.comments.*`。 |
| **I5** | W4 / B2 | 移除 `adopt_verdict.py` / `compute_validate_conclusion.py` 上的 **`\|\| true`**，或 upload 改读墙 `adoption_status`/`artifacts.complete`，**禁止** `steps.adopt.outcome` 假绿。 |
| **I6** | Y3 | 生产 Mission 仓：**CI 拒绝**无显式 `foreman_mode=prod` 的宽口径领班（不仅是默认 `test` 文档声明）。 |
| **I7** | §8 清存量 | 收口卡删除或改写「状态代偿记录 / 评论代偿板面」为 **仅审计镜像**，与 PAT 写板 **互斥** 叙述。 |
| **I8** | 四步法 ③ | **至少一例** 拉取 Actions 工件活验：采认失败、评论硬失败、PAT 缺失、半套 artifact 四类各 **证据不足** 直至补齐。 |

**蓝图 W1–W6 在本 PR 的映射**：W3/W5/lint/Y1 **大体落地**；W1/W2/W4 **仍有缝**；W6 **依赖 validate job 尾步**，assemble 未消费 `human_stop`。

---

## 9. 仍存逃逸口（合入后摘要）

1. **prep 门未接 `completed_pids`**（工人部分 cancelled + job failure/cancelled 组合）。  
2. **assemble 双轨选 verdict + 墙可选下载**。  
3. **adopt/derive `|| true`** 削弱步骤级失败语义。  
4. **lead/replan 评论软失败**可代偿流程继续。  
5. **`foreman_mode=test` 默认** + 收口文案仍承认评论代偿板面。  
6. **计一致 / live run** 未证。

---

## 10. 对 PR #505 的评论摘要（供线程）

1. **总判**：**有条件通过** — 相对 v2.6.5 **显著硬化**；**不得**宣称零逃逸。  
2. **`main` 现状**：未合入前仍 **驳回** 级风险。  
3. **优先必改**：**I1、I2、I5**（prep 门、assemble 权威、`\|\| true`）。  
4. 活验：**证据不足**；请补最小四类 run 工件后再申「硬墙」。  
5. 本审 **仅增** `docs/领班制-整面API墙-实现对抗审.md`，stack 于 #505。

---

## 11. 与 PR 关系

| PR | 关系 |
|---|---|
| #505 | 被审实现 |
| #503 / #501 | 蓝图与 v2.6 对抗审 |
| 本审查 PR | 仅文档，stack 于 #505 |

---

*对抗审完成；未修改任何实现文件。*