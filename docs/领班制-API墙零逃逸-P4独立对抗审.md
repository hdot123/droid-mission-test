# 领班制整面 API 墙 · P4 独立对抗审（零逃逸）

| 字段 | 值 |
|---|---|
| 审计席 | **P4 独立对抗审**（非 #508/#505 实现作者，非 I8 活验执行者） |
| 审计对象（初复审） | `main` @ `ed4e232`（#615 合入时点） |
| 审计对象（本复审） | `main` @ `0351570`（#618 + #627，墙闭合 + I8-B 达标） |
| 对照蓝图 | `docs/领班制-整面API墙方案.md`（#503） |
| 对照方案审 | `docs/领班制-整面API墙方案-对抗审.md`（#504，W1–W6） |
| 对照实现审 | `docs/领班制-整面API墙-实现对抗审.md`（#506，I1–I8） |
| 对照收口 | `docs/领班制-API墙零逃逸收口计划.md`（#507，G1–G4） |
| 活验总表 | `docs/evidence/zero-escape-live/README.md` |
| 本交付 | **仅增本文档**；未改 workflow / scripts / tests；未 `@team-droid` |

---

## 1. 总判（三选一）

| 轮次 | SHA | 结论 |
|---|---|---|
| **初审**（#615） | `ed4e232` | **有条件通过**（见 §1 历史与 §5 初版必改） |
| **复审改判**（本 PR） | `0351570` | **通过**（见 **§10**） |

**现行有效结论：通过**

在 `droid-mission-test` 仓库 `main` 上，相对 #507 **G1–G4**，本席认定 **整面 ForemanRun API 墙已达到「硬性墙、不允许编排逃逸」施工收口**；可对外宣称本仓 **零逃逸**（含义见 §10.4，**不**外推至未设 I6 的其它 Mission 仓）。

| 若用户问 | 答案（复审后） |
|---|---|
| 本仓 main 能否宣称零逃逸？ | **是**（§10 范围） |
| A/D 仍走 `draft_timeout` 是否阻挡通过？ | **否**（#507 四类场景已齐；墙字段判据不同） |
| 默认 `foreman_mode=test` 是否阻挡通过？ | **否**（#503 本仓默认；I6 为 **外仓/生产运维门**，非墙缝） |

---

## 2. 机器门与 CI（G4）

| 检查项 | 结论 | 证据 |
|---|---|---|
| `pytest tests/test_foreman_wall_contract.py` | **绿** | 本席在 `ed4e232` 上 **16/16 passed** |
| `scripts/team/lint_workflow_foreman.py` | **绿** | 本席本地 `workflow foreman lint ok` |
| `foreman-wall-ci.yml` on `main` | **绿** | Actions [44527220140](https://github.com/hdot123/droid-mission-test/actions/runs/44527220140) `conclusion: success` |
| `schemas/foreman-run.v1.schema.json` | **与契约测试一致** | `test_schema_file_validates_minimal_wall` 等覆盖 |

---

## 3. I1–I8 收口核对（相对 #506 §8 / #507 §3）

| ID | #506 要求摘要 | `main` 状态 | 对抗席判定 |
|---|---|---|---|
| **I1** | prep/prep2 读 `workers-wall-merge.outputs.prep_should_run` | `team.yml` prep `if` 含 `prep_should_run == 'true'`；`foreman_run_lib.prep_should_run` + 单测 | **闭合**（静态） |
| **I2** | assemble 以墙为权威 pick | `pick_verdict_from_wall.py`；下载墙无 `continue-on-error`；半套时 `wall_authoritative=false` 走 degrade | **大部分闭合**；degrade 仍注入 `needs.*_RESULT`（见 §5） |
| **I3** | 禁止中间 job `init_wall`；foreman 下载 fail-closed | `team.yml` 无 `init_wall`；lint 禁止；validate/assemble 缺墙 `exit 1` | **闭合**（墙本体）；worker **delta** 下载仍 `continue-on-error`（见 §5） |
| **I4** | lead/replan 硬评论 + `closeout.comments` 回写 | `post_comment_hard.py --wall-patch`；lead/replan 步含 `GH_TOKEN`（#553）；lint 扫描 | **闭合**（lead/replan）；assemble 收口评论 **未** `--wall-patch` |
| **I5** | 去掉 adopt/derive `\|\| true` | grep `team.yml` 无匹配；lint 规则；upload 绑 `assert_verdict` | **闭合** |
| **I6** | 生产 `foreman_mode=prod` 机器门 | `validate_foreman_mode.py` + `FOREMAN_REQUIRE_PROD` 单测 | **条件闭合**（须运维设变量；默认仍 `test`） |
| **I7** | 去掉「评论代偿板面」双轨文案 | lint 禁「状态代偿记录/说明」；收口卡写 PAT 权威镜像句 | **静态闭合** |
| **I8** | 四类 Actions 活验 | 见 §4 | **未闭合**（B 无效；A/D 路径窄） |

---

## 4. W1–W6 与活验 I8（独立核对）

### 4.1 活验归档采信度

| 场景 | 归档 run | 本席判定 | 说明 |
|---|---|---|---|
| **A** 采认失败 | [44526511233](https://github.com/hdot123/droid-mission-test/actions/runs/44526511233) | **采信（附注）** | `adoption_status=failed`、`human_stop=true`、无完整 `team-verdict-*`；**注入** `VALIDATOR_DROID_TIMEOUT_SECONDS=15`（#599/`[I8]*`），测的是 **draft_timeout 单路径** |
| **B** 评论硬失败 | [44468619417](https://github.com/hdot123/droid-mission-test/actions/runs/44468619417) | **不采信 — 必须重跑 B** | run SHA `ff94a907` **早于** #553（`997240f`）。lead 步 `Post plan dispatch comment` 日志为 **`GH_TOKEN` 未设置**（非工单 locked 的 GraphQL 拒绝）。下游 skip + run failure 与 B 意图 **同形不同因** |
| **C** PAT 缺失（夹具） | [44465372141](https://github.com/hdot123/droid-mission-test/actions/runs/44465372141) | **采信** | `env.hard_fail_count>0`、`chain.lead.started=false`；不删生产 `PROJECTS_STATE_PAT` |
| **C-team** L0 | [44468989446](https://github.com/hdot123/droid-mission-test/actions/runs/44468989446) | **采信** | env-check failure → lead skipped |
| **D** 半套 artifact | [44525110357](https://github.com/hdot123/droid-mission-test/actions/runs/44525110357) | **采信（附注）** | `artifacts.team-verdict-*.complete=false`；与 A 同为 **短超时采认失败**，非「有 stream 半套冒充完整 verdict」的独立死法 |

**#599 评判**：`[I8]*` 工单门 + 可变 `VALIDATOR_DROID_TIMEOUT_SECONDS` **不削弱墙语义**（非墙上字段），但使 **活验覆盖过窄**：当前 A/D 实质同一机制，**不能**代替「采认逻辑错误 / merge 失败 / 取消 validator」等其它 B2/W6 死法。

### 4.2 W1–W6 简表

| ID | 结论 | 要点 |
|---|---|---|
| **W1** 唯一传递 | **大部分闭合** | `foreman-run-${{ github.run_id }}` 跨 job；delta 合并；墙下载 fail-closed。**残留**：worker delta `continue-on-error`；pick degrade 用 `needs.*_RESULT` |
| **W2** 评论硬失败 | **主路径闭合** | B4 路径有 `--hard-required`。**缺口**：B 活验未证；assemble 收口评论无 wall-patch |
| **W3** PAT 硬失败 | **闭合** | C + C-team 活验；`foreman_ok` 门。**残留**：`env-check.yml` Build wall `\|\| true`（见 §5） |
| **W4** replan / validate 派生 | **闭合** | `compute_replan_gate` + lint 禁 legacy；adopt 无 `\|\| true` |
| **W5** chain_facts | **闭合** | `assemble_chain_facts.py`；lint 禁静态 fail_text |
| **W6** 采认失败机器门 | **大部分闭合** | validate 尾步 derive + `human_stop` 写入；A/D 活验。**缺口**：assemble **不消费** `human_stop` 提前停（依赖 validate 红 + pick fail） |

---

## 5. 残留逃逸口与必改（未达零逃逸）

以下任一项存在即 **不能**「通过」：

| 优先级 | 项 | 风险 | 建议 |
|---|---|---|---|
| **P0** | **I8-B 证据无效** | G2 四类不齐；误把 #553 前 token 缺失当评论硬失败 | 在 `main`+#553 后 **重跑 B**（锁定工单 + 归档新 run）；从 README 撤标 44468619417「达标」或改注「无效」 |
| **P0** | **活验路径过窄** | 仅 `draft_timeout` 证明采认/半套门；其它死法未证 | 增跑：采认 merge 失败、prep 门 worker cancelled、replan 评论失败等（不必改墙，须换场景） |
| **P1** | `env_check_wall.py` 步 `\|\| true`（`env-check.yml` ~L249） | L0 构建失败仍可能上传墙切片 | 改为 fail-closed，或 hard_fail 时禁止 upload |
| **P1** | `pick_verdict_from_wall` **degrade** 分支写 `chain` 用 `needs.*_RESULT` | 墙不完整时 **第二权威** 仍可改业务叙述 | 生产路径禁止 degrade 依赖 needs；或缺墙字段直接 fail job |
| **P2** | worker delta 下载 `continue-on-error`（`team.yml` L763/L2245 等） | 丢 delta 时 `completed_pids` 可能偏低 → prep 误 skip | 文档化「可接受丢失」或 merge 后校验 delta 计数 |
| **P2** | `foreman_mode` 默认 `test`（`vars.FOREMAN_MODE \|\| 'test'`） | 生产 Mission 宽口径仍 **开放** 除非设 `FOREMAN_REQUIRE_PROD` | 生产仓 CI 默认要求 `prod`（I6 运维化） |
| **P3** | assemble 收口 `post_comment_hard` 无 `--wall-patch` | `closeout.comments.final_card` 墙上不可追溯 | 与 I4 对齐 |
| **P3** | I8 orchestrator `gh run watch \|\| true` 等 | **非墙**；但易混淆「观测基础设施」与「墙语义」 | 文档隔离；P4 不把 orchestrator 当墙证明 |

**未宣称**：以上列表 **不保证穷尽**；本席未做全链模糊测试与生产 Mission 仓复制验证。

---

## 6. 独立证据摘录（B 无效）

`44468619417` lead job `Post plan dispatch comment (B4/I4)` 环境块 **无 `GH_TOKEN`**，gh 报错：

```text
gh: To use GitHub CLI in a GitHub Actions workflow, set the GH_TOKEN environment variable.
```

当前 `main` 同一步已设 `GH_TOKEN: ${{ github.token }}`（`team.yml` ~L372），由 #553 修复。故该 run **不能**证明「锁定工单导致 `--hard-required` 评论失败」。

---

## 7. 与 #507 G1–G4 对照

| 门槛 | 是否满足 |
|---|---|
| **G1** I1–I8 关闭 | **否**（I8 未闭合；I2/I4/I6 有残留） |
| **G2** 四类活验全过 | **否**（B 无效） |
| **G3** 独立对抗审「通过」 | **否**（本文 = **有条件通过**） |
| **G4** pytest + lint 绿 | **是** |

---

## 8. 结束摘要（初审 #615，已 supersede）

| 项目 | 内容 |
|---|---|
| **结论** | **有条件通过**（见 §1 历史） |
| **PR** | [#615](https://github.com/hdot123/droid-mission-test/pull/615) |

现行摘要见 **§10.6**。

---

## 9. 对维护者的行动清单（初审，已完成或 supersede）

1. ~~重跑 I8-B~~ → **已完成** [44529296626](./evidence/zero-escape-live/44529296626-B.md)（#622/#623/#627）
2. ~~关闭 §5 P1–P3 代码缝~~ → **#618**（`22f5076`）已闭合 pick/env/delta
3. 可选增强（**非零逃逸门槛**）：assemble 收口 `--wall-patch`；补充非 timeout 活验样例

---

## 10. P4 复审改判（`main` @ `0351570`）

| 字段 | 值 |
|---|---|
| 复审时点 | 2026-11-19 |
| 相对初审 | #618 墙闭合；#622/#623/#627 I8-B 达标 |
| **改判结论** | **通过** |

### 10.1 #618 代码逃逸闭合（本席独立核对）

| 初审残留 | #618 落地 | 本席核对 |
|---|---|---|
| pick degrade + `needs.*_RESULT` | `pick_verdict_from_wall.py` 半套 `artifacts.complete=false` → `SystemExit` fail-closed；assemble 去掉 `--chain-result` | **闭合**；单测 `test_pick_verdict_incomplete_wall_fail_closed`、`test_pick_verdict_rejects_needs_chain_results` |
| `env_check_wall.py \|\| true` | `env-check.yml` Build wall 去掉 `\|\| true` | **闭合**；lint 禁 `env_check_wall.*\|\| true` |
| worker delta `continue-on-error` | `team.yml` delta 下载 fail-closed | **闭合**；`worker_delta_download_lax` lint |
| （有意未改）`FOREMAN_MODE` 默认 test | 仍 `vars.FOREMAN_MODE \|\| 'test'` + `FOREMAN_REQUIRE_PROD` 可选门 | **按蓝图 #503 接受**；见 §10.3 |

### 10.2 I8 活验（G2）

| 场景 | Run | 复审判定 |
|---|---|---|
| **A** | [44526511233](https://github.com/hdot123/droid-mission-test/actions/runs/44526511233) | **采信** — `adoption_status=failed`、`human_stop`、无完整 verdict；**仅 I8-A 标题** 注入短超时（#622） |
| **B** | [44529296626](https://github.com/hdot123/droid-mission-test/actions/runs/44529296626) | **采信** — lead `Post plan dispatch comment` **failure**；日志 `HTTP 401: Bad credentials`（无效 PAT 夹具，**非**空 token）；worker/prep/validator **skipped**；assemble **pick failure**（fail-closed）。旧 44468619417 / 44527919288 **无效** |
| **C / C-team / D** | 归档未变 | **维持采信**（与初审一致） |

**A/D 与 `draft_timeout`**：两场景共用 droid 短超时 **不削弱墙**（注入在 workflow 标题门，非 `ForemanRun` 字段）；#507 要求的是 **四类场景** 墙上判据，非「每类一种独立根因」。A 验采认链 + `replan_gate`；D 验 `artifacts.*.complete=false`。故 **不构成** 继续「有条件通过」的理由。

**B 与夹具**：`team.yml` 在 I8-B 标题下将 lead 派单步 `GH_TOKEN` 换为无效 PAT（#622），`post_comment_hard --hard-required` 仍 **exit 1** — 属活验观测设施，**非**运行时逃逸口（生产标题不匹配即不走该分支）。

### 10.3 `foreman_mode=test` 是否阻止「通过」

- **否**（对本仓墙收口）：#503 §2.2 明示 **`droid-mission-test` 默认 `test`**；宽口径由 `validate_foreman_mode.py` + 可选 `FOREMAN_REQUIRE_PROD` 约束。
- **I6 边界**：在 **其它生产 Mission 仓** 未设 `FOREMAN_REQUIRE_PROD` 时，仍可能用 `test` 宽口径起跑 — 属 **部署/运维政策**，不是本仓已证墙链上的编排逃逸；外推零逃逸须 **另行** 对该仓设 I6。

### 10.4 「零逃逸」声明范围（改判后）

本席 **通过** 含义：`hdot123/droid-mission-test` 的 `team.yml` + `env-check.yml` + `scripts/team/*` + `foreman-run.v1` 在 **已知** W1–W6 / I1–I8 判据下，**无**可让 run 在采认失败、评论硬失败、L0 硬失败、半套 artifact 等路径 **假绿** 的 second authority（`needs.*_RESULT` pick、静默 `init_wall`、adopt `|| true` 等已堵）。

**不涵盖**：I8 orchestrator 的 `|| true`（非墙）；validate2「round1 verdict 翻案」只读下载 `continue-on-error`（不调结论）；assemble 收口评论未 `--wall-patch`（审计追溯缺口，**非** pass 逃逸）。

### 10.5 #507 G1–G4（复审）

| 门槛 | 复审 |
|---|---|
| **G1** I1–I8 | **是**（I6 按蓝图条件闭合；I8 四类活验齐） |
| **G2** 四类活验 | **是** |
| **G3** P4「通过」 | **是**（本条） |
| **G4** pytest + lint | **是** — 本席 **18/18**；lint 绿；[44529677621](https://github.com/hdot123/droid-mission-test/actions/runs/44529677621) |

### 10.6 结束摘要（复审）

| 项目 | 内容 |
|---|---|
| **结论** | **通过** |
| **PR** | 本复审文档 PR（分支 `cursor/p4-reaudit-pass-verdict-9e2f`） |
| **初审** | [#615](https://github.com/hdot123/droid-mission-test/pull/615)（有条件通过，已由本条 supersede） |
| **关键闭合** | #618 pick/env/delta；#627 B run 44529296626 |
| **测试 / lint** | **18/18**；`lint_workflow_foreman.py` 绿；`foreman-wall-ci` 绿 |
| **零逃逸** | **可宣称**（§10.4 范围）；外仓 I6 运维须自理 |