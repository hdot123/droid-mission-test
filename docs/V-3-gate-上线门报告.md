# V-3 上线门报告（round54-root-cure M2 硬门）

日期：2026-11-26 ｜ 断言：VAL-V3-001 ｜ 判定：**门已过（2026-11-26 重跑轮）——新 prompt 具备上线资格，live 发单前置检查见收档报告第七节**

## 重跑结果（2026-11-26 第三次实测，通道裁决后）

**通道裁决**（大哥 2026-11-26，已落 mission environment.md）：上游是路由模式，请求返回 200 的模型即视为可用通道——`deepseek-v4.1-flash` 403 不构成阻塞，V-3 门换用实测 200 的 `glm-5.3-flash` 重跑（该模型在首探与复探两轮都作为对照的 200 正样本）。真 CI host（droid-test.lumivane.dpdns.org）鉴权走 GitHub secret，worker 侧不可旁路，按裁决不再尝试。

| 项 | A 包 | C 包 |
|---|---|---|
| 证据包 | `/tmp/r54-audit/a/evidence/`（issue 812, run 45195635939, manifest sha eb7da7af…） | `/tmp/r54-audit/c/evidence/`（issue 814, run 45195771256, sha 5fcbcf1a…） |
| judgeable | damm, easterorthodox, graph | ellipse, issn, pluralize |
| prompt | `build_validator_prompt(judgeable, round_num=1)` 现渲染，5,423 B，与上轮就绪件逐字节一致（含 `--final`/`--conflict` 说明、无双连字符 bullet） | 同源渲染，5,417 B，逐字节一致 |
| 会话命令 | `timeout --signal=TERM --kill-after=30s 480s droid exec --settings <session> --auto high -m custom:DeepSeek-V4.1-Flash-Go --output-format stream-json "<prompt>"`（settings 内 CI 同款模型 id → glm-5.3-flash） | 同 |
| 工作目录 | `/tmp/v3-gate/a/work`（=证据包内容＋judgeable/blocked＋PYTHONPATH 含 scripts/team，`python3 -m salvage_verdict` 真可执行） | `/tmp/v3-gate/c/work` |
| 退出码 | 0（正常完成，无墙杀） | 0 |
| **recorder 调用数** | **4**（damm→pass、easterorthodox→pass、graph→pass、graph→pass＋--final 收口） | **3**（ellipse→pass、issn→pass、pluralize→pass＋--final 收口） |
| 落盘产物 | verdict-partial.json（final=true，3/3）、verdict-droid.json、verdict-droid.md | 同左（3/3） |
| 采认链 | 真 wrapper 三步（run_adopt_step → compute_replan_gate → compute_validate_conclusion）：**overall=pass、validate_job_conclusion=success、should_replan=False、should_revalidate=False** | 同左 |
| 会话指标 | turn_metrics：13 回合 / 首响 10.74s / 最大回合延迟 25.16s / 总 30,655 字符，无停滞回合、无删失尾 | 13 回合 / 首响 11.92s / 最大延迟 21.54s / 27,446 字符，无停滞回合 |

判定口径（AGENTS.md「V-3 门判定」）：`type=="tool_call"` 事件且 Execute command 实际调用 `python3 -m salvage_verdict`（计 4/3 次；写报告 MD 的 Create 调用内容里提到 recorder 字样不计）。A/C 各 ≥1 → **过门**。

证据（PR-able，已入仓）：`docs/evidence/v3-gate-rerun/{a,c}/`——pruned 流（去 reasoning 双计事件，保留 tool_call/tool_result/message/system/completion）、verdict-partial.json、verdict-droid.json、session-meta.json（manifest sha/退出码/模型映射）、墙账 foreman-run.json、采认链 verdict.json 与 --github-output。

执行中的两次环境修正（不涉及判定口径）：
1. 裸 `droid exec` 不带 `--settings` 时硬编码模型 id 报 Invalid model——按上轮 kit 结论加 `--settings`（会话级单模型映射，CI id 逐字保留）。
2. 首轮 adopt 链重放误判 `droid_step_failed`，根因是我自搭的 `blocked.json` 用了 list 而 adopt 按 CI 形状读 dict（`{pid: missing[]}`）——修正 fixture 后全链通过；pipeline 代码无改。

## 首跑记录（2026-11-26，通道阻塞期，留档）

| 项 | A 包 | C 包 |
|---|---|---|
| 结果 | EXIT=1，流 10,073 B，零 tool_call：init 事件后收到 `403 Model access is disabled`（agent_loop error ×2），会话未启动即终止 | 未执行（通道阻塞） |

阻塞根因（已按裁决解除）：CI live 同通道模型 `custom:DeepSeek-V4.1-Flash-Go` 上游访问被禁（403，opencode console 控制页）。逐模型探测（node-01 网关）：deepseek-v4.1-flash=403；glm-5.3-flash / kimi-k2.7-code / mimo-v2.6-flash=200；其余变体=400。当时按旧口径判「门未过、禁止上线」；大哥随后裁决 200 模型即有效通道，本报告重跑部分即为执行结果。

## 上线资格结论

- 新 prompt（PR #840 后单源模板）在真实 droid 会话、真 CI 模型 id（会话级映射到裁决批准的 200 模型）下：**逐件落盘纪律被服从**（每件一读一记，末件 --final 收口），recorder 首调用率 2/2 会话，采认链全绿。
- 前置三件已合入（PR #840，mergeCommit 06e519a5）：渲染位点统一、revalidate sha 门钉住、prompt 增补 `--final`/`--conflict` 说明。
- VAL-CROSS-001/002/003 此前已验（预算冻结 diff 0 字节、333 passed 2 skipped + 五 lint 绿、A/C 型死法端到端重放不复现，见 `docs/V-3-closeout-收档报告.md` 第八节）；本轮重跑后代码面复核继续全绿（见同报告第六节更新）。
- live 发单前置（大哥操作）：第 54 轮四单（#812/#813/#814/#815）处置完毕后按收档报告第七节清单发单收档。
