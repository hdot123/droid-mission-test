# 逐席位失败规范（failure-specs 底稿）

> 底稿（mission F4/failure-specs 产出；主设计稿 §5 失败规范章素材）。本件给 7 席位各一份失败规范（照引擎点位普查表五字段形制：怎么死／死了谁知道／谁处置／机器判据／缺口），并完成两项并入：**已批根治 1+2+4 并入失败规范格**（不再单独立项）、**第 3 层回合熔断按上游登记口径显式标注不可施工面**。每墙每门必死样本设计与执法延迟实测口径见姊妹底稿 `acceptance-line-map.md`（主设计稿 §6 验收线章素材），本件不重复定义桩形态。
>
> **真源声明**：引擎失败规范形制以 `docs/wall-v3/form-basis.md` 要点 10（原物锚：引擎仓 `docs/guides/exception-point-inventory.md:23`/`:27`/`:94`）为准；测试仓现状行号以 `docs/wall-v3/as-is-capability-inventory.md`（锚件 2）为准。席位授权面以 `docs/wall-v3/seat-gates.md`（F2 底稿）为准——每席失败规范的处置手段引用该席门清单的门（§0 口径 4）；交接物/证据执法面以 `docs/wall-v3/handoff-schemas.md` 为准。本件全部 file:line 锚经实读核实（2026-11-27 快照，测试仓 R58-D 收尾态基线 564ce30）。
>
> **三态纪律**（照引擎普查表口径）：每席处置现状定级只能取 **有**（机器判据＋执法通道都在树）/ **部分**（判据在树、执法通道缺角）/ **无**（判据与通道都缺）；目标态设计不得把「无」写成「有」。结构盲区显式列出（§8）。
>
> **版本口径**：本件属设计稿 v3.0 体系，作废 v2.7~v2.10 账面墙口径。

---

## §0 形制与口径（读本件前必读）

**0.1 五字段形制**（照抄引擎点位普查表，form-basis 要点 10）：每席失败规范一张表，字段固定——**怎么死**（触发面与死法形态）／**死了谁知道**（死亡信号到达面）／**谁处置**（处置主体与动作链）／**机器判据**（判定死亡与触发处置的机器可执行判据）／**缺口**（现状定级＋v3.0 收口）。判据不写散文：凡机器判据必给可执行判定式（读哪个字段、比较什么、红了退出码几）。

**0.2 「机器判据」的构造纪律**：判据只允许引用三类载体——①墙上机器记录（`worker-delta` 三字段 / 墙切片 / 墙补丁）；②机器守卫退出态（caps-gate/F-1/budgets lint 的三态退出码 0/1/2，对位引擎判词纪律 form-basis 要点 4）；③会话流机器事件（stream tail marker）。**会话自述（prompt/narrative/handoff.md 自由文本）不进任何判据**（handoff-schemas §1 原则 4：自由文本不承载判定）。无机器载体可引的死法，其判据只能写「缺席即事件」（§0.5）或登记进结构盲区（§8），不得虚设判据。

**0.3 并入口径——根治 1+2+4 并入本格**（来源：`docs/R58D-收尾决策留痕-NC6与遗留决策点.md` §一批准范围行 :3/:5；`docs/回合熔断上游特性需求登记-droidCLI.md` 结论行 :17）：

| 根治层 | 现状载体锚 | 并入落位 |
|---|---|---|
| 第 1 层（M2）补卷守卫/补卷器 | `scripts/team/worker_salvage.py:13`（守卫四条件 docstring，机器判定 fail-closed）、接线 `team.yml:1223-1226` | 并入 **worker 席**失败规范「谁处置」（补卷器=死因 B 类的机器处置）与 **recorder 席**（机器兜底=写板缺席的处置）；守卫四条件原文登记于 §1.4 |
| 第 2 层（M3）模板单源＋守卫 | `scripts/team/worker_prompt_template.py:13`（增量落盘引导，P-2 口径预期封顶） | 并入 **worker 席**缺口列与 **recorder 席**（prompt 单源=措辞面，无运行时效力，防「措辞」冒充「执法」的口径由本件统一登记） |
| 第 4 层（M1）死亡上墙＋归责根治 | `team.yml:836`（write_worker_delta 上墙）、`team.yml:885`（merge_worker_deltas）、`schemas/foreman-run.v1.schema.json:146-157`（by-pid 三映射）、`scripts/team/attribution_reason.py:26/:65/:75`（归责分支化） | 并入 **worker 席**「死了谁知道」与 **replan 席**「机器判据」（死因注入面枚举化，四问题①收口，handoff-schemas §9） |

并入口径随附规格明文：**补卷覆盖面 ≠ 中性归因覆盖面**（`scripts/team/worker_salvage.py` docstring；守卫经「非零 droid_exit_code」子句接纳 exit-1 自崩族，归责只按 wall_killed 分支）——凡引用根治 1+2+4 之处不得假设「补了卷 ⟹ 归因已中性化」。

**0.4 第 3 层（回合熔断）不可施工面——上游登记口径显式标注**（`docs/回合熔断上游特性需求登记-droidCLI.md` :11-:17 裁定理由三条、:19-:24 立项前置三能力）：

> **不可施工裁定（大哥已裁，登记于上游需求件）**：回合级熔断（per-turn circuit breaker）不在本仓施工。理由逐条：① droid CLI 无回合预算接口——回合是 agent-loop 内部概念，外层进程控制粒度止步于进程（`回合熔断上游特性需求登记-droidCLI.md:13`）；② 外层早杀对工件保护更差——把 900s 调小只会更早杀死会话、砍断更多落盘机会，比现状更差（`:14`）；③ 无续作能力——exec 一次性会话，被杀即终，无 resume 接口（`:15`）。
>
> **对失败规范的约束**：worker/validator/replan/lead 四席死法表中凡触及「单回合推理膨胀」类死法（死亡账第 1 类，V-3 收档报告 §三 :34 起），其处置列**不得设计回合级熔断**——v3.0 体外执法的粒度上限是「会话级进程组终止＋落盘产物机器回收」，第 3 层待上游提供回合预算/安全收束/续作三能力（登记件 :19-:24 表）后再立项。设计稿任何章节出现「回合熔断/回合预算」字样必须带本段口径引用，防止后续施工把上游特性需求误当仓内可施工面。

**0.5 缺席即事件口径**（硬规则⑥，判据形态由本件统一定义、逐席引用）：**某席位的必交件/必落字段/约定首步在判定窗口内未出现，即视为一次事件**（not "nothing happened"）。机器判据形态统一为：`观察点在窗口截止时点读取授权计数器/落点存在性，计数=0 或落点缺席 → 产生告警事件（墙记缺席面＋硬评论）`。窗口与观察点由承载席门清单 `budgets`/`probes` 键定义（seat-gates §2）；缺席告警的执法延迟口径随 acceptance-line-map §3（缺席类事件无超时点到真死的时间差，其延迟口径=告警事件产出时延，同口径采样取上界）。缺席即事件的逐席判据落位：recorder 席（§7）、worker 席（§1 判据 5）、verdict 面（§3 判据 3）。

---

## §1 工人席（worker；镜像 worker2 `team.yml:2697`）

门清单：seat-gates §2.2。预算锚：账面 `scripts/team/foreman_run_lib.py:53-54`（900，不接线）；裸跑硬编码 `team.yml:599`（worker2 同款 `:2784`）。

| 字段 | 内容 |
|---|---|
| **怎么死** | 三类死法：**A. 墙杀**——GNU timeout 900s 外墙 TERM→KILL（`:599`；exit 124= TERM 杀、137=SIGKILL 杀，机器杀印）；45B 实证过「超时不执法」形态：孤儿子进程持管道使 step 活到 25m job 墙（名义 900s 实测墙钟 1800s，锚件 2 §10-②）。**B. 落盘未遂**——会话死（墙杀或自崩）于写 evidence 件之前，已全绿工作因缺件面临作废（58-D 主型：`docs/第58轮-死亡账分型登记-58D归第1类.md:21-22`——hslconv 死于 900s 墙前未写 evidence 件，两个膨胀回合占会话 64.41%）。**C. 自崩**——droid 非零退出（exit 1 族）无 completion 事件（`scripts/team/write_worker_delta.py:42` SELF_EXIT_CODES=(0,1) 的排除面）。 |
| **死了谁知道** | 全部死法都有机器信号面：`worker-delta.json` 三字段（session_outcome / droid_exit_code / stream_tail_marker，分类器 `scripts/team/write_worker_delta.py:45` classify_session_outcome，exit 124/137→wall_killed、interrupt 尾标→wall_killed、cancelled job→job_wall_cancelled、其余非零→按族分类）→ `team.yml:836` 上墙 → `team.yml:885` merge_worker_deltas 并集 → 墙 workers 切片三映射（`schemas/foreman-run.v1.schema.json:146-157`）。**矩阵面**：每 pid 一条，缺 delta=缺席事件（prep 门走既有缺件路径，seat-gates §2.3 events_consumed）。 |
| **谁处置** | **A 类**（墙杀）：链不断——workers-wall-merge `always()` 接纳 cancelled（lint_workflow_wall_exits 执法面，锚件 2 §12）；死因随墙流 prep/replan；重做面归 replan（plan-v2）。**B 类**（落盘未遂）：**根治第 1 层处置**——prep 补卷器机器补写缺失 evidence 件并标 salvaged_from_machine（`team.yml:1223-1226` 接线）；守卫四条件不满足=不补卷、pack 维持缺件（见判据）。**C 类**（自崩）：不补卷归责分支（补卷覆盖面≠归因覆盖面，§0.3）——死因进 delta，归责措辞由 `scripts/team/attribution_reason.py:75` neutral_attribution 分支渲染。 |
| **机器判据** | ①墙杀判定：`droid_exit_code ∈ {124, 137}` 或 stream 尾=interrupt marker（`write_worker_delta.py:63-75` 分支）→ `session_outcome=wall_killed`。②自崩判定：`droid_exit_code ∉ {0,1,124,137} 且 >0 且 stream 无 completion 事件`（`write_worker_delta.py:79-86`）。③补卷守卫**四条件 ALL-of**（`scripts/team/worker_salvage.py:13` docstring 机器判定 fail-closed）：merged true ＋ F-1 clean ＋ prep 复跑 checks 全绿且 checks-failed.marker **按内容判红** ＋ 会话异常终止（wall_killed／非零 droid 退出码／真 stream_tail_marker 任一）。④取消链保护：job cancelled 时 verify marker 不翻转 result（BLK-2，`write_worker_delta.py` docstring :16-19）。⑤**缺席即事件**：窗口（budgets.droid_wall_sec）截止时 delta 缺席 → prep 门按缺件路径＋缺席告警（§0.5 判据形态）。 |
| **缺口** | 现状定级：**部分**——判据①②③④已在树（根治 1+2+4 交付），但执法通道缺角：工人会话**裸跑**（`:599`/`:2784`，budgets lint 豁免分支 `scripts/team/lint_workflow_budgets.py:43-51`）→ 900s 执法与会话同体（超时不执法的 A 类变体无体外执法）；verify 步 subprocess 无超时（锚件 2 §2）。**v3.0 收口**（承接 seat-gates §4）：工人席收进包装器（预算从门清单读、哨兵→SIGTERM 组→宽限→SIGKILL 组体外执法、豁免分支废止）——对应必死样本 SL-3 恒挂桩（acceptance-line-map §2.2）。第 3 层回合熔断**不可施工**（§0.4 口径引用），第 1 类死法的 v3.0 处置上限=会话级体外终止＋补卷回收。 |

---

## §2 领班席（lead）

门清单：seat-gates §2.1。预算锚：`scripts/team/foreman_run_lib.py:37-40`（600）；包装接线 `team.yml:202-204`。

| 字段 | 内容 |
|---|---|
| **怎么死** | 四类：**A. 墙杀**——包装器墙 600s（`foreman_run_lib.py:38` droid_wall_sec=600）杀会话，计划分段卡残缺。**B. 计划残缺**——会话活但产出分段卡不足/stitch 失败，`team-plan.json` 不成立，派单无卡。**C. 越权写**——会话写 team/lead-plan-segments/ 外文件（现状无机器守卫仅 prompt 纪律，锚件 2 §1）。**D. 门未过**——env-check 门 `foreman_ok=='true'` 不放行或 dup 判重。 |
| **死了谁知道** | A 类：包装器墙 patch（budgets.session_outcome，FOREMAN_RUN_PATCH=1 面，`team.yml:202`）→ 墙 budgets 切片（`schemas/foreman-run.v1.schema.json:59` 起 budget_slice 面）＋workflow job result（wall_exits lint 强制每链席 always() 记墙退出）。B 类：stitch 步退出码＋计划 artifact 上传缺席（`team.yml:439-443` plan upload 面）→ assemble always() 仍收口。C 类：现状**无信号面**（无守卫）——v3.0 由 caps-gate `out-of-scope-write` 判词供信号。D 类：gate 输出面＋墙 env 切片。 |
| **谁处置** | A/B 类：workflow 链失败传播（wall-exits 语义：lead 红→下游按 needs 门静默不启）＋assemble fail-closed 收口报终态（`team.yml:4420` pick_verdict_from_wall 权威 pick）＋人工点名重跑（issue 评论触发面）。C 类：v3.0 处置=caps-gate 红进 CI（恒跑接线锁，seat-gates §1.4）＋工作区写目标收窄（默认删多出的门，seat-gates §3.4 表 1/3）。D 类：env-check 体检评论（hard-required 面）→人工处置入口。 |
| **机器判据** | ①墙杀判定：lead 会话步 job result≠success 或墙 budgets.session_outcome ≠ ok（读 budget_slice，`schemas/foreman-run.v1.schema.json:59` 起面）。②计划残缺判定：plan artifact 缺席或 stitch 退出码≠0 → 派单步禁发（fail-closed，不派残缺单）。③越权写判定：caps-gate `out-of-scope-write`（seat-gates §1.3 判词表）——会话变更集对 `artifacts` 登记写面（lead-plan-segments 唯一工作区面）越界即退出码 1。④门未过判定：`needs.env-check.outputs.foreman_ok != 'true'` → job 短路（现状 `team.yml:52` 门）。⑤**缺席即事件**：派单窗口内 plan_dispatch patch 缺席 → 缺席告警（§0.5）。 |
| **缺口** | 现状定级：**部分**——①②④判据在树；**③无信号面**（lead 会话写无机器 F-1 类守卫，锚件 2 §1/§9 风险 12），⑤无 per-run 报警载体。**v3.0 收口**：caps-gate 三探针补齐（seat-gates §2.1 probes）；对应必死样本 SL-1/SL-4b（acceptance-line-map §2.1/§2.4b）。回合熔断不适用（lead 死法第 1 类占比低，52 轮曾死 lead 面的口径登记于 V-3 收档报告 :44 L-3 行——分账必列 lead/replan 面，v3.0 处置仍为会话级体外终止）。 |

---

## §3 验收席（validator；镜像 validate2 `team.yml:3618`、变体 revalidate `team.yml:1779` / revalidate2 `team.yml:4010`）

门清单：seat-gates §2.4。预算锚：`foreman_run_lib.py:42-45`（480＋adopt 储备 120）；包装接线 `team.yml:1534`（revalidate `:1949`）。

| 字段 | 内容 |
|---|---|
| **怎么死** | 四类：**A. 墙杀**——包装器 480s 墙杀会话（死亡账第 2 类主型：协议致延迟落盘——逐件落盘纪律排在全部推理之后，54A/C 实测 recorder 0 次/删失尾 265.69s 与 250.80s，`docs/V-3-closeout-收档报告.md:47-48`）。**B. 停滞**——请求级停滞（死亡账第 5 类，网关侧成因，`V-3-closeout-收档报告.md` §三 表行 5）占满墙。**C. 证据包破**——manifest sha 复验不齐（篡改嫌疑）或缺件。**D. 判定残缺**——会话死前 verdict-partial 未达 adopt 语义（封章缺席）。 |
| **死了谁知道** | A 类：墙 budgets.session_outcome（FOREMAN_RUN_PATCH 面，`team.yml:1534` 接线）＋workflow job result。B 类：同 A（停滞以墙杀显形，无独立信号——诚实登记：停滞本身不可机内观测，归结构盲区 §8 第 4 条）。C 类：prep manifest sha 门（证据包下载步 fail-closed，锚件 2 §3 入口面）。D 类：D-2 封章面——sealed 粘性（`scripts/team/salvage_verdict.py:93-94`：sealed 后晚期写不得翻封）；封章缺席=round 重验纪律（adopt 面既有，:47 adoptable 语义行）。 |
| **谁处置** | A 类：adopt 储备 120s（`foreman_run_lib.py:44` adopt_reserve_sec=120）承接会话尾段；封章在案的部分判定可采认（fail-closed pick 只采 sealed 齐覆盖件）。**墙杀回收与重验**：revalidate 变体（`team.yml:1779`，一次性哨兵 `:1806-1816` 区段「Refuse a second revalidate」步 fail-closed 拒二次——round-2 锚修正：原记 `:1784-1788` 为 job 头区段，非哨兵步）。**死亡账登记义务**（G-3 口径，`V-3-closeout-收档报告.md:44`）：每例 validator 预算杀必须记录「结论是否已形成 / recorder 调用数 / 删失尾秒数」——v3.0 落位=墙 validation 切片扩 recorder_call_count 字段（缺席即事件载体，§7 判据 2）。C 类：篡改嫌疑=conflicts[].kind=evidence_tampering（handoff-schemas §3 枚举）→fail 传播 replan。D 类：D-2 封章缺席→不采认→重验。 |
| **机器判据** | ①墙杀判定：同 §1 判据①形态（包装器墙 patch 三字段）。②判定残缺判定：verdict-partial 的 final=true 且覆盖 judgeable 集=adoptable（`salvage_verdict.py:47` 语义行、`:30` 定义）；任一不满足=不采认。③**缺席即事件**：verdict 窗口（budgets.droid_wall_sec＋adopt_reserve_sec）截止时 sealed partial 缺席 → 告警事件＋round 重验（§0.5；现状封章语义的常载化——`salvage_verdict.py:45` D-2 seal 语义行，非 final 的 partial 不满足 adoptable 判据即触发重验路径）。④红章判死：checks-exit.json 任一非零 exit 或 marker 按内容红 → verdict 必 fail（`scripts/team/validator_prompt_template.py:97` HARD RULE 机器面——由 v2 schema cause=checks_red＋evidence_refs 承载，handoff-schemas §3）。⑤采认 fail-closed：墙无 validation 切片=pick 拒（`team.yml:4420`）。 |
| **缺口** | 现状定级：**部分**——①②④⑤在树；③缺席报警无 per-run 载体（recorder 服从率 0/4 的生产首验无报警，`V-3-closeout-收档报告.md:11`——59 轮四问题④的验收席面）；死亡账 G-3 登记维度（recorder 调用数/删失尾）无墙字段。**v3.0 收口**：recorder_call_count 入墙切片＋缺席告警（§7 recorder 席判据 2 同源）；对应必死样本 SL-2 伪造叙事桩＋SL-8a 缺席报警（acceptance-line-map §2.2/§2.8）。 |

---

## §4 改计划席（replan）

门清单：seat-gates §2.5。预算锚：`foreman_run_lib.py:48-50`（480）；包装接线 `team.yml:2405-2406`；死因推断段 `team.yml:2259-2282`（F-1 文案赋值 `:2278-2279`）。

| 字段 | 内容 |
|---|---|
| **怎么死** | 四类：**A. 墙杀**——包装器 480s 墙杀（L-3 口径：replan 自身也是 480s 会话，52 轮曾死 lead 面，`V-3-closeout-收档报告.md:44`）。**B. 叙事违约**——死因叙事由脚本内置推断生成（分支缺席→「F-1 检查拒绝」，无机器记录佐证；59 轮四问题①，机制锚件 2 §10-①）——这不是会话死，是**交接物死**（产出不可采认）。**C. 落单违约**——plan-v2 覆盖集/claim 不相交/受保护路径校验拒（落单步机器闸，`team.yml:2420-2423`）。**D. 归责错位**——归责模板只认 wall_killed 分支，exit-1 自崩族输出工人归责措辞（`docs/第58轮-D单追认口径与replan归责缺陷立号.md:23` 缺陷事实行）。 |
| **死了谁知道** | A 类：墙 budgets.session_outcome（`:2405` FOREMAN_RUN_PATCH 面）＋job result。B 类：现状**部分无信号**——推断文案在 prompt 组装期生成，唯一的「知道」面是契约测试把文案钉成正确行为（`tests/test_replan_context_and_skipped_outcome_r53c.py:190` 测试定义、`:198-202` 逐字行、`:205` count==1 断言）——钉子方向反了（把违约钉成期望），v3.0 反转（判据②）。C 类：落单步机器校验拒=无 v2 子单产生（fail-closed 显形）。D 类：attribution_reason 四合并步调用面（`docs/第58轮-D单追认口径与replan归责缺陷立号.md:32` 表——死因在场→中性归因措辞；死因不在场→现行措辞逐字节不变 fail-closed）。 |
| **谁处置** | A 类：同会话墙杀链（replan 红不阻断 assemble always() 收口）。**B 类**：**根治第 4 层处置＋handoff-schemas §9 收口**——死因注入面改由机器构造：plan-v2 的 death_facts 数组由机器步从墙 by-pid 三映射构造（handoff-schemas §4 schema，replan 会话只读）；`f1_rejected_machine_confirmed` 枚举值只能由 origin=machine_guard_record/f1 的证据对象支撑（handoff-schemas §6 构造权单源）；分支缺席＋无 F-1 机器证据=`unknown`（「未明」缺省）——replan 拿 unknown 按缺料处理，不输出死因断言。C 类：校验拒→不落单→链终态 failure（人工入口=issue 评论）。D 类：归责模板分支化已落地（:32 表），v3.0 演进为读 delta cause 枚举渲染（handoff-schemas §9.3 对位段）。 |
| **机器判据** | ①墙杀判定：同 §1 判据①形态。②**叙事证据判定（钉子反转后）**：prompt 含「F-1 check rejected」字样 **当且仅当**存在 origin=f1 的机器证据对象；cause=unknown 时 prompt 死因面板呈现「未明（无机器证据）」（handoff-schemas §9.2 三件套第 3 件；施工时与 schema 演进同批反转 :190-:205 钉子）。③叙事违约判定：caps-gate `narrative-without-evidence`（seat-gates §1.3 判词）——因果结论无证据对象佐证即退出码 1。④落单判定：覆盖集/claim 不相交/受保护路径校验（现状 `team.yml:2420-2423` 机器闸沿用＋plan-v2 v1 schema 校验，handoff-schemas §8 校验点表）。⑤**缺席即事件**：replan 窗口内 plan-v2 落单缺席且 should_replan=true → 告警（§0.5）。 |
| **缺口** | 现状定级：**部分**——①④⑤判据在树（④为机器闸现状）；**②③缺口**：死因推断无佐证且被钉子测试钉成正确行为；narrative 无 schema 无判词。**v3.0 收口**：钉子反转＋plan-v2 schema＋narrative-without-evidence 判词（handoff-schemas §9 全节）；对应必死样本 SL-3b' 伪造死因桩（acceptance-line-map §2.4，59 轮四问题①回归样本）。 |

---

## §5 备料席（prep；镜像 prep2 `team.yml:3107`）

门清单：seat-gates §2.3。纯脚本席（无 droid、无 BYOM）；补卷接线 `team.yml:1223-1226`；报告步令牌 `team.yml:1321`。

| 字段 | 内容 |
|---|---|
| **怎么死** | 三类：**A. 步级超时**——全量 pytest 600s / 卡 checks 300s 步超时（锚件 2 §5；v2.6.4 E 已加，超时即该步红）。**B. merge 失败**——候选分支合成冲突/ls-remote 失败。**C. 守卫拒**——补卷守卫四条件任一不满足（拒=正确行为，但若拒后无下文即链滞留）。 |
| **死了谁知道** | A 类：step 失败→job result（wall_exits 面）。B 类：git 步退出码→job result→validate `needs.prep.result` 不满足（锚件 2 §3 入口面）→下游全静默（结构性可见：链断在 needs 面）。C 类：补卷拒=pack 维持缺件→validator blocked 扫描见缺件（`worker_salvage.py` docstring 产品纪律段）→verdict fail/blocked 语义。 |
| **谁处置** | A/B 类：链失败传播＋人工入口（issue 评论重跑；prep 无自动重试——诚实登记：现状无自动续作，第 3 层续作能力不可施工同理 §0.4）。C 类：**处置=不处置**（fail-closed 拒绝是守卫的正确输出）；拒后的缺件面由 verdict 判 blocked_evidence 走 replan（plan-v2 death_facts 承载缺料事实）。 |
| **机器判据** | ①步级超时判定：`timeout 600s pytest`/`timeout 300s checks` 退出码 124 → 步红。②merge 判定：git 退出码≠0。③守卫四条件：同 §1 判据③（`worker_salvage.py:13`）。④**缺席即事件**：prep_should_run=true 的窗口内 evidence.tar.gz 缺席 → 告警（§0.5；证据包是 validate 的 manifest sha 门输入，缺席必显形，告警使其 per-run 可见）。 |
| **缺口** | 现状定级：**有**（本席判据①-③全在树：步级超时、守卫四条件、merge 退出码）——④缺席告警载体缺（并入 F4 验收线常驻设计）。v3.0 变更仅一点：补卷守卫四条件作为**根治理倒影**接受失败矩阵测试（acceptance-line-map §2.5 SL-5 对其逐条注入违约，断言必红必拒）。 |

---

## §6 装配席（assemble）

门清单：seat-gates §2.6。纯脚本席；PAT 单点 `team.yml:4431`（调用 `:4441`）；墙权威 pick `:4420`；chain_facts 收口 `:4636`；板面权威声明行 `:4599`。

| 字段 | 内容 |
|---|---|
| **怎么死** | 四类：**A. pick 拒**——墙无 validation 切片/切片不可采认，fail-closed pick 拒（`:4420`）。**B. 板面写失败**——PAT 写板 API 失败（限流/权限/网络）。**C. 翻板**——写板终态后被图外自动化翻回（Item closed 内建自动化，翻板演员 `github-project-automation`，三单实测 `docs/板面关单翻板-最小操作指引.md:12-14`；repo 侧不可拦截，专档结论 `:24`）。**D. 收口残缺**——final_status_card patch 缺席/chain_facts 不完整。 |
| **死了谁知道** | A 类：pick 退出码→job result→链终态。B 类：project_state_write 退出码＋`closeout.project_state_written` 布尔（`schemas/foreman-run.v1.schema.json:214`，closeout_slice 面 `:210`）。C 类：现状**图外无信号**——翻板发生在 run 结束后，repo 侧零写入点可拦（专档 :20/:24）；v3.0 信号=board_drift 对账事件（F3 §2.1 图内再同步：漂移对账步记 board_drift＋重写板＋仍漂移则硬评论报警）。D 类：foreman lint 执法面——assemble 收口必须 `--wall-patch final_status_card`（锚件 2 §12 lint 表）。 |
| **谁处置** | A 类：fail-closed 报 failure（不写板不报 pass——**不冒充**）。B 类：重试面现状无（诚实登记）；v3.0 随 board_drift 对账步承载一次重写。**C 类**：**板侧禁绝主责在大哥**（Disable 内建规则或改终态选项，专档 :26-:32 操作指引；「保留原样」不在可行集）＋图内防复发=装配席对账（F3 §2.1 三步：board_drift 记账→PAT 单点重写→硬评论报警；env-check 探测项 WARN 人工巡检）。**诚实边界**：关单发生在 run 结束后时，图内机制是发现与纠正、不是阻断——图内无兜底（硬规则⑩）。D 类：lint 红→CI 拒合。**human_stop 消费缺口**：human_stop 已上墙（schema `:33`）且机器面有消费（validation 判定 `foreman_run_lib.py:232`：adoption_status=failed 须 human_stop 或 run_must_fail 兜底；replan 重试面 `adopt_verdict.py:580-583`：非 revalidate 形态打 human_stop 标志、重试 job 消费之）——**真实缺口＝assemble 收口分支的提前停消费缺席**（锚件 2 §6/§9 风险 13），v3.0 补该分支的消费门（seat-gates §2.6 probes）。 |
| **机器判据** | ①pick 判定：墙 validation 切片缺席或不齐 → pick 退出码 1（fail-closed）。②写板判定：`project_state_written=true` 且 enum 终态合法（closeout_slice 字段，`:210-215` 区段）。③**翻板对账判定**：PAT 读板回查——「工单关闭且 Status≠assemble 写入终态」→ board_drift 事件（判据输入=板面读＋墙 closeout 切片，两机器载体比对）。④收口判定：foreman lint 静态断言（收口步带 --wall-patch final_status_card）。⑤**缺席即事件**：assemble 窗口内 final_status_card patch 缺席 → 告警（§0.5）。⑥human_stop 判定：墙 `human_stop=true`（`:33`）→ assemble 消费分支必须提前停（v3.0 探针钉住消费分支存在性）。 |
| **缺口** | 现状定级：**部分**——①②④在树；**③无信号**（图外翻板，板侧动作待大哥=F3 三态纪律的 blocked 件）；⑤⑥载体缺。**v3.0 收口**：board_drift 对账＋env-check 探测项＋human_stop 消费门＋final_status_card 缺席告警；对应必死样本 SL-6 翻板回归样本＋SL-14 板面写单点违例桩（acceptance-line-map §2.6/§2.13，59 轮四问题③回归样本；RS-3 执法载体=SL-6＋SL-14，SL-7 为 lead 图外写口桩不在此处）。 |

---

## §7 写板席（recorder——目标态独立席）

门清单：seat-gates §2.7。现状承载点：validator prompt 单源 `team.yml:1515`＋prep 补卷器 `team.yml:1223-1226`；D-2 封章 `scripts/team/salvage_verdict.py:93-94`（sealed 粘性）、`:18` PARTIAL_NAME。

| 字段 | 内容 |
|---|---|
| **怎么死** | 三类（本席特有：死法是**缺席**不是崩溃）：**A. 逐件落盘缺席**——会话全程零 recorder 调用或批量落盘（生产首验服从率 0/4、墙杀场景回收 0/2，`docs/V-3-closeout-收档报告.md:11`；工人席对应 58-D 口径：13 次工具调用零次以 handoffs/status 为目标，`docs/第58轮-死亡账分型登记-58D归第1类.md`；锚件 2 §10-④）。**B. 承载会话死**——validator/worker 会话被墙杀，逐件落盘随会话死（validator 面 54A/C：recorder 0 次/删失尾 265.69s 与 250.80s，`V-3-closeout-收档报告.md:47-48`）。**C. 封章缺席**——写了 partial 但未达 final 封章。 |
| **死了谁知道** | A 类：现状**无人知道**——per-run 无 recorder 调用数墙字段、无报警（59 轮四问题④的机制核心，锚件 2 §7/§10-④）；V-3 门只证明受控会话可达标（发版前置人工门），生产 per-run 无报警（`V-3-closeout-收档报告.md` §一）。B 类：随承载席墙 patch 显形。C 类：封章缺席=round 重验纪律（D-2 seal 语义，`salvage_verdict.py:45-47`）。 |
| **谁处置** | **v3.0 立席后的处置链**（立席本身即四问题④的结构化收编，seat-gates §0/§2.7）：①**缺席即事件**（硬规则⑥的旗舰判据）：包装器采样 recorder 调用数与首步落盘时点，窗口内零调用/零落盘 → 告警事件（墙记 recorder_call_count＋硬评论报警）——缺席从「无人知道」变「必有人知道」。②**机器兜底**（根治第 1 层处置复用）：死亡工序缺失 evidence 件由 prep 补卷器机器补写并标 salvaged_from_machine（§0.3 并入）。③**模板单源**（根治第 2 层）：worker prompt 单源增量落盘引导（`worker_prompt_template.py:13`），P-2 口径预期封顶——**措辞无运行时效力，执法靠①②不靠措辞**（防「措辞」冒充「执法」的口径由本席统一登记）。 |
| **机器判据** | ①**缺席判定（本席主判据）**：观察点=包装器采样器（validator/worker 会话）；窗口=首个分析单元内（首步窗口）与 budgets 窗口（全程窗口）；判据=`recorder_call_count==0 或 verdict-partial 落点缺席` → 告警事件（§0.5 判据形态的旗舰实例；载体=schema validation 切片扩 recorder_call_count 字段，施工随 schema 演进同批改锁，handoff-schemas §7.1）。②封章判定：partial sealed 粘性（`salvage_verdict.py:93-94`）＋adoptable 语义（`:47`）——final=true 且覆盖 judgeable 集=可采认。③兜底判定：补卷守卫四条件（§1 判据③）。④迟到写判定：sealed 后晚期写不翻封（粘性，:93-94）。⑤触发面正样本门（G-2 制度，`V-3-closeout-收档报告.md:15`）：recorder 机制上线判据=真实会话流中 tool_call 正样本在案（离线重放只算回收链测试）——本席所有执法上线前必过此门。 |
| **缺口** | 现状定级：**无**（四问题④正席：判据①载体不存在，A 类死法现状零信号）——这是 7 席中唯一「无」级。**v3.0 收口**：立席＋缺席即事件＋墙字段＋硬评论报警；对应必死样本 SL-8a 缺席报警桩（acceptance-line-map §2.8，59 轮四问题④回归样本）。 |

---

## §8 结构盲区（显式列出，照引擎普查表 :94 盲区范式）

| # | 盲区 | 定性 | v3.0 处置 |
|---|---|---|---|
| 1 | **第 3 层回合熔断**：回合粒度执法整体不可施工（§0.4 三条裁定理由） | 结构性不可见（回合是 agent-loop 内部概念，外层不可观测） | 显式不施工登记＋上游三能力立项前置（登记件 :19-:24）；任何章节引用须带本口径 |
| 2 | **请求级停滞**（死亡账第 5 类）：模型请求路径 2–8 分钟停滞，非全局停摆，机内零信号（V-3 收档报告 §三 表行 5） | 结构性不可见（成因在网关侧，仓内无观测点） | 登记为仓外成因（S-3 观测另案）；墙杀显形后按死亡账 G-3 维度登记（删失尾秒数），不在席位判据内虚设判据 |
| 3 | **板面关单后翻板**：run 结束后的人工关单时点无 workflow 触发器可挂（专档 :24 repo 侧不可拦截结论） | 结构性图外（触发面+执行体+写目标三重图外，F3 §2.1） | 板侧禁绝主责（大哥）＋图内发现与纠正（board_drift 对账）；图内侧无阻断能力，不冒充兜底 |
| 4 | **工作区顶层孤儿件**：repo 外工作区顶层 verdict 孤儿（F3 §2.4）无 CI 执法点 | 结构性 repo 外 | 人工巡查判据登记（F3 §4 表④）；设计稿执法面只覆盖 repo 树，诚实声明 |
| 5 | **memory/ 运行态会话面**：hook 体系图外运行，untracked 永不入 git（F3 §2.6） | 结构性图外 | 接口收口（证据入库单点＋席位禁写），不收编运行；59 轮四问题①回归样本从图内可构造（worker-delta 注入路径），不依赖图外面还原现场 |

---

## 附A 本件 file:line 锚清单（供锚解析器）

> 锚判据＝文件在树、行号不越界、锚定内容含预期关键词。「转引」=姊妹底稿锚清单已核实，解析以其附表为准；本件新增锚标 ★（均已实读核实）。

| 锚 | 解析判据（该行应含） | 来源 |
|---|---|---|
| `team.yml:202` | `run_droid_session.py`（lead 包装调用行；--role lead 落 :203） | ★（修正锚件 2 §1 的 :203-204 区段口径，实读 :202 起跨行） |
| `team.yml:599` | `900s`（worker 裸跑行） | 转引 seat-gates 附A |
| `team.yml:710` | `GH_TOKEN`（worker commit 步） | 转引 |
| `team.yml:731` | `reset --soft` | 转引 |
| `team.yml:836` | `write_worker_delta` | 转引 |
| `team.yml:851` | `workers-wall-merge:` | 转引 |
| `team.yml:860` | `prep_should_run` | 转引 |
| `team.yml:885` | `merge_worker_deltas` | 转引 |
| `team.yml:1223` | `worker_salvage`（接线区段起） | 转引 |
| `team.yml:1321` | `GH_TOKEN`（prep 报告步） | 转引 |
| `team.yml:1515` | `build_validator_prompt` | 转引 |
| `team.yml:1534` | `run_droid_session.py`（validator 包装） | 转引 |
| `team.yml:1779` | `revalidate:`（job 头） | 转引 |
| `team.yml:2141` | `replan:`（job 头） | 转引 |
| `team.yml:2259` | `Round-53 fix`（推断注释起） | 转引 |
| `team.yml:2278` | `the round-1 branch for process`（F-1 文案赋值行） | 转引 handoff-schemas 附表 |
| `team.yml:2405` | `run_droid_session.py`（replan 包装） | 转引 |
| `team.yml:2420` | 落单步机器校验区段起 | 转引 handoff-schemas 附表 |
| `team.yml:2697` | `worker2:`（job 头） | 转引 |
| `team.yml:2784` | `900s`（worker2 裸跑） | 转引 |
| `team.yml:3618` | `validate2:`（job 头） | 转引 |
| `team.yml:4010` | `revalidate2:`（job 头） | 转引 |
| `team.yml:4420` | `pick_verdict_from_wall` | 转引 |
| `team.yml:4431` | `PROJECTS_STATE_PAT` | 转引 |
| `team.yml:4441` | `project_state_write` | 转引 |
| `team.yml:4599` | 板面权威审计镜像声明 | 转引 out-of-graph 附A |
| `team.yml:4636` | `assemble_chain_facts` | 转引 |
| `schemas/foreman-run.v1.schema.json:33` | `human_stop` | 转引 |
| `schemas/foreman-run.v1.schema.json:59` | `budget_slice` | ★ |
| `schemas/foreman-run.v1.schema.json:146` | `session_outcome_by_pid` | 转引 |
| `schemas/foreman-run.v1.schema.json:153` | `droid_exit_code_by_pid` | 转引 |
| `schemas/foreman-run.v1.schema.json:157` | `stream_tail_marker_by_pid` | 转引 |
| `schemas/foreman-run.v1.schema.json:210` | `closeout_slice` | 转引 out-of-graph 附A |
| `schemas/foreman-run.v1.schema.json:214` | `project_state_written` | 转引 out-of-graph 附A |
| `scripts/team/foreman_run_lib.py:37` | `"lead": {` | 转引 seat-gates 附A |
| `scripts/team/foreman_run_lib.py:42` | `"validator": {` | ★（droid_wall_sec=480 落 :43、adopt_reserve_sec=120 落 :44） |
| `scripts/team/foreman_run_lib.py:48` | `"replan": {` | ★（droid_wall_sec=480 落 :49） |
| `scripts/team/foreman_run_lib.py:53` | `"worker": {` | 转引 |
| `scripts/team/write_worker_delta.py:42` | `SELF_EXIT_CODES` | 转引 |
| `scripts/team/write_worker_delta.py:45` | `def classify_session_outcome` | 转引 |
| `scripts/team/write_worker_delta.py:63` | 分类分支区段起（124/137→wall_killed、cancelled→job_wall_cancelled） | ★ |
| `scripts/team/worker_salvage.py:13` | `The guard is machine-judged and fail-closed`（四条件 docstring） | 转引 |
| `scripts/team/salvage_verdict.py:47` | adoptable 语义行 | ★（F5 总装实读修正：原误记 `worker_salvage.py:47`——该行实为补卷产品清单行；adoptable 语义在 salvage_verdict.py:45-47 区段） |
| `scripts/team/salvage_verdict.py:18` | `PARTIAL_NAME` | 转引 |
| `scripts/team/salvage_verdict.py:30` | `def salvage_verdict` | 转引 handoff-schemas 附表 |
| `scripts/team/salvage_verdict.py:93` | sealed 粘性（跨 :93-:94） | ★ |
| `scripts/team/salvage_verdict.py:45` | `final` is the D-2 seal 语义行（跨 :45-:47） | ★ |
| `scripts/team/attribution_reason.py:26` | `def blocked_reason` | ★ |
| `scripts/team/attribution_reason.py:65` | `def blocked_report_line` | ★ |
| `scripts/team/attribution_reason.py:75` | `def neutral_attribution` | ★ |
| `scripts/team/validator_prompt_template.py:97` | `HARD RULE — a red mandated check is never a pass` | ★ |
| `scripts/team/validator_prompt_template.py:98` | 冲突升级必录行 | ★（转引 handoff-schemas 附表） |
| `scripts/team/worker_prompt_template.py:13` | `Incremental persistence guidance`（第 2 层载体） | ★ |
| `scripts/team/worker_prompt_template.py:67` | status.json 键面 | ★ |
| `scripts/team/lint_workflow_budgets.py:43` | worker/900s 豁免分支 | ★ |
| `scripts/team/budget_resolve.py:73` | validator 480 硬断言行 | ★ |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:190` | `def test_replan_prompt_names_absent_branch_as_real_cause`（钉子定义） | ★ |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:201` | F-1 文案逐字行（跨 :201-:202——:201 分支缺席行、:202 F-1 拒绝括注行） | ★ |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:205` | `prompt.count(line) == 1` 断言 | ★ |
| `docs/回合熔断上游特性需求登记-droidCLI.md:11` | `## 为何本仓不可施工`（三条裁定理由段起） | ★ |
| `docs/回合熔断上游特性需求登记-droidCLI.md:13` | droid CLI 无回合预算接口 | ★ |
| `docs/回合熔断上游特性需求登记-droidCLI.md:17` | `第 3 层（回合级熔断）不在本仓施工`（结论行） | ★ |
| `docs/回合熔断上游特性需求登记-droidCLI.md:19` | `## 上游需要提供的能力`（三能力表） | ★ |
| `docs/R58D-收尾决策留痕-NC6与遗留决策点.md:5` | 十文件子集维持现状裁定行 | ★ |
| `docs/V-3-closeout-收档报告.md:11` | 逐件落盘服从率 0/4（Opus 终审引文行） | ★ |
| `docs/V-3-closeout-收档报告.md:15` | G-2 触发面正样本上线门 | ★ |
| `docs/V-3-closeout-收档报告.md:34` | `## 三、死亡账分账五类` | ★ |
| `docs/V-3-closeout-收档报告.md:44` | G-3 登记维度＋L-3 行 | ★ |
| `docs/V-3-closeout-收档报告.md:47` | A 席死亡账实测行（recorder 0 次/删失尾 265.69s） | ★ |
| `docs/V-3-closeout-收档报告.md:48` | C 席死亡账实测行（recorder 0 次/删失尾 250.80s） | ★ |
| `docs/第58轮-D单追认口径与replan归责缺陷立号.md:23` | 缺陷事实行（硬编码归责预设） | ★ |
| `docs/第58轮-D单追认口径与replan归责缺陷立号.md:32` | 归责模板分支化表行 | ★ |
| `docs/第58轮-死亡账分型登记-58D归第1类.md:21` | hslconv 死法行（900s 墙/末事件 interrupt） | ★ |
| `docs/第58轮-死亡账分型登记-58D归第1类.md:22` | 膨胀回合 64.41% 行 | ★ |
| `docs/板面关单翻板-最小操作指引.md:12` | 三单实测表（跨 :12-:14） | 转引 out-of-graph 附A |
| `docs/板面关单翻板-最小操作指引.md:20` | 仓内零写入点结论行 | ★ |
| `docs/板面关单翻板-最小操作指引.md:24` | repo 内无可拦截结论行 | ★ |
| `docs/板面关单翻板-最小操作指引.md:26` | 板侧操作节起 | ★ |
| 引擎：`docs/guides/exception-point-inventory.md:23/:27/:94` | 普查表形制（要点 10） | 转引 form-basis 附表 |

## 附B 席位×判据×必死样本索引（acceptance-line-map 的反向入口）

| 席 | 失败规范判据 | 对应必死样本（acceptance-line-map §2/§5） | 59 轮回归样本 |
|---|---|---|---|
| worker | ①②③④⑤ | SL-3 恒挂桩、SL-3b 越界写桩、SL-5 根治倒影矩阵 | RS-2（900s 不执法）、RS-1（虚构死因的结局面） |
| lead | ①②③④⑤ | SL-1 会话墙恒挂、SL-4b 图外写口桩 | —（RS 组四问题不涉 lead） |
| validator | ①②③④⑤ | SL-2 伪造叙事桩、SL-3 恒挂桩、SL-8a 缺席报警（validator 面） | RS-4（recorder 缺席报警） |
| replan | ①②③④⑤ | SL-3b' 伪造死因桩（plan-v2 面） | RS-1（replan 虚构死因钉子反转） |
| prep | ①②③④ | SL-5 根治倒影矩阵（四条件逐条违约） | — |
| assemble | ①②③④⑤⑥ | SL-6 翻板回归桩、SL-7 图外写口桩 | RS-3（板面翻板） |
| recorder | ①②③④⑤ | SL-8a 缺席报警桩（acceptance-line-map §2.8） | RS-4（缺席即事件） |
