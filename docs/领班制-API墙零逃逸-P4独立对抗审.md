# 领班制整面 API 墙 · P4 独立对抗审（零逃逸）

| 字段 | 值 |
|---|---|
| 审计席 | **P4 独立对抗审**（非 #508/#505 实现作者，非 I8 活验执行者） |
| 审计对象 | `main` @ `ed4e232`（v2.7.0 墙合入 #508 及后续至 #614） |
| 对照蓝图 | `docs/领班制-整面API墙方案.md`（#503） |
| 对照方案审 | `docs/领班制-整面API墙方案-对抗审.md`（#504，W1–W6） |
| 对照实现审 | `docs/领班制-整面API墙-实现对抗审.md`（#506，I1–I8） |
| 对照收口 | `docs/领班制-API墙零逃逸收口计划.md`（#507，G1–G4） |
| 活验总表 | `docs/evidence/zero-escape-live/README.md` |
| 本交付 | **仅增本文档**；未改 workflow / scripts / tests；未 `@team-droid` |

---

## 1. 总判（三选一）

**结论：有条件通过**

按 #507 G1–G4：**不得**宣称「硬性 API 墙、不允许逃逸」或「零逃逸」。相对 v2.6.5 与 #506 对 #505 的「有条件通过」，当前 `main` 上 **I1–I7 在代码与契约层大部分闭合**，活验 **A/C/C-team/D 可采信但有路径局限**；**I8 场景 B 归档不达标**（必须重跑）。墙尚未达到「真正零逃逸」的 **通过** 门槛。

| 若用户问 | 答案 |
|---|---|
| 能否 merge 后对外说零逃逸？ | **否** |
| 墙相对 #508 初版是否实质硬化？ | **是** |
| 是否建议停跑生产宽口径领班？ | 在补齐 B 活验与下表必改前，**不应**把本仓当「零逃逸已证」 |

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

## 8. 结束摘要

| 项目 | 内容 |
|---|---|
| **结论** | **有条件通过**（非通过；非驳回 v2.7 墙整体回退） |
| **PR** | 由本席分支 `cursor/p4-zero-escape-adversarial-audit-9e2f` 提交（见下方 merge 后链接） |
| **关键残留** | B 活验必须重跑；A/D 仅 timeout 路径；env `|| true`、pick degrade、delta continue-on-error、`foreman_mode` 默认 test |
| **测试 / lint** | 契约 **16/16 绿**；`lint_workflow_foreman.py` **绿**；`foreman-wall-ci` on `main` **绿** |
| **零逃逸** | **不得宣称**；仅当 G1–G4 全绿且本席改判「通过」后方可 |

---

## 9. 对维护者的行动清单（最短）

1. **重跑 I8-B**（#553 后 `main`，锁定工单），更新 `docs/evidence/zero-escape-live/` 与 README。
2. 为 A/D **之外**至少再增一例采认/评论/replan 死法活验（不依赖 `VALIDATOR_DROID_TIMEOUT_SECONDS`）。
3. 择期关闭 §5 P1–P3 代码缝（单独 PR，**不得**为凑绿削弱墙）。