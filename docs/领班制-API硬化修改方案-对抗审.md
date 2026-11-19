# 领班制 API 硬化修改方案 · 第二轮对抗审

| 字段 | 值 |
|---|---|
| 审计席 | 独立对抗审计（非方案作者） |
| 审计对象 | [PR #499](https://github.com/hdot123/droid-mission-test/pull/499) → `docs/领班制-API硬化修改方案.md` |
| 基线分支 | `cursor/foreman-api-hardening-plan-7ca0`（与 #499 同支） |
| 对照代码 | `.github/workflows/team.yml`（**Droid Team v2.6.5**）、`.github/workflows/env-check.yml`（当前 `main` 同 SHA 一致） |
| 审计方法 | Lauren Tan API 硬化四步法；仓内 grep/读行；方案叙述与 YAML 行号逐条核对 |
| 本交付 | **仅本文档**；未改 workflow/测试/业务代码；未 `@team-droid` |

---

## 1. 总判

| 维度 | 结论 |
|---|---|
| **v2.6.5 现行流水线 + PR #499 仅设计稿** | **驳回** — 犯过的错**今仍可犯**；方案未改变任何 API/工作流行为。 |
| **方案作为 v2.7 施工蓝图（未落地前）** | **有条件通过** — 根因刻画与多数仓内引证**成立**，P0/P1 方向与四步法对齐；但存在**必改设计缺口**、**证据笔误**与**逃逸口未闭合**项，按现稿施工无法保证「手边只剩正确的路」。 |

**Lauren 四步法对方案文稿的审度（不是对 v2.7 实现）：**

| 步 | 方案自身 |
|---|---|
| ① 为何能犯 | **通过** — 各条与 v2.6.5 行为匹配度高。 |
| ② 改 API | **部分通过** — 抽象命名清晰，但多处仍靠 **PAT/人配 secret、评论镜像、prompt 保留** 作二级控制。 |
| ③ 机器守 | **未满足** — 本文档性质为设计；硬化脚本/workflow 变更在「非目标」中明确不做。 |
| ④ 清存量 | **偏弱** — 多条写「改 prompt/文档」；与方法论「禁止文档当控制面」存在张力。 |

---

## 2. 仓内证据核对（方案说准 / 说错）

### 2.1 方案引用**准确**（已复核行号）

| 方案主张 | 仓内对证 |
|---|---|
| validate `Upload verdict artifact` 为 `if: always()`，且 path 含 `verdict.json` + `work/validator-stream.jsonl` | `team.yml` L1269–L1277 |
| droid 600s 杀在 merge 之前；merge 无 `if: always()` | L1095–L1142：validator droid 步失败则 **Merge verdict 不跑** |
| replan 要求 `needs.validate.result == 'success'` | L1283 |
| replan `cp dl/team-verdict-*/verdict.json` | L1341 |
| worker `timeout-minutes: 25`；droid `900s` | L371、L461 |
| lead/validate job `timeout-minutes: 15`；lead/validate droid `600s` | L52、L186；L997、L1140 |
| prep 因 `needs.worker.result != 'cancelled'` 跳过 | L653 |
| assemble 无 verdict 时 `chain_order` + `fail_text.worker`「备料未启动」 | L2666–L2700 |
| assemble 收口评论 `|| echo "::warning::"` | L2875；兜底卡 L2895 |
| lead/assemble「状态代偿记录」仅评论 | L352、L2871 |
| env-check 板面失败为 WARN、`ok` 仅看 `HARD_FAIL` | `env-check.yml` L179–L187、L208 |
| `PYTEST_FULL_TIMEOUT = 600` | `team.yml` L710 |
| 版本头 v2.6.5 | `team.yml` L1 |

### 2.2 方案**笔误或与仓内不符**

| 条目 | 问题 | 证据 |
|---|---|---|
| **P1-2 ②**「L2777–**1797**」 | 明显行号笔误 | PR 逻辑在 L2777–L2797（`gh pr create` / close 子单） |
| **§0.2 job 链**「validate droid 600s, **job 15m**」 | 未强调 **15m 内需塞 precheck + droid + merge + upload** | validate 步序 L1008–L1277；与 P0-2 预算叙事有关但 §0.2 易误读为有余量 |
| **P0-2 ⑤**「第 45 轮 A run `44428440695` validate success」 | 本轮**未下载 Actions 工件复核** | 标 **证据不足（本地）**；不否定方案，但审计席不能二次证实 run 级结论 |

### 2.3 方案未写全、审计席补证的现行死法

| 现象 | 仓内补充 |
|---|---|
| **validate job 红 + replan skip + assemble 合成理由** | validate failure → replan L1283 不触发 → assemble L2666+ 仍可贴「收口」评论（含误导 `fail_text`） |
| **overall=pass 但评论失败仍可能 run 绿** | L2875 吞评论失败；L2877–L2881 仅在 `overall != pass` 或 PR 失败时 `exit 1` → **pass 且无收口评论仍可绿**（#A4 核心） |
| **兜底卡标题仍含「收口」** | L2891「团队状态卡（收口·兜底）」正文写「未收口」→ 与计一致/人读标题冲突（方案 P1-2 未点名） |
| **handoff/prep/replan 评论失败可吞** | L630、L989、L1618 等 `|| echo` — **P1-2 清扫范围偏窄** |
| **env-check 报告评论失败可吞** | `env-check.yml` L245 |

---

## 3. 已知死法：方案是否**设计级**焊死

| 死法 ID | v2.6.5 现状 | 方案条目 | 设计是否闭合 | 对抗备注 |
|---|---|---|---|---|
| 补 18 采认链 | **仍开放** — stream-only artifact 可能上传 | P0-1 | **大体闭合** | 须定义 `adoption_status`/`adoption_error` 与 **validate job 结论**（见必改 1–2） |
| 补 10 / 600s K 型 | **仍开放** — merge 不跑、无 verdict | P0-2 + P0-1 | **依赖 P0-1** | `TeamDroidSession` 为包装层；**真硬化在 adopt + upload 门** |
| 自动写板 | **仍开放** — 仅评论 | P1-1 | **未闭合** | 新 secret `PROJECTS_STATE_PAT` = **运维自觉**；未 PAT 则仍 WARN（至 P1-4 落地） |
| A4 必贴收口 | **仍开放** | P1-2 | **部分闭合** | 未覆盖 handoff/prep；未禁止「收口·兜底」标题假阳 |
| F2 理由撒谎 | **仍开放** | P1-3 | **闭合有条件** | 依赖 P0-1 禁止无 artifact 猜 `fail_text`；单测 golden 可守 |
| env-check 板面 WARN | **仍开放** | P1-4 | **设计闭合** | 需新增 PAT 探针 + `hard_fail_count` **output**（方案 L258 提及但 env-check **无此 output 现态**） |
| 45 轮 worker 25m → prep skip | **仍开放** | P1-5 | **设计闭合** | matrix 聚合 + prep if 改造逻辑自洽 |
| replan `success` 门 + 字符串 `[]` | **仍开放** | P0-2③、P1-6 | **设计闭合** | P1-6 与 P0-2 对 replan 条件需**合并为一处规范**（见应改 3） |

---

## 4. 逃逸口检索（方案落地后仍可能成立者）

| 逃逸口 | 现 v2.6.5 | 按**现方案稿**落地后是否仍可走 |
|---|---|---|
| 假绿：无收口评论但 run 绿 | **可以**（pass + comment 吞） | P1-2 修 assemble **主卡**；**仍可能**若未改 pass 路径 hard publisher |
| 评论代偿当权威板面 | **可以** | P1-1 后板面优先；**试验线过渡期**方案自承「评论镜像」→ 代理仍可只读评论 |
| stream 冒充 verdict | **可以**（artifact 半套） | P0-1 upload 门 **应堵住**；replan/assemble 须禁 fallback 猜理由 |
| validate 红 → replan skip | **可以** | P0-2 解耦 **若**采认成功；采认失败 `adoption_status!=ok` 时 **故意**不 replan — OK，但须 **人类停单 API**，方案仅散文描述 |
| job 绿时 skip replan（overall 未写出） | **边缘** — merge 不跑则 outputs 空，replan 不因 success 误触 | adopt 后 outputs 必有；**须** schema 门防半套 |
| worker cancelled 拖死 prep | **可以** | P1-5 **应堵住** |
| 试验线 pass 母单 Open **逃避收口** | 制度允许 Open | P1-2 要求母单必贴卡 — **与 0.1 一致**；但 **PR 不合并** 仍可 overall=pass run 红，不算假绿 |
| `foreman_mode=test` 宽口径被生产抄 | **可以** | P2-1 **默认 test** — 生产裁剪未强制 |

---

## 5. 「改了 API」vs「只多写规则」

| 方案条目 | 真 API/机器 | 仍靠文档/自觉/运维 |
|---|---|---|
| P0-1 adopt-verdict | workflow 步序 + schema + upload 条件 | `adoption_error` 枚举需人维护 |
| P0-2 TeamDroidSession | 预算 lint 脚本 | prompt「at most N tool calls」仅降级为提示 |
| P1-1 ProjectStateWriter | assemble 写板失败 exit 1 | **PAT 签发与轮换** |
| P1-2 CloseoutPublisher | exit 1 | 范围不全（见必改 4） |
| P1-3 AssembleChainFacts | Python 单测 | 模板渲染仍需人审 golden |
| P1-4 env-check | HARD_FAIL 扩展 | PAT 配置 |
| P1-5 WorkerMatrixResult | prep if + summary artifact | — |
| P1-6 team-gate-*.json | lint 禁 `!= '[]'` | — |
| P2-1 foreman_mode | plan validate 脚本 | **默认 test** |

---

## 6. 试验线 / 生产正形串位风险

- 方案 **0.1** 写明试验线可 Open、PR 可不合并 — **与 P1-2「母工单必贴收口卡」不冲突**（制度≠关单）。
- 风险：agent 将「失败不关单」误读为「可无收口卡」— 现行 assemble **必跑**（L2598 `always()`）且尽量贴卡，但 A4 漏洞可导致 **无卡仍绿**。
- **foreman_mode 默认 test**（P2-1）：生产正形若未显式 `prod`，方案**不能**防止抄 6 工序宽口径 — 属逃逸口。

---

## 7. 分级清单

### 7.1 必改（零则施工不得宣称 API 硬化完成）

| ID | 针对 | 要求 |
|---|---|---|
| **B1** | P0-1 / P0-2 | 明确规定：`adopt-verdict` **exit 0 且必产出 schema 合法 `verdict.json`**（含采认失败态）；`validate` job 红/绿与 `adoption_status` 分工写死，避免「采认成功但 job 仍 failure → replan 仍 skip」矛盾。 |
| **B2** | P0-1③ | `upload-verdict` 条件与「artifact 要么完整要么不存在」：禁止 `actions/upload-artifact` 在缺文件时**静默少传**（现 L1270–L1277 行为）；需 pre-upload 断言或分步上传。 |
| **B3** | P1-4③ | `env-check` 增补 **`hard_fail_count`（或等价）output**，`team.yml` lead 门与方案叙述一致；不仅 `result == success'`。 |
| **B4** | P1-2 | **CloseoutPublisher 范围**扩至所有工单可见「状态/收口」评论路径（至少 assemble 主卡+兜底卡、lead 派单卡）；pass 路径评论失败必须 fail job。 |
| **B5** | P1-2 / 计一致 | 禁止或重命名 `团队状态卡（收口·兜底）` 标题，避免「未收口」正文与「收口」标题同时满足计一致脚本（若脚本只看标题 — **证据不足**，须与计一致脚本联审）。 |
| **B6** | 文稿 | 修正 P1-2 行号 **L2777–1797 → L2777–2797**。 |

### 7.2 应改

| ID | 内容 |
|---|---|
| **Y1** | P0-2 与 P1-6 **合并 replan 触发契约**（job 结果 + gate artifact + `adoption_status` + `overall` + unattributed），避免两处条件漂移。 |
| **Y2** | P1-1：`PROJECTS_STATE_PAT` 缺失纳入 env-check **FAIL**（与 P1-4 同步写清顺序）。 |
| **Y3** | P2-1：生产仓 **默认 `foreman_mode=prod`** 或 CI 拒绝无 mode 的 plan 落盘。 |
| **Y4** | 存量清理：列出 v2.6.5 prompt 中仍鼓励 **efficiency/工具次数** 的段落，标为 v2.7 删除列表（不只散文「保留但非控制面」）。 |

### 7.3 可议

| ID | 内容 |
|---|---|
| **K1** | 采认失败是否允许 replan（现方案倾向人类停单） — 需产品裁决。 |
| **K2** | env-check 仓库 Actions 设置读不到时 WARN vs FAIL（方案偏用户诉求 FAIL；现 L141 WARN）。 |
| **K3** | 历史 run artifact 不回溯 — 接受。 |

---

## 8. 对 PR #499 的对抗审结论（摘要）

1. **方案作为故障百科 + 改造蓝图质量偏高**，与 v2.6.5 仓内契约**多数一致**，P0-1/P0-2/P1-5/F2 根因链**可信**。
2. **不能**将 PR #499 视为「API 已硬化」：四步法③④对**仓库现行行为**为零。
3. 按现稿 v2.7 施工，若不处理 **§7.1 必改**，仍可复现：**stream 半套 artifact（upload 语义）**、**pass 无收口假绿**、**评论板面双源**、**PAT 未配时 lead 仍起跑**。
4. 方案作者主张句本审计**未改**；本文件仅对抗评审。

---

## 9. 与 PR #499 关系

- 本 PR 基于 **#499 同一 head 分支**（或自其开出），**只增** `docs/领班制-API硬化修改方案-对抗审.md`。
- 建议评审顺序：**先 #499 方案 → 再本对抗审 → 修订方案后再 v2.7 施工 PR**。

---

*第二轮对抗审 · Cloud Agent 审计席 · 未触发 team workflow*