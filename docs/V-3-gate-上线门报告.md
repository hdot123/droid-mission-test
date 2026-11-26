# V-3 上线门报告（round54-root-cure M2 硬门）

日期：2026-11-26 ｜ 断言：VAL-V3-001 ｜ 判定：**门未过（通道级阻塞）——禁止上线新 prompt，等通道恢复后重跑**

## 复探记录（2026-11-26 当日第二次实测，任务收尾轮）

- 通道复探（node-01 网关，与首探同法）：`deepseek-v4.1-flash` 仍 **403**「Model access is disabled. Change model access at https://opencode.ai/console/wrk_01M2TDZV72YSY2CP6M55418B5Y/controls.」；对照 `glm-5.3-flash` 仍 200——阻塞未解除。
- 真 CI 通道探测（`https://droid-test.lumivane.dpdns.org`，team.yml 四个 BYOM 步的 baseUrl）：1Password 在册的 lumivane CF 网关调用凭证在该 host 的 chat 端点返回 401（该网关鉴权走 GitHub secret `GO_GITHUB_RUN_TOKEN`，非 1Password 在册凭证）；裸 urllib 被边缘 CF 以 error 1010 拦（客户端指纹）。CI 通道侧无法从 worker 侧证实/证伪 deepseek 状态，但上游（opencode console）403 已经独立证实模型本身访问被禁。
- 重跑就绪件复核：`/tmp/v3-gate/{a,c}/validator-prompt.txt` 与当前 main 单源模板渲染**逐字节一致**（A 5,423 B / C 5,417 B，含 `--final`/`--conflict` 说明、无双连字符 bullet）——通道恢复即可按原命令形态重跑，无需重造。
- 代码面复核（同日）：全量 pytest **333 passed 2 skipped**、五 lint 全绿、预算冻结 diff 0 字节——门未过与代码面无关，维持「禁止上线新 prompt」。

## 门定义（validation-contract.md VAL-V3-001）

用 54 轮 A/C 证据包（`/tmp/r54-audit/{a,c}/evidence/`）各跑一次真实 droid 会话（与 CI live 同通道、新 prompt），流事件级解析必须各出现 ≥1 次 `salvage_verdict` tool_call。任一流零调用 → 门未过。

## 执行记录

| 项 | A 包 | C 包 |
|---|---|---|
| 证据包 | `/tmp/r54-audit/a/evidence/`（issue 812, run 45195635939, manifest sha eb7da7af…） | `/tmp/r54-audit/c/evidence/`（issue 814, run 45195771256） |
| judgeable | damm, easterorthodox, graph | ellipse, issn, pluralize |
| prompt | `build_validator_prompt(judgeable, round_num=1)` 渲染，5,423 B，含 `--final`/`--conflict` 说明、无 `- - plan.json` 双连字符（PR #840 后） | 同源渲染，5,417 B |
| 会话命令 | `timeout --signal=TERM --kill-after=30s 600s droid exec --auto high -m custom:DeepSeek-V4.1-Flash-Go --output-format stream-json "<prompt>"` | 同 |
| 工作目录 | `/tmp/v3-gate/a` | `/tmp/v3-gate/c` |
| 结果 | **EXIT=1，流 10,073 B，零 tool_call**：init 事件后收到 `403 Model access is disabled`（agent_loop error ×2），会话未启动即终止 | 未执行（通道阻塞） |

## 阻塞根因（通道级，非 prompt 级）

模型 `custom:DeepSeek-V4.1-Flash-Go`（CI live 会话的 BYOM 模型 id，`dynamic/droid-review` @ `https://droid-test.lumivane.dpdns.org`）**上游访问被禁**。逐模型探测（2026-11-26，node-01 网关同款模型/密钥形态直连探测）：

| 模型 | HTTP | 判定 |
|---|---|---|
| deepseek-v4.1-flash | **403** permission_error「Model access is disabled. Change model access at https://opencode.ai/console/wrk_01M2TDZV72YSY2CP6M55418B5Y/controls.」 | 不可用 |
| glm-5.3-flash | 200 | 可用 |
| kimi-k2.7-code | 200 | 可用 |
| mimo-v2.6-flash | 200 | 可用 |
| glm-5.3 / glm-5.4 / deepseek-v4-flash-vision-exp / muse-spark / space-bunny / longcat | 400 | 不可用（网关侧 400） |

影响面不止 V-3 门：CI live 的四个验收会话（validate/validate2/revalidate/revalidate2 全部 BYOM 步）用的都是同一个模型 id——通道不恢复，下一轮 live 四单也会全部 403。

## 为什么判「门未过」而不是「换模型跑过门」

G-2 制度（W-17 教训的制度化）要求上线门验证的是「生产通道上模型对新 prompt 的触发面」。换任何一个可用模型跑出来的正样本，都不是 CI live 会要跑的那个通道的证据。environment.md 也明确预注：「如 V-3 会话被拒，报告 orchestrator，勿自行换模型」。故按规则如实判失败并上报。

## 已就绪、等通道恢复即可重跑的部分（约 15 分钟内可完成）

1. 每会话 droid settings（模型 id 与 CI 逐字一致）：`/tmp/v3-gate/{a,c}/settings.json`
2. 新 prompt 渲染件（PR #840 后的单源模板）：`/tmp/v3-gate/{a,c}/validator-prompt.txt`
3. 判定脚本口径：`type=="tool_call"` 事件、`toolName`/参数含 `salvage_verdict` 即计一次；A/C 各 ≥1 过门（与 CI 判定器同口径，见 AGENTS.md「V-3 门判定」）
4. 修复选项（需人工在网关/console 侧操作，本 worker 无权限）：
   - 恢复 `deepseek-v4.1-flash` 的模型访问（403 信息指向 console 控制页）；或
   - CI 四个 BYOM 步换用任一 200 模型（需大哥明示换型，不属于 worker 越权范围）。

## 附：本 feature 已完成且不受阻塞的其余项

- V-3 前置三件已合入（PR #840，mergeCommit 06e519a5）：渲染位点统一、revalidate sha 门钉住、prompt 增补 `--final`/`--conflict` 说明。
- VAL-CROSS-001/002/003 已验：预算冻结 diff 0 字节、333 passed 2 skipped + 五 lint 绿、A/C 型死法端到端重放不复现（`docs/V-3-closeout-收档报告.md`）。
