# 领班制整面 API 墙方案 · 独立对抗审

| 字段 | 值 |
|---|---|
| 审计席 | 独立对抗审计（**非** #503 方案作者） |
| 审计对象 | [PR #503](https://github.com/hdot123/droid-mission-test/pull/503) → `docs/领班制-整面API墙方案.md` |
| 基线分支 | `cursor/whole-api-wall-plan-df60`（与 #503 同支，stack 于 #503） |
| 对照材料 | `docs/领班制-API硬化修改方案.md`（#499）、`docs/领班制-API硬化修改方案-对抗审.md`（#501） |
| 对照代码 | `.github/workflows/team.yml`（**Droid Team v2.6.5**）、`.github/workflows/env-check.yml` |
| 审计方法 | 用户「整面墙」标准；Lauren Tan 四步法；#501 B1–B6 / Y1 吸收度；仓内行号逐条复核 |
| Actions 工件 | **本轮未拉取**；凡 run 级断言标 **证据不足** |
| 本交付 | **仅增本文档**；未改方案正文、workflow、测试、业务代码；未 `@team-droid` |

---

## 1. 总判

| 维度 | 结论 |
|---|---|
| **v2.6.5 现行流水线 + #503 仅设计稿（workflow 未改）** | **驳回** — #501 已证之错 **今日仍可犯**；本文档不改变任何运行时行为。 |
| **#503 作为 v2.7「整面墙」施工蓝图（未落地前）** | **有条件通过** — 相对 #499 **形态上是一面墙**（单一 `ForemanRun` / `foreman-run.v1`，`replan_gate` 合并 Y1）；#501 **B1–B6、Y1 在设计层大部写入墙字段**；但仍存在 **必改设计缺口** 与 **分层施工期逃逸口**，按现稿施工 **不能** 宣称「手边只剩正确的路」。 |

**仅此三选一：上方第二行 = 有条件通过（针对蓝图）；第一行 = 驳回（针对今日现状）。**

---

## 2. 「一整面墙」符合度（用户标准 1–2）

### 2.1 相对 #499：是否仍为「分墙换名」

| 审度 | 结论 |
|---|---|
| 文档结构 | **通过** — 硬化项落在 §6 **墙上字段表**，未再开 `adopt-verdict` / `TeamDroidSession` / `ProjectStateWriter` 等独立 API 章作为施工权威（正文仅 §1.2 列举旧名以否定）。 |
| 运行态契约 | **通过** — 根对象 **`ForemanRun`** + `schema_version: foreman-run.v1`；采认 → `validation.*`，预算 → `budgets.*`，编排 → **`replan_gate` 单对象**，收口 → `closeout.*`。 |
| 子段 `*-slice.v1` | **有条件** — `env-slice.v1` 等是 **墙内切片**，不是第二套并行 HTTP 面；但若施工按 L0–L6 **只落切片 JSON、未强制汇总进单文件 `foreman-run.json`**，会退化为 **多文件分墙**（见必改 W1）。 |
| 实现物命名 | **可接受** — `foreman-run-session`、`foreman-run-patch.py` 定位为 **读写墙的包装**，方案 §3 明确「不列为第二契约」；施工若把这些脚本的 I/O 当成权威而绕过墙，则算 **逃逸**（见 §5）。 |

**结论**：#503 **不是** #499 式「按功能并列接口换皮」；在文档意图上 **符合「一整面墙」**。风险在 **施工如何传递与合并墙实例**，不在方案目录结构。

### 2.2 同一套入口 / 产物 / 失败语义（设计稿自洽性）

| 语义 | 方案主张 | 对抗席 |
|---|---|---|
| 入口 | §3 `foreman-run-session` 唯一包装 | **说准** — 与分墙否定一致；**未写** matrix 工人是否各开 session 还是领班代写 `workers` 切片。 |
| 产物 | §4 artifact 为墙投影 + `assert-artifact-complete` | **说准** — 对准 L1269–1277 `always()` 死法；pre-upload 门为真硬化点。 |
| 失败 | §2.3.5 B1 表 + §5 禁止代偿表 | **大部说准** — 采认 vs job 颜色、replan 解耦方向正确；**validate job conclusion 推导式未写成可 lint 的布尔式**（见必改 W4）。 |

---

## 3. Lauren Tan 四步法（审 **#503 文稿**，非 v2.7 实现）

| 步 | 对 #503 方案 | 备注 |
|---|---|---|
| ① 为何能犯 | **通过** | §6 映射表 + §11 行号与仓内 **多数一致**（见 §4）。 |
| ② 改 API 拿掉错选项 | **部分通过** | 扩展 `ForemanRun` 方向对；**错选项仍在运维/PAT、默认 `foreman_mode=test`、评论镜像过渡期**（§8、§12.2）。 |
| ③ 机器守住 | **未满足** | §7 为施工清单；**仓库现状为零**（与 #501 相同）。 |
| ④ 清存量 | **偏弱** | §8 原则为主；**Y4 级 prompt 删除列表仍未枚举**（#501 应改 Y4 未闭合）。 |

---

## 4. 仓内证据：说准 / 说错 / 证据不足

### 4.1 方案引用**准确**（已复核）

| #503 主张 | 仓内对证 |
|---|---|
| validate upload `if: always()` 含 stream | `team.yml` L1269–1277 |
| replan `needs.validate.result == 'success'` + 字符串 `failed_processes` | L1283 |
| prep `needs.worker.result != 'cancelled'` | L653 |
| worker `timeout-minutes: 25` | L371 |
| lead/validate droid `600s` | L186、L1140 |
| droid 失败则 **Merge verdict** 不跑（无 `always()`） | L1095–1140 失败 → L1142 步不执行 |
| assemble `chain_order` + `fail_text.worker`「备料未启动」 | L2666–2700 |
| 收口评论 `|| warning`；pass 路径可不因评论失败标红 | L2875；L2877–2881 仅 `overall!=pass` 或 PR 失败时 `exit 1` |
| 兜底卡「收口·兜底」 | L2891–2895 |
| PR 后关子单 | L2777–2794（方案写 L2777–2797，**可接受**，已修正 #499 L2777–1797 笔误） |
| env-check 板面 WARN、`ok` 仅 `HARD_FAIL` | `env-check.yml` L179–187、L208 |
| lead 门仅 `env-check.result == success` | `team.yml` L49–50 |
| handoff/prep 评论 `|| echo` | L630、L989（方案 B4 提及 L630；**L1618/1887/2310 未逐条列入 closeout 表**） |

### 4.2 方案**不精确或证据不足**

| 条目 | 问题 |
|---|---|
| §6 P0-1「merge 依赖 judge 成功」行号 **L1095–1142** | **区间略宽**：judge 止于 L1140；merge 自 L1142。语义 **说准**。 |
| §10 / 继承 run 叙述（如 `44374403734`） | **证据不足** — 本轮未拉工件；#503 已自标，对抗席 **不二次宣称 live 核实**。 |
| `chain_facts` | §1.1 / §2.2 表承诺 `chain.*.chain_facts`，§2.3.3 JSON **无该字段** — **设计自相矛盾**（必改 W5）。 |
| B6「PR 逻辑 L2777–2797」 | 现文关单逻辑 **L2777–2794**；**非实质性错误**。 |

### 4.3 对抗席补证（#503 未写全、仍影响总判）

| 现象 | 仓内 |
|---|---|
| **overall=pass + 收口评论失败 → run 仍可绿** | L2875 吞错 + L2877 条件不覆盖「pass 无卡」— #503 B4 **意图覆盖**，但 **closeout 枚举未列 env-check 报告评论**（`env-check.yml` L245） |
| validate merge 与「采认」名实 | 现 workflow **无** `adoption_status` 字段；merge 即 verdict 产出 — #503 将采认 **入墙** 为设计增量，**非对现态误述** |
| replan 无条件 `cp .../verdict.json` | L1341 — 无 artifact 时 **cp 失败**；#503 禁止路径对证 **说准** |

---

## 5. #501 B1–B6 与 Y1 吸收度

| ID | #503 落点 | 吸收 | 对抗备注 |
|---|---|---|---|
| **B1** | §2.3.5 表 + `replan_gate.inputs_satisfied.adoption_status_ok` | **是** | 须 **W4**：validate **job** 结论推导写死，防施工回绑 `validate.result` |
| **B2** | §2.3.8 + §4 pre-upload | **是** | 依赖 `assert-artifact-complete` 真落地 |
| **B3** | §2.3.1 `hard_fail_count` + lead 读 `env.ok` | **是** | env-check **现无** `hard_fail_count` output；属 v2.7 增量 |
| **B4** | §2.3.7 `comments.*.hard_required` | **部分** | assemble 主卡/兜底、handoff **有**；**env-check 报告、prep2 handoff、lead 主评论失败** 覆盖 **不全**（W2） |
| **B5** | §2.3.7 兜底标题 + `run_must_fail` | **是** | 与计一致脚本联审仍 **证据不足**（#503 §14 自知） |
| **B6** | §6 行号 L2777–2797 | **是** | 笔误已修 |
| **Y1** | §2.3.6 **唯一** `replan_gate` / `should_replan` | **是** | 相对 #499 **实质改进**；workflow 须 **禁第二处** replan `if` |

---

## 6. 逃逸口（方案按现稿落地后仍可能成立）

| 逃逸口 | v2.6.5 今可否 | 按 #503 设计落地后 |
|---|---|---|
| stream 半套 artifact | **可以**（L1269–1277） | B2 **应堵**；分层 L1 前旧 upload 仍可能存在 |
| validate 红 → replan skip | **可以**（L1283） | `replan_gate` **应解**；采认失败故意不 replan — **缺机器化人类停单**（W6 / K1） |
| 评论失败 run 绿（pass 路径） | **可以**（L2875–2877） | B4 **应修主卡**；未列路径 **仍可能**（W2） |
| 评论代偿板面 | **可以**（L352、L2871） | P1-1 写板 + §8 清存量；**过渡期镜像** 方案自承 |
| worker cancelled → prep skip | **可以**（L653） | `workers.completed_pids` **应修** |
| `foreman_mode=test` 生产抄宽口径 | **可以** | 默认 test + L6 才 Y3 — **设计期仍开放** |
| 兜底标题 vs 计一致 | **可以**（L2891） | B5 **应修标题**；脚本是否只看标题 — **证据不足** |
| **墙实例双写**（outputs + 旧 artifact 并行） | N/A | L0–L6 分期 **高风险**；无 W1 则 **整面墙名存实亡** |
| matrix 并发 patch `ForemanRun` | N/A | 方案 **未定义** 合并语义 — **可腐蚀墙唯一性** |
| PAT 未配仍起跑 | **可以** | `secrets_required` 示例 **非** FAIL 硬门（W3 / Y2） |

---

## 7. 两层结论详表

### 7.1 现行 v2.6.5 + 仅 #503 文档

- **驳回理由**：upload `always()`、replan 绑 `validate.success`、merge 随 droid 失败而缺席、assemble 合成 `fail_text`、pass 路径吞评论、env 板面 WARN、prep 盯整 job `cancelled` 等 — **与 #501 审计一致，今日均可触发**。
- #503 **未改变** 上述任一 YAML 行。

### 7.2 #503 作为 v2.7 整面墙蓝图

**相对 #499 的升级（说准处）**：

1. 单一 **`ForemanRun`** 叙事与字段表，**非** 多 API 并列施工权威。
2. **`replan_gate` 单点** 吸收 Y1，避免 P0-2 / P1-6 双写条件。
3. B1–B6 **显式映射** §6.1，修正 #499 行号笔误。
4. artifact **投影 + complete 门** 对准半套 artifact 根因。

**仍阻止「无条件通过」的原因**：

1. **墙物理实例**（跨 job 传递、matrix 合并）未规格化 → 施工易 **墙 + 旧 outputs 并存**。
2. B4 **范围缝隙** + pass 路径 **机器式未闭合于全评论面**。
3. **Y2/Y3/Y4** 仍偏原则；默认 `test` 至 L6。
4. `chain_facts` **schema 缺口** 影响 P1-3 可验证性。
5. 四步法 ③④ 在 **文稿阶段**  inherently 未满足（与 #501 同构，不单独扣分，但 **不得** 误读为已硬化）。

---

## 8. 必改清单（非零 → 不得宣称可按现稿完成 API 硬化施工）

| ID | 针对 | 要求 |
|---|---|---|
| **W1** | §4 / §9 分层施工 | 写死 **`foreman-run.json`（或等价 artifact）唯一传递、每 job 尾步 patch 合并、matrix 工人写 `workers` 切片的并发规则**；禁止 L1–L5 与 `needs.*.outputs` / 旧 gate 字符串 **长期双轨**。 |
| **W2** | B4 / §2.3.7 | `closeout.comments`（或 env 专用段）**显式覆盖**：env-check 报告评论（`env-check.yml` L245）、prep/prep2 计划评论（L989、L2310）、worker handoff 子单（L630、L1887）；**pass 路径**任一 `hard_required` 失败 → job exit 1。 |
| **W3** | Y2 / §2.3.1 | `PROJECTS_STATE_PAT`（及写板所需 secret）**缺失 = `hard_fail_count++` 且 `env.ok=false`**，不能仅 `secrets_required` 示意对象。 |
| **W4** | B1 / validate job | 增加 **validate job `conclusion` 派生式**（逐步：precheck / session / adoption / upload），与 §2.3.5 表 **一一对应**；CI lint **禁止** replan `if` 再出现 `needs.validate.result == 'success'` **作为采认已成功之后的唯一条件**。 |
| **W5** | P1-3 / §2.3.3 | `chain.<job>` **补齐 `chain_facts` 结构与枚举**（与 `downstream_blocker` 分工），并列入 `schemas/foreman-run.v1.schema.json` 施工验收项。 |
| **W6** | K1 / 人类停单 | `adoption_status=failed` 时 **`closeout.run_must_fail=true`** 或墙内 **`human_stop: true` + 工单评论模板码**；不得仅 assemble 散文「人类停单」而无字段门。 |

**#501 B1–B6 视为已写入墙字段，但 W2/W4/W6 为整面墙形态下 **仍缺的一圈机器边界**；施工前须并入蓝图或施工 PR 首包。**

### 8.1 应改（不阻断「有条件通过」，但影响焊死程度）

| ID | 内容 |
|---|---|
| **Y2′** | 与 W3 合并落地顺序：env-check 先于 lead，secret 探针失败 **不可 WARN 起跑**。 |
| **Y3′** | §12.2：本试验仓可默认 `test`，但文档须 **强制**「生产 Mission 仓 CI 拒绝无 `foreman_mode` 的 plan」为 L6 **阻塞项**。 |
| **Y4′** | §8 附 **v2.6 prompt 删除列表**（efficiency 句等），非仅「保留提示」。 |
| **Y5′** | 明确 **round2** 子树与 `validation.round` / `replan_gate` 在第二轮的 **只读墙字段**，防 validate2 再开平行契约。 |

---

## 9. 对 PR #503 的评论摘要（供线程）

1. **总判（蓝图）**：**有条件通过** — 形态上 **是一面墙**，Y1/B1–B6 **大部吸收**；**W1–W6 必改** 前不得宣称可按现稿硬化完工。
2. **总判（今日现网）**：**驳回** — workflow 未动，错仍可犯。
3. **相对 #499**：对抗席 **不认定**「分墙换名」；认定 **设计意图为单一 `ForemanRun`**。
4. **相对 #501**：逃逸口表 **大部分继承**；#503 **闭合了 Y1 与接口并列问题**，**未闭合**墙传递、B4 全覆盖、Y2/Y4。
5. Run 级活验：**证据不足**（未拉工件）。

---

## 10. 与 PR 关系

| PR | 关系 |
|---|---|
| #503 | 被审方案 |
| #501 | B1–B6/Y1 对照源；**不修改** #501 文件 |
| 本分支 | 仅增 `docs/领班制-整面API墙方案-对抗审.md`，stack 于 #503 |

---

*独立对抗审 · 未触发 team workflow · 未改 `docs/领班制-整面API墙方案.md` 正文*