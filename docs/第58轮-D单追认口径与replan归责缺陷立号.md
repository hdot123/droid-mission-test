# 第 58 轮 D 单追认口径 + replan 归责缺陷立号（待裁第 14 项裁定留痕）

本件留痕「待裁第 14 项」的两件裁定记录：D 单按「落盘失败型·关单＋已验收」追认，以及 replan 归责错位缺陷立号并由本 mission 根治其 repo 侧机制。证据语料：`adversarial/round58-d-verify/`（本地落盘，run 45812793849 CI 工件）；仓内 verbatim 夹具 `tests/fixtures/worker-r58d/`。

## 一、D 单追认：落盘失败型·关单＋已验收

**口径原文（issue #929 关单评注，第 398 行段）：**

> 第 58 轮关单（交付层验收通过、run 层死亡入账，两层并记）：主 run 45812793849 终局 Failure。过程全程披露：第一轮 hslconv 工人会话被 900s 会话墙杀死于最后 checks 步（两回合单回合推理膨胀 203s＋376s，死于会话墙而非实现——实现完整、checks 全绿、384 passed），handoff/status 未及落盘、证据包缺件，verdict1 判 fail；replan 触发后第二轮只重跑 hslconv 全绿（391 passed, 2 skipped），validator 二轮 pass、assemble 成功、候选 PR #949 开出（按活验口径不合并）。交付层终局机器判定全过（verdict2 pass、validation overall=pass），板面已由流水线写为已验收，故本单关单＋已验收，不改标失败；run 层 Failure 后果入账：整单死亡 +1（死亡账整单 46/93）、持续进化计数按规则清零。……

**追认口径分解（本登记的裁定留痕）：**

1. **死因定性：落盘失败型，非实现失败。** 工人会话死于 900s 进程墙（exit 124、末事件被中断的 tool_error、13 次工具调用零次以两件证据文件为目标），而工序产出的机器验证（prep 合并后重跑 checks 全绿，卡片 21 passed / 合并态 384 passed）早已成立且独立于会话死活。失败形态是「证据文件产出责任绑在被杀会话上」，不是工作质量。
2. **两层并记：** 交付层验收通过（二轮全绿、verdict2 pass、板面已写已验收）与 run 层死亡入账（终局 Failure、整单死亡 +1、进化计数清零）同时成立，互不覆盖。
3. **处置：关单＋已验收，不改标失败。** 追认依据是交付层终局机器判定全过，且死亡后果已在 run 层单独入账——不因 run 层 Failure 回改交付层板面。
4. **台账侧执行：** 关单评注与板面翻板由大哥在台账侧执行收档（工单写操作不在本 mission 边界内，issue #929 全程只读）。
5. **结构根治：** 本型死亡的后果链由本 mission 三层根治（补卷器/死亡上墙/归责根治）。verifier 步 `if: always()` 守卫与补卷闸的连锁交互（scrutiny round-1 BLK-1/2）已按「marker 按内容判定红、取消路径排除」修复并钉死（`tests/test_verify_prep_salvage_chain.py` / `tests/test_verify_marker_interaction.py`），后续同类死法在结构上不再产生「已全绿工作作废＋二轮重做」。

（时间线注记：上节第 5 条与下节「修复面」表为**裁定后的修复完成态**；缺陷立号在引用口径写成时（第 58 轮关单评注原文尾句）为「立号待裁」，其裁定落在本件第二节。）

## 二、replan 归责缺陷立号

**缺陷事实（run 层证据）：** 一轮 validator 判 blocked 后，replan 输入面只有 plan/verdict/manifest/packs/pytest-output，无 exit code、无 timeout 信号、无 worker-delta——死亡事实对 replan 决策面不可见。机制根源是 validate 合并步的硬编码归责预设「缺件归该工序补齐」对一切缺件形态输出工人归责措辞，于是 retry_note 把墙杀死工序归责为工人服从性问题（"the fault is yours for not writing the two evidence files"），与「会话被机器墙杀死于落盘之前、产出经机器复验全绿」的事实不符。二轮整会话从头重做已全绿的活。

**裁判更正：** 该归责错位已在裁判报告中更正（round58-referee.md，仓外本地正本之一，未入仓/未入 issue/PR——留痕缺口见「Known Pre-Existing Issues」注记），缺陷立号待裁。

**裁定：缺陷成立，立号，repo 侧机制由本 mission 根治。** 修复面（全部机器判定，零模型参与）：

| 修复件 | 位置 | 行为 |
|---|---|---|
| worker-delta 结构化结局 | team.yml delta 记录步 + `scripts/team/write_worker_delta.py` + `scripts/team/merge_worker_deltas.py` | session_outcome（ok/wall_killed/job_wall_cancelled）/ droid_exit_code / stream_tail_marker 三字段确定性分类上墙 |
| 归责模板分支化 | `scripts/team/attribution_reason.py`（validate/revalidate/validate2/revalidate2 四合并步调用） | 死因在场（wall_killed）→ 中性归因措辞（含死因事实，不含「缺件归该工序补齐」）；死因不在场 → 维持现行措辞逐字节不变（fail-closed） |
| replan 输入面死因注入 | team.yml replan 步 heredoc 输入段 | worker-delta 结局事实进 "In front of you" 输入面板；wall_killed 时面板附中性归因指令，redispatch/revise 判定权仍在领班 |

验收：`tests/test_replan_death_context_attribution.py`（VAL-M1-004/005，含 CI 保真 clean-subprocess 回放）+ 端到端 `tests/test_r58d_e2e_replay.py`（VAL-CROSS-001/002：死链中性化 vs 对照链现行措辞）。

## 三、待裁第 14 项状态

- D 单追认（落盘失败型·关单＋已验收）：**已裁定，本件留痕**；台账侧收档评注由大哥执行。
- replan 归责缺陷：**已立号并根治**（repo 侧机制全落地、全套件/lint 门全绿）；round58-referee.md 正本仍在仓外，追认引用以本件与 issue #929 关单评注为准。
