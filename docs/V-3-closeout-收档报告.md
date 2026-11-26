# V-3 收档报告：W-17 更正 · W-16 短表 · 死亡账五类 · P-1~P-8 终裁 · S-1 不立项 · live 验收清单

日期：2026-11-26 ｜ 基线：main 06e519a5（PR #840 合并后）｜ 依据：`adversarial/round54-root-cure/` 三份对抗报告（GLM-5.4 方案 → Opus 5.5 终审 → Fable 5.2 复核）收敛裁定

---

## 一、W-17 定性更正（U-6 裁定，留痕件非保险丝）

**最终定性**（Opus 第三节处置全文，Fable 采信）：

> 「离线回收链 3/3 通过；生产首验 4 会话中 2 个调用了 recorder，但逐件落盘服从率 0/4（B/D 均在最后一回合批量落盘）；墙杀场景回收 0/2；且按现行 adopt/门控代码，即使回收 3/3 也不改变 human_stop 与 replan 关闭的结局——**W-17 在现行管线中只能留痕，不能救单**。」

- 处置：保留 W-17 的写盘与读取代码，不回滚；**停止将其表述为「保险丝」**；由 I-6 把它升级为唯一产出通道，由 I-5 补上救单能力。
- 第 54 轮是 W-17 的首次生产运行（PR #785 合并于 2026-11-23T03:29Z，第 53 轮运行树不含该 PR）——「生产首验 0/2、服从率 0/4」即 W-17 的全部生产数据。
- G-2「触发面正样本上线门」批准为制度：任何「让模型调用某工具才生效」的机制，上线前必须有真实会话流中的 tool_call 正样本；离线重放只算回收链测试。V-3 门是 G-2 的第一次执行。

## 二、W-16 证据短表（U-6 裁定：补表后再定是否结项；本 mission 只补表，不动修复面）

W-16 本体（worker 阶段恢复畅通）在 adversarial 目录与仓内 docs 均无独立定义材料（Fable 检索结论）；可证实的间接事实：第 54 轮四单 12 个 worker 全部 success、prep/workers-wall-merge 全部 success、链路首次完整跑到 validator。**按 Opus 裁定「维持现状，不扩不改」，是否结项待大哥读表后定。**

短表（U-6 要求的两条 worker 侧事实 + Fable N-1 正样本）：

| # | 事实 | 数字 | 来源 |
|---|---|---|---|
| 1 | 12/12 worker 会话首次跑 pytest 全部遇到「No module named pytest」，各自多花回合安装（两次 validator 停滞恰好发生在这个多余回合的链条上） | 12/12 | Fable 第四节，U-6 强制入表 |
| 2 | flesch 会话时长 825.0s，占 900s 墙的 91.7% | 825.0s / 91.7% | Fable 第四节，U-6 强制入表 |
| 3 | cssunits 会话 709.8s，其中 490.2s 是非生成型停滞（流 idx 18→19，产出 112 字符；工具结果 0.1s 内已返回） | 490.2s 停滞 | Fable 第四节 + N-1 |
| 4 | 非生成型停滞正样本共 2 个：D-sllist 119.5s / 67 字符、B-cssunits 490.2s / 112 字符；其余 10 个 worker 会话的回合延迟 3.5–9.6s（正常） | 16 会话中 2 个 | Fable N-1 |
| 5 | flesch 最大回合字符量：turn_metrics 口径 40,538 字符 / 505.25s / 80.23 字符每秒（GLM 原报 79,882 系 reasoning 事件成对落盘双计，L-5 口径更正） | 40,538 | Opus F-05 裁定 |
| 6 | 修复面状态：worker 预装依赖已落地（PR-1/U-10：`Install dev dependencies (U-10)` 步在两轮 worker 会话前跑 `pip install -r requirements-dev.txt`，test_revalidate_workflow_contract.py 钉序） | 已修复 | PR #835 |

「12/12 success」不得读成「有余量」：事实 1–3 说明 worker 阶段的余量被缺装回合与请求级停滞吃掉了大头。

## 三、死亡账分账五类（G-1 + Fable 增补；每例按类登记，不再合并统计）

| # | 类别 | 机制 | 主型/例证 | 修法方向 |
|---|---|---|---|---|
| 1 | 单回合推理膨胀 | 一个回合的推理+工具调用跨过整面墙 | worker 主型；54B-flesch（40,538 字符/505.25s 回合） | P-1/P-4（worker 面，另开单） |
| 2 | 协议致延迟落盘 | 验收协议把唯一落盘动作排在全部推理之后；回合原子性+批量读证据使逐件落盘结构上不可能 | validator 主型；54A/C（27 次 tool_call 零 recorder） | I-1/I-6/I-5（本 mission 已落地） |
| 3 | 证据内部不一致诱发反复权衡 | 计数矛盾/冲突边界/上限算术三道决策题拖长推理 | 52B、54 全部 12 包 | I-3/I-4 + 权威计数（已落地） |
| 4 | 超时防线失效 | 应有的超时机制不生效 | 45B（P-8 另案） | 另案 |
| 5 | **请求级停滞**（Fable U-9(3) 增补） | 模型请求路径上 2–8 分钟、与生成量无关的单请求级停滞；非全局停摆 | D-sllist 119.5s、B-cssunits 490.2s；与 54A/C 被杀回合时间重叠 | 网关治理/S-3 观测（仓外成因） |

登记维度（G-3）：每例 validator 预算杀必须记录「结论是否已形成 / recorder 调用数 / 删失尾秒数」。Opus 追加（P-5 行）：分账必须单列 lead/replan 面（L-3：replan 自身也是 480s 会话，52 轮曾死在 lead 面）。

54 轮 A/C 的死亡账登记（本轮重放实证）：
- A：流 62 事件 / 23 tool_call / recorder 0 次 / 删失尾 265.69s（占墙 55.4%）/ 末事件 14:50:06.825Z / 结论已形成（reasoning 可见）
- C：流 21 事件 / 4 tool_call / recorder 0 次 / 删失尾 250.80s（占墙 52.3%）/ 末事件 14:49:11.304Z / 第 3 回合已明写三件全 pass
- 归类：第 2 类为主因（协议致延迟落盘），第 3 类为诱因（12/12 计数不一致），第 5 类为可疑共存因素（cssunits 停滞窗口覆盖 A/C 被杀回合的约九成；F-08 未排除前不作定论）

## 四、P-1～P-8 终裁表（G-4 逐项，U-7 已裁）

| 项 | GLM 处置 | Opus 终裁 | 要点 |
|---|---|---|---|
| P-1 worker 禁脑内验算 | 吸收 | **同意** | 活样本成立；强度更正为 40,538 字符/505.25s（非 79,882）；会话 825.0s 占墙 91.7% 属实。落地另开单 |
| P-2 段级推理措辞 | 吸收但降预期 | **同意** | 四条 validator 流 init 均 `reasoning_effort=none` 仍出 14,867/20,183 字符回合——措辞类约束无运行时效力（已知既有问题，不修） |
| P-3 证据引用优先 | 推翻前提 | **改判：撤回，意图并入 I-3/I-4** | 呈批件 §7.3 已自行修正前提；长回合主因是对账与冲突边界，引用优先无作用 |
| P-4 字符量软预算 40k | 限 worker 面 | **同意** | validator 完成回合最大 15,451/20,631，零命中；worker 面仅 flesch 一例越线，作审计语义保留。落地另开单 |
| P-5 lead 暂不设 | 维持 | **同意＋L-3** | G-1 分账必须单列 lead/replan 面 |
| P-6 墙值维持 | 维持到 S-1 后重定 | **同意维持；重定条件改为「S-1 立项时」** | `budget_resolve.py:73` 硬断言 480，改值须同步断言与 lint；本 mission 预算冻结 diff 0 字节 |
| P-7 turn_metrics 收档 | 吸收，--job-log 必配 | **同意＋L-5 口径** | 复跑 A 265.69s / C 250.80s，与墙账一致；禁止手工对 reasoning 事件求和 |
| P-8 45B 超时失效 | 维持另案 | **同意** | 与本轮无关 |

## 五、S-1 不立项声明＋触发条件（U-5 已裁）

**S-1（拆会话/每件一个 180s 独立会话+机器简表）：不立项。**

不立项理由（Opus 2.2 四接缝，Fable 复核后仍成立的）：
1. **跨件冲突丢失**（Fable 修正后的真接缝）：12 包的 status.json 无结构化冲突字段、handoff 小节标题写法多样，机器简表抽不出可靠的冲突声明段——fail-open 方向风险；
2. **扇入合并**：三会话并行需要新扇入 job 与部分采认语义（正是 human_stop 要防的灰区）；
3. ~~合并 pytest 归因~~（Fable 反驳成立：unattributed_failure 完全由机器计算，单件会话无需给出，不构成阻碍）；
3'. **并发放大**（Fable：证据两头都有但更硬的反对成立）：墙越短对请求级停滞越脆弱——490.2s 型停滞必杀 180s 墙，119.5s 型吃掉三分之二墙；F-08 未分清前上 S-1，可能把死法从「长推理」换成「停滞杀」。

**触发条件**（按 Fable U-5 修正版写明，区别于 Opus 原文）：

> 立即层（I-5/I-6）与 S-2 落地后，**连续 2 轮 live（8 单）中「首次验收会话被杀 ≥2」或「出现任一双杀」**，先按 N-1 方法对被杀回合分型；**属于长推理型才启动 S-1 立项**，属于停滞型走网关/重试治理，不走 S-1。

（Opus 原条件「墙杀 ≥1 且重验后仍失败」要求双杀，而 I-5 上线后双杀概率 ~4%，8 单大概率观察不到——条件会被 I-5 自己掩盖，故改为看首次被杀率＋分型。）

触发前的必报数据链：每轮收档的「首次被杀数」自动接入本条件（见第七节 live 清单）。

## 六、V-3 上线门状态（指针）

V-3 门本轮未过：`custom:DeepSeek-V4.1-Flash-Go`（CI live 同通道模型）上游 403「Model access is disabled」，A 包会话未启动即终止，C 包未执行。**禁止上线新 prompt 至 live**；修复与重跑路径见 `docs/V-3-gate-上线门报告.md`。前置三件（PR1-8/PR1-10/PR2-6）已合入（PR #840），门可随时重跑。

**当日复探（收尾轮，2026-11-26）**：上游 403 未解除（对照 glm-5.3-flash 200）；真 CI 通道（droid-test.lumivane.dpdns.org）鉴权走 GitHub secret `GO_GITHUB_RUN_TOKEN`，worker 侧无从旁路证实。重跑就绪件复核完毕：prompt 渲染件与 main 单源模板逐字节一致、判定脚本口径在位——通道恢复后 ~15 分钟内可重跑。复核同步确认：333 passed 2 skipped＋五 lint 绿＋预算冻结 0 字节，收档数据全部继续有效。

## 七、给大哥的 live 验收清单（U-9 最终口径；V-3 过门后、发单时按此收档）

**总判定**：连续 2 轮（8 单）live 全绿才算治好；「过了几单」不作为治好依据。V-3 门永久保留为发版前置。

验收门（硬指标）：
1. **因验收会话被杀而死的单数 = 0（含重验后）**（V-7 修正版验收门）
2. draft_timeout 形态下 revalidate 自动触发且至多 1 次；重验通过走正常采认、重验再失败才 human_stop（V-5，墙账 replan_gate + job 图核对）
3. 被墙杀会话的 verdict-partial.json analyzed_count ≥ reasoning 中已形成结论件数（V-1）
4. 证据包内计数差异 = 0（check-summary.json 权威计数生效）（V-4）

必报指标（每轮收档固定输出，不设门槛但必须报数）：
5. 首次验收会话被杀数（接 S-1 触发条件：连续 2 轮 ≥2 或双杀即评估分型）
6. 重验触发数 / 重验成功数
7. 逐件落盘服从率（recorder 调用与证据读取交替出现的会话占比）
8. recorder 首调用率；被杀会话的 recorder 调用数
9. 删失尾秒数（turn_metrics --job-log 必配；L-5：禁手工对 reasoning 事件求和）
10. 停滞回合清单：延迟 ≥60s 且产出 <500 字符的完成回合，validator 流与 worker 流都算
11. 包内计数不一致数

观测项（不作验收门）：
12. V-6 关键词计数（`12 tool`/`tool call`/`call budget` 与「Hmm＋计数词」共现）——措辞类指标易被绕过，降为观测。

发单前置检查（大哥操作）：
- V-3 门已过（A/C 各 ≥1 次 recorder tool_call，流文件路径入档）
- CI 四个 BYOM 步的模型通道恢复可用（本轮 403 阻塞已解除）
- 第 54 轮四单工单（#812/#813/#814/#815）处置完毕，不与本轮混算

## 八、验证记录（VAL-CROSS 三条，2026-11-26 实测）

| 断言 | 命令/方法 | 结果 |
|---|---|---|
| VAL-CROSS-001 | `git diff 7698e54 -- scripts/team/budget_resolve.py scripts/team/foreman_run_lib.py` 字节数；team.yml timeout 行 old-vs-new 集合差 | **0 字节**；移除集合为空（仅新增 2×15/2×2/2×3 分钟步级超时于新 revalidate/extract/verdict 步） |
| VAL-CROSS-002 | `pytest tests/ -q` + 五个 lint 脚本 | **333 passed, 2 skipped**（基线零回归）；五 lint 全绿；无绕过 sha 校验或机器闸的新路径（PR #840 只加 pin 与打印） |
| VAL-CROSS-003 | 真 wrapper 端到端重放（run_adopt_step → compute_replan_gate → compute_validate_conclusion，GNU timeout 120s，真实 r54A/C 包） | **不复现**：首次超时（无产物）→ human_stop=False + should_revalidate=True；torn draft + sealed full partial → 采认 ok（A: overall=pass salvage_assembled=True pytest_exit=0；C: overall=fail failed=[issn] human_stop=False）；重验后再超时（marker 已盖章）→ human_stop=True（唯一合法 fail-closed 分支）；should_replan 路由：首超时→False，C 型采认失败→True（进二轮），重验成功 FAIL→True |

重放工件目录：`/tmp/v3-cross003/`（含 out-*.txt 三个 --github-output 与两份墙账快照）。

## 九、本轮产物清单

- PR #840（mergeCommit 06e519a5）：V-3 前置三件（渲染位点统一 / revalidate sha 门逐位点 pin / prompt `--final`+`--conflict` 说明 / 双连字符 bullet 修正）；新增 `tests/test_v3_prework_pins.py` 15 测试
- `docs/V-3-gate-上线门报告.md`：门未过定性 + 通道阻塞证据 + 重跑就绪件
- 本文档：收档四件 + live 验收清单
- mission handoff：EndFeatureRun 回填（含 V-3 阻塞上报）
