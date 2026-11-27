# 验收线（acceptance-line-map 底稿）——每墙每门必死样本＋执法延迟实测口径

> 底稿（mission F4/failure-specs 产出；主设计稿 §6 验收线章素材）。本件给**每道墙/每个门**配：①必死样本设计（常驻 pytest 负例——fake-droid 桩注入违约会话：恒挂/越界写/伪造叙事/图外写口，断言守卫必红必杀，零网络零真树污染）；②实测执法延迟口径（超时点到进程组真死的时间差，多次采样取上界，CI 每次跑出实测数）；③「没有活验数字不算建成」判据；④缺席即事件不变量检查设计；⑤59 轮四问题回归样本设计。逐席失败规范（判据侧）见姊妹底稿 `failure-specs.md`（本件 SL 样本与其判据经其附B 反向索引互锁）。
>
> **真源声明**：执法形制（终止序列/哨兵语义/预算公式）以 `docs/wall-v3/form-basis.md` §10 补遗（原物锚：引擎仓 `src/infra_core/engine/droid_review/run_lead.sh:9-10`/`:282`/`:286`/`:52-55`）为准；常驻必死形态先例以 form-basis 要点 7 补遗（`tests/test_lead_engine.py:1041`/`:1044`/`:794` hang 桩 E2E 族）为形制对位物。现状行号转引 `docs/wall-v3/as-is-capability-inventory.md`（锚件 2）。本件全部 file:line 锚经实读核实（2026-11-27 快照，测试仓 R58-D 收尾态基线 564ce30）。
>
> **CI 落位纪律**（承 NC-6 裁定口径，`docs/R58D-收尾决策留痕-NC6与遗留决策点.md:5`）：本件定义的常驻负例族目标态载体＝`tests/test_wall_v3_design_contract.py`（设计契约测试，F5 纯新增）＋ `tests/fixtures/wall-v3/`；既有守卫负例族（worker_salvage/worker_delta/attribution/f5 系在树测试）已在 `pytest tests/ -q` 全套件门内（257 用例，NC-6 留痕 §二表）。CI 子集扩面属 workflow 门清单变更，须单独呈裁——本件不预设扩面。
>
> **版本口径**：本件属设计稿 v3.0 体系，作废 v2.7~v2.10 账面墙口径。

---

## §1 口径总纲（读各节前必读）

### 1.1 必死样本定义与硬性要求

**必死样本**＝对一个墙/门注入**确定的违约输入**、断言执法体**必红必杀**的常驻自动化负例。「必死」三要素，缺一不成立：

1. **确定性注入**：违约输入由桩（fake-droid / 内存变异 / 文本夹具）确定性地构造，不依赖网络、真树、真凭证、真实 droid 进程——**零网络、零真树污染**（零真树判据：写面全部在 tmp 探针 tree 或内存对象；对位引擎负例形制 form-basis 要点 3 负对照共用生产校验路径、`tests/test_module_wall.py` tmp 探针 tree 先例）。
2. **守卫在岗断言**：断言对象是**守卫本体的退出态**（退出码 1/判词点名/拒收行为），不是守卫源码存在性——每样本必须真跑守卫（与生产校验共用同一实现），红了才算过（负例绿=守卫死=样本红）。
3. **必杀断言**（对执法类墙）：断言违约会话**被终结**（进程组不存在/哨兵在案/产物不采信），且终结证据上墙——不只断言「守卫报红」，还断言「违约者真死」。

**常驻要求**：全部样本进 `pytest tests/ -q` 全套件门（基线随批次增长，以 features.json/handoff 最新实测为准——当前 953 passed＋2 skipped 含设计契约测试；原 599+2 为 R58-D 收尾态历史值）；红线=任何样本在本仓测试环境 flaky（网络/时序依赖超阈值）——桩设计必须确定性（时钟由注入、随机由种子、无外部服务）。

**对位先例**（引擎仓已验证形态，form-basis 附表锚）：`tests/test_lead_engine.py:1041` `TestRunLeadBoundedExitE2E`（吊死样本常驻 CI：mode="hang" 桩→必触发 soft_timeout 遗书；turn_spam→轮限哨兵；exit137→恰重试一次；哨兵在案→产物不采信）；`:794` fake droid 桩 mode="hang" 分支；`:792` 哨兵文件写入。**领班域 SL 族按此形制落**。

### 1.2 执法延迟实测口径（硬规则④「没有活验数字不算建成」）

**定义**（对位任务书口径逐字）：执法延迟 = **超时点到进程组真死的时间差**。三个时点全部机器可测：

| 时点 | 定义 | 采样实现 |
|---|---|---|
| T0＝超时点 | 预算到期时刻：包装器预算计时器到期（墙杀样本=droid_wall_sec；软超时样本=job_timeout_sec−400——基座=job timeout，与引擎 `run_lead.sh:6` 口径对应；由样本参数指定） | 桩会话内记录：包装器注入 `FAKE_DROID_BUDGET_EPOCH`，桩在收到 TERM 时读自身单调钟与该 epoch 差 |
| T1＝终结发起 | 执法体发起终结：哨兵写入时刻（`lead-terminated.reason` 同形态哨兵，目标态 `session-terminated.reason`） | 包装器写哨兵时刻（哨兵文件 mtime 或哨兵内记录的单调钟值） |
| T2＝进程组真死 | 被管进程组最后成员退出：waitpid(-pgid) 返回（对位引擎 `run_lead.sh:282` 负 PID 组信号→wait 收尸形态） | 监督者 wait 收尸时刻＋桩进程退出时向哨兵目录写 exit-stamp |

**延迟 L ＝ T2 − T0**（含 T0→T1 的哨兵延迟＋T1→T2 的 TERM→宽限→KILL 序列耗时）。**口径细则**：

- **多次采样取上界**：每类执法墙每次 CI 跑 **N≥5 个采样会话**（参数化桩：预算到期后分别以「立即死/TERM 后拖延/吞 TERM 靠 KILL」三种抗死形态各≥1 采样，另加 2 个普通采样），实测值取**最大值（上界）**为该墙本次执法延迟报告值——上界才暴露最坏抗死形态的执法成本，均值会掩埋 KILL 路径。
- **CI 每次出实测数**：延迟报告落 CI 输出（pytest 报告段：`SL-x enforcement-latency upper-bound = <秒>`）＋可选落 artifact（目标态 `wall-v3-latency.json`：`{sample_id, wall, budget_sec, t0, t1, t2, latency_sec, kill_path: term|kill_after|grace}` 逐采样行）。**报告中数字必须来自本次运行的实测**，禁止常量断言（「延迟<10s」式断言只许作为 sanity 上限护栏，且必须与实测数同时报告）。
- **上界预算护栏**：延迟实测值必须满足设计上界。执法延迟 L=T2−T0 的正确上界是**「宽限＋SIGKILL 完成期」**——T0 之后包装器立即发起终止序列（写哨兵→TERM 组→宽限→KILL 组），序列耗时只有哨兵写入＋宽限等待＋KILL 传播三段，400s 的软超时余量是「哨兵先于 GitHub job 硬杀」的作业窗口（引擎 `droid-review-lead.yml:35-37` margin 口径），**不是执法延迟的上界**。故：**全部软超时与墙杀样本 L ≤ 宽限秒＋SIGKILL 完成期余量**（目标态宽限=10s 对位引擎 `LEAD_KILL_GRACE_SEC` 默认，`run_lead.sh:55`；KILL 完成期余量取 10s 采样护栏）。**实测超上界=墙建成失败**（判据 §1.3 第 3 条）。
- **无真 droid 依赖**：延迟实测对象是**包装器执法路径**（哨兵→SIGTERM 组→宽限→SIGKILL 组），被杀者是桩进程组——桩表现抗死形态（忽略 TERM、睡眠、fork 孤儿持管道），执法通道特性（组信号整组收、不依赖被管进程配合）因此被真实 exercised。45B 孤儿拖管道形态（锚件 2 §10-②）在桩内复现：桩 fork 子进程继承管道后父吞 TERM，断言 KILL 后**整个进程组**（含孤儿）不存在。

**缺席类事件的延迟口径**（§4）：缺席即事件无「超时点到真死」语义（没有可杀的对象），其延迟口径＝**告警事件产出时延**（窗口截止时点→告警事件上墙时点，同采样纪律：N≥5 取上界、CI 出实测数）。

### 1.3 「没有活验数字不算建成」判据（硬规则④收口条款，入稿声明）

> **墙的建成判据不是「守卫存在」「lint 全绿」「文档成文」，而是四条活验数字，缺一即未建成：**
>
> 1. **必死样本全红率**：SL 族每个样本对其目标守卫的红灯率＝100%（守卫对违约输入必红；守卫对合法输入必绿——红绿对照对全）。
> 2. **执法延迟上界实测数**：每面执法墙本次 CI 的 L 上界数字存在且 ≤ 设计上界；**该数字是本次运行的实测值**（非历史值、非常量）。
> 3. **哨兵在案不采信率**：违约会话的产物采认率＝0%（哨兵在案→delta/verdict/plan-v2 一律不采信，强制失败优先，对位引擎哨兵语义 `run_lead.sh:10`）。
> 4. **缺席报警触发率**：缺席注入样本的告警触发率＝100%，且告警事件含可定位字段（席位/窗口/缺席面）。
>
> 四条全部由 CI 常驻测试输出数字，任何人复跑 `pytest tests/ -q` 可复现。**没有这四组数字的墙，一律按「未建成」登记**——纸面有门不执法的形态（引擎 VAL-M4-004/007 缺口，form-basis §11.1）在领班域按禁抄项处理。

### 1.4 墙/门清单（SL 样本覆盖对象）

| 墙/门 | 执法载体 | SL 样本 | 59 轮回归样本 |
|---|---|---|---|
| 会话墙（lead/worker/validator/replan） | 包装器体外执法（哨兵→TERM 组→宽限→KILL 组） | SL-1（lead 恒挂）、SL-3（worker 恒挂＋孤儿拖管道） | RS-2（900s 不执法） |
| 写目标门（F-1 判词化） | caps-gate `out-of-scope-write`＋包装器写预授权（事中守卫） | SL-3b（worker 越界写）、SL-4b（lead 图外写口） | RS-1（越界写结局面，机制面非叙事面） |
| 证据授权门 | verdict v2/plan-v2 schema＋`narrative-without-evidence` 判词＋构造权单源（handoff-schemas §6/§8） | SL-2（validator 伪造叙事）、SL-3b'（replan 伪造死因）、SL-11a（构造权越权） | RS-1（replan 虚构死因钉子反转） |
| 体外执法墙本身（工人席收编后） | 包装器执行体（预算从门清单读＋组信号） | SL-3（同上，兼测包装器接线） | RS-2 |
| 补卷守卫（根治 1 倒影） | `worker_salvage.py:13` 四条件 fail-closed | SL-5（四条件逐条违约） | RS-2/RS-4 关联 |
| 板面终态门 | assemble board_drift 对账＋PAT 单点 | SL-6（翻板回归）、SL-7（图外写口） | RS-3（板面翻板） |
| 缺席即事件（recorder/verdict/delta/patch/evidence manifest 面） | 包装器采样＋墙计数＋硬评论报警 | SL-8（缺席注入族 a-e） | RS-4（recorder 缺席报警） |
| 令牌 scope 门 | validator 双置空＋replan 拆门＋caps-gate `token-scope-violation` | SL-4 族（越权令牌注入） | — |
| 交接口枚举门 | worker-delta v2/verdict v2/plan-v2 v1/handoff v1 schema（handoff-schemas §2-§5 违约表 W-1..H-3） | SL-9（枚举外值/悬挂引用族） | RS-1 |
| caps-gate 判词负例门（工具/制品/事件/状态读面） | caps-gate 文本断言层（`unregistered-tool-call`/`undeclared-artifact`/`undeclared-event`/`undeclared-state-read` 判词） | SL-10a/b/c/d | — |
| 登记面升级闸门 | caps-gate `caps-schema-drift`＋`mixed-registry-change`＋`evidence-construct-violation` 判词 | SL-11a/b/c | — |
| 钥匙面升级闸与旁路面 | 钥匙面守卫（`unregistered-bypass-surface`/`mixed-key-registry-change` 判词，out-of-graph §3.6 判词枚举） | SL-12a/b | — |
| 席位 probe 专属门（五 probe：lead 接线锁/prep 候选分支越权/validator D-2 封章粘滞/assemble human_stop＋pick 变体） | 包装器 caps load＋caps-gate 文本层＋adopt/pick 执法本体 | SL-13a-e（逐 probe 映射表见本节末） | — |

**判词 × 样本满映射表（caps-gate 十判词＋钥匙面五判词 × SL 样本，逐判词至少一条必死样本设计；§2 的 SL 族是本表判据载体的展开）**：

| # | 判词 | 样本 ID | 样本设计要点（注入面照既有 SL 族形制——文本级注入＋守卫在岗断言＋判词点名红＋干净对照绿） |
|---|---|---|---|
| 1 | `unregistered-tool-call` | SL-10a | 注入：workflow 文本夹具给席位步新增门清单 api/local_uses 白名单外的会话工具调用面（如 worker 步注入 gh api 写调用）；断言：caps-gate 判词点名红（席位×工具未登记）＋现状四文件原树绿 |
| 2 | `out-of-scope-write` | SL-3b（会话层）＋SL-4b（文本层） | 既有族：SL-3b 卡面 allowed 外文件注入→守卫拒；SL-4b lead 步产物落点越登记面→判词红 |
| 3 | `token-scope-violation` | SL-4 族 | 既有族：非授权席位步注入 `${{ secrets.PROJECTS_STATE_PAT }}`／validator 族注入 GH 写令牌→判词红；干净对照绿 |
| 4 | `undeclared-artifact` | SL-10b | 注入：席位步新增登记 artifacts 面外产物落点（文本级：workflow 产物路径/write 面不在该席 artifacts 登记集）；断言：`undeclared-artifact` 判词点名红＋对照绿 |
| 5 | `undeclared-event` | SL-10c | 注入：席位步新增登记 events_produced/consumed 名单外事件面（如 prep 步注入 issue close 调用——其 events_produced 无关单权）；断言：判词红＋对照绿 |
| 6 | `undeclared-state-read` | SL-10d | 注入：席位步新增登记 state_reads 面外状态读取面（如 recorder 步注入跨席 packs 树读——其 state_reads=本会话中间态）；断言：判词红＋对照绿 |
| 7 | `narrative-without-evidence` | SL-2（validator）＋SL-3b'（replan） | 既有族：cause 非空而 evidence_refs 空/叙事内嵌判定→判词红＋schema 拒 |
| 8 | `evidence-construct-violation` | SL-11a | 注入：非核查环节构造证据对象（lead/worker/replan/assemble 会话产物内含 evidence 对象字段——构造权白名单外，handoff-schemas §6）；断言：判词红（构造权主体×对象不匹配）＋validator/机器守卫步合法构造对照绿 |
| 9 | `caps-schema-drift` | SL-11b | 注入：内存变异 foreman-caps 登记段——增删键/改词表而不同批改契约测试（对位引擎要点 3 同批改锁）；断言：caps-gate schema 校验 exit 1 判词点名（漂移键/漂移词）＋合法登记对照绿 |
| 10 | `mixed-registry-change` | SL-11c | 注入：变更集文本夹具改 `foreman-caps.v1.toml` 门清单行而不带 `wall-registry-change: true` 声明行；断言：判词红；带声明对照绿（对位引擎判词形制 `check_module_wall.py:131` 常量） |
| 11 | `orphan-secret-expansion` | SL-7 第④注入 | 既有族：`${{ secrets.* }}` 展开位点≠台账锚集（位点扫描含 droid.yml/droid-probe.yml/probe6.yml 全生产树）→红 |
| 12 | `anchor-drift` | SL-7 第④注入同面 | 锚集失配向（登记锚集含已消失位点）→红；与判据 11 同载体双向断言 |
| 13 | `value-leak` | SL-7 第①注入 | 既有族：PAT 前缀族字面注入生产文本→红（例外位=件②夹具哑值显式登记，拆除批消除） |
| 14 | `unregistered-bypass-surface` | SL-12a | 注入：台账 `[[external_face]]`/`[[orphan]]` 外新增旁路面（文本级：新增 workflow 直写 `~/.factory/settings.json` 或 verdict 白名单外落点而台账无登记行）；断言：判词红＋已登记面（memory 树/runner 会话配置/探针族）对照绿 |
| 15 | `mixed-key-registry-change` | SL-12b | 注入：变更集改台账（foreman-keys.toml）或守卫本体而不带 `key-registry-change: true` 声明行；断言：判词红；带声明对照绿（升级闸常量对位引擎 `check_module_wall.py:131` 形制） |

判词覆盖口径：caps-gate 十判词（seat-gates §1.3 表）在本表 1-10 行逐条有样本；钥匙面五判词（out-of-graph §3.6 判词枚举）在 11-15 行逐条有样本——**「每墙每门至少一条必死样本」对判词面满覆盖成立**；两个既有族样本（SL-7 第①/④注入）复用其 §2.7 设计不重复展开。缺席即事件五不变量面（INV-1..7 中可注入面）由 SL-8a-e 承载（§2.8）。

**席位 probe→SL 显式映射表（逐 probe 一行；seat-gates §2 各席 probes 键句中的每条可注入 probe 逐条入表，无毯式归属——「本席 probes 归 SL-x」式整席折叠声明废止，round-2 实证毯式句下五 probe 零样本）**：

| probe | 所属席位 | 承载 SL | SL 节 | 注入面 | 断言 |
|---|---|---|---|---|---|
| 接线锁（门清单键缺失→包装器拒启） | lead | SL-13a | §2.13 | 包装器 caps load 面注入：内存变异门清单删 `[seat.lead]` 段 / budgets 键不齐 | fail-loud exit 2＋零会话启动＋零产物 |
| 写目标越界三探针（写越界/令牌越界/未登记工具） | lead | SL-4b＋SL-10a | §2.4b/§2.10 | workflow 文本层注入：lead 步产物落登记面外 / 门清单外工具调用 | 判词点名红＋现状树对照绿 |
| 候选分支越权写 | prep | SL-13b | §2.13 | 文本层注入：非 prep 席位步 push `team/issue-N/candidate-R` 形态 | F 类守卫红（undeclared-artifact/out-of-scope-write 判词）＋现状树对照绿 |
| 补卷守卫四条件负例 | prep | SL-5 | §2.5 | 违约 pack 内存构造（merged=false/F-1 越界/红 checks/exit-0+ok） | 五变体全不补卷＋绿路对照补卷成功 |
| verdict schema 执法负例 | validator | SL-2／SL-9（V 行） | §2.2/§2.9 | verdict-partial 内存构造：枚举外 cause/无证据 refs/reason 内嵌判定 | schema 拒＋adopt 拒采＋判定通道不读 reason |
| D-2 封章粘滞 | validator | SL-13c | §2.13 | verdict 半套注入（final 章在而 evidence_refs 缺/晚期写翻 partial） | sealed 粘性拒翻＋半套不达 adoptable 拒采 |
| 伪叙事钉子反转三负例 | replan | SL-3b' | §2.4 | worker-delta/plan-v2 违约构造（枚举外 F-1 文案/悬挂引用/无证据 f1 断言） | 拒＋钉子反转正样本成立 |
| droid 会话禁入 | assemble | SL-13d 前置断言 | §2.13 | 桩注入 assemble 步 droid 会话调用面 | unregistered-tool-call 红（零 droid 席探针） |
| human_stop 消费 | assemble | SL-13d | §2.13 | 墙注入 human_stop 事件而收口步桩化照常 pick | 提前停分支必被消费；未消费=红＋零板面写 |
| pick fail-closed | assemble | SL-13e | §2.13 | 墙 validation 切片存在但整片 adoptable=false（全 partial 未封章） | pick 拒=零板面写/零 PR/零关单；缺切片正例同断言（在树） |
| 缺席即事件采样 | recorder | SL-8a | §2.8 | 桩 validator 会话全程零 recorder 调用零落盘 | 告警必产＋recorder_call_count=0 上墙＋字段可定位 |

（worker 席 probes——F-1 越界守卫＋裸跑探针——分别由 SL-3b/SL-3b' 与 SL-3/RS-2 承载，已在 §2.3/§2.4 逐样本展开，不另立行。）

### 1.5 桩形态总登记（fake-droid 桩约定）

全部 SL 执法类样本共用一个 fake-droid 桩协议（形制对位引擎 `tests/test_lead_engine.py:794` FAKE_DROID_CONFIG 桩）：

```
fake-droid（tests/fixtures/wall-v3/fake_droid.py，目标态）
  --mode hang|hang-ignore-term|fork-orphan|write-oob|exit <code>|quiet
  --budget-epoch-env FAKE_DROID_BUDGET_EPOCH   # T0 采样面
  --sentinel-dir <dir>                          # exit-stamp 写入面（T2 采样面）
  --oob-path <path>                             # 越界写目标（SL-3b/SL-4b）
  --narrative-file <file>                       # 伪造叙事注入面（SL-2/SL-3b'）
```

桩纪律：零网络；写面限 tmp；TERM 抗死形态显式参数化（`hang`=TERM 后 30s 内死、`hang-ignore-term`=吞 TERM 只死 KILL、`fork-orphan`=fork 孤儿持管道后父退出）；每次运行输出机器可读 trace（模式/时点/退出路径）供延迟采样聚合。

---

## §2 SL 必死样本设计（逐墙逐门，常驻 pytest 负例）

> 每样本六要素：注入（桩形态）→执法体（被测守卫）→断言（必红＋必杀）→判据载体（机器可断言的退出态）→延迟采样（适用执法类墙）→59 轮/判据对位。目标态载体统一为 `tests/test_wall_v3_design_contract.py`＋`tests/fixtures/wall-v3/`（F5 落树）；标注「在树先例」的断言面已由既有测试承载（NC-6 留痕 §二表），v3.0 底稿对齐其断言面。

### 2.1 SL-1 领班席会话墙恒挂桩（对应 failure-specs §2 lead 判据①⑤）

- **注入**：fake-droid `--mode hang`（永挂，不产出分段卡）；包装器以 lead 门清单预算（600s，`foreman_run_lib.py:38`）启动，样本内预算按比例缩放（测试参数 wall_sec=2s 级，不真等 600s——预算值注入而非读取生产门清单值，生产接线由契约测试另钉）。
- **执法体**：包装器体外执法（哨兵→SIGTERM 组→宽限→SIGKILL 组，引擎终止序列形制）。
- **断言**：①软超时哨兵在案（reason=soft_timeout 同形态）；②进程组真死（waitpid(-pgid) 返回＋桩 exit-stamp 在）；③lead 产物不采信——分段卡缺失时 stitch 不产 team-plan.json（fail-closed，§1.3 判据 3）；④lead 预算 patch session_outcome≠ok 上墙。
- **判据载体**：哨兵文件内容＋墙 budgets 切片字段＋stitch 退出码。
- **延迟采样**：T0=预算到期，L 上界报告（§1.2）。
- **在树先例**：`tests/test_lead_engine.py:1041`/`:1044`（引擎侧同形制 E2E——本样本是领班域对位物）。

### 2.2 SL-2 验收席伪造叙事桩（对应 failure-specs §3 判据②④；59 轮四问题①validator 面）

- **注入**：构造违约 verdict-partial——judged[].cause=checks_red 而 evidence_refs=[]；以及 judged[].cause=枚举外自由值（"pass with concerns"）；以及 reason 字段内嵌 `"verdict": "pass"` 试图以叙事承载判定（handoff-schemas §3.1 V-2/V-3/V-6 三注入同源）。
- **执法体**：verdict v2 schema 校验（jsonschema 校验器，负对照与生产共用同一实现）＋caps-gate `narrative-without-evidence` 判词＋adopt 采认步 fail-closed。
- **断言**：①schema 校验拒（三注入全拒）；②adopt 拒采（无 sealed 齐覆盖=不采认，`salvage_verdict.py:45-47` D-2 seal 语义）；③判定通道只读枚举与证据引用——V-6 注入不得翻转机器判定（负面断言）。
- **判据载体**：schema 校验器异常＋adopt 退出码＋caps-gate 判词输出。
- **在树先例**：红章判死机器面=`validator_prompt_template.py:97`（HARD RULE），v2 schema 载体归 handoff-schemas §3。

### 2.3 SL-3 工人席恒挂＋孤儿拖管道桩（对应 failure-specs §1 判据①④⑤；59 轮四问题②回归底座）

- **注入**：fake-droid `--mode fork-orphan`（fork 孤儿继承管道后父进程吞 TERM 不退，复现 45B 形态：孤儿子进程持管道使 step 活到 job 墙，锚件 2 §10-②）；预算注入 2s 级。
- **执法体**：v3.0 工人席包装器（seat-gates §4 收编后形态——预算从门清单读、哨兵→TERM **进程组**→宽限→KILL **进程组**；对位引擎 `run_lead.sh:282/:286` 负 PID 组信号）。
- **断言**：①**进程组整组收**：KILL 后父子进程与孤儿全部不存在（孤儿不存活=执法通道不依赖被管进程配合的真实证明）；②哨兵在案→worker-delta 不采信为 ok（强制失败优先）；③delta 三字段 wall_killed 分类正确（`write_worker_delta.py:45` 分类器对桩 trace 判 124/137→wall_killed）；④**缺席即事件**：会话死于落盘前→delta 仍上墙（机器分类不依赖会话配合）。
- **判据载体**：进程存在性探针（os.killpg(pgid, 0) 抛 ProcessLookupError）＋哨兵＋墙 workers 切片。
- **延迟采样**：本样本是延迟上界的**主采样源**（fork-orphan=最坏抗死形态）。
- **在树先例**：`tests/test_worker_salvage.py:293`（exit-0+ok 墙不被补卷翻案的守卫负例）；墙杀夹具=`tests/fixtures/worker-r58d/worker-delta-wall-killed.json`（58-D 真实形态夹具，sha256 对账在 `tests/test_worker_r58d_fixtures.py`）。
- **59 轮回归对位**：RS-2（§5）以本样本的执法形态为「反转后正解」——现状裸跑形态（`team.yml:599`）对同一注入必然拖到 job 墙（45B 实证），v3.0 包装器必须整组收。

### 2.4 SL-3b 工人越界写桩＋SL-3b' replan 伪造死因桩（写目标门＋证据授权门；59 轮四问题①回归核心）

**SL-3b（越界写，对应 failure-specs §1 判据③面）**：

- **注入**：违约会话产物含卡面 allowed 集合外文件（越界路径注入 tmp 探针 tree）；以及 status.json files 字段含 F-1 拒过的路径（handoff-schemas §5.1 H-3 注入）。
- **执法体**：F-1 守卫（现行载体逻辑，`team.yml:731` reset --soft 后逐文件比对面）＋v3.0 caps-gate `out-of-scope-write` 判词（事中守卫化，seat-gates §4.3 ②）。
- **断言**：①越界写被拒（守卫退出码 1，拒绝清单点名越界文件）；②越界文件不得进入 delta files 面（H-3 双红）；③**红绿对照**：合法卡面产物同场跑=绿（守卫只对越界红）。
- **判据载体**：守卫退出码＋拒绝清单。
- **在树先例**：F-1 在树契约面（worker 守卫测试族，NC-6 留痕 §二表）。

**SL-3b'（replan 伪造死因，对应 failure-specs §4 判据②③；RS-1 的断言面）**：

- **注入**：worker-delta v2 cause=「F-1 检查拒绝」自由文本（枚举外，W-3 注入）；plan-v2 death_facts[].cause=f1_rejected_machine_confirmed 而证据登记无 origin=f1 对象（P-1 注入）；narrative 含「F-1 check rejected」字样而 cause=unknown（P-2 注入）。
- **执法体**：worker-delta/plan-v2 schema 校验＋证据登记解析器（悬挂引用拒）＋caps-gate `narrative-without-evidence`。
- **断言**：①枚举外 cause 拒；②无机器证据的 f1 断言拒（构造权：origin=machine_guard_record/f1 白名单外即红，handoff-schemas §6）；③cause=unknown＋F-1 字样=narrative-without-evidence 红；④**钉子反转正样本**：存在合法 origin=f1 证据对象时，prompt 含 F-1 文案且恰好一次（反转后真值条件成立）。
- **判据载体**：schema 校验＋证据解析＋反转后契约测试（目标态载体改造 `tests/test_replan_context_and_skipped_outcome_r53c.py:190` 测试语义——现状 :201-:202 逐字行、:205 count==1 断言反转为条件断言，施工时与 schema 演进同批，handoff-schemas §9.2）。

### 2.4b SL-4 族令牌 scope 注入桩＋SL-4b 领班图外写口桩（令牌 scope 门＋写入口收口门；对应 failure-specs §2 lead 判据③、§7 判据①）

> SL-4 族＝越权令牌注入样本（令牌 scope 门），SL-4b＝领班席图外写口样本（写入口收口门）。两者注入面同为 workflow 文本层（SL-7 载体同面），执法体同为 caps-gate 判词，故设计共节——但对象门不同（token-scope-violation vs out-of-scope-write/orphan-secret-expansion），样本分立命名、断言分立点名。

**SL-4 族（越权令牌注入）**：

- **注入**：workflow 文本夹具注入两类令牌越界形态：①非授权席位步出现板面 PAT 展开位点（`${{ secrets.PROJECTS_STATE_PAT }}` 出现在 assemble PAT 单点之外）；②validator 族步出现 GH 写令牌展开（双置空面被新增 `${{ secrets.* }}` 令牌注入破坏）。
- **执法体**：caps-gate 文本断言层（`token-scope-violation` 判词）＋secrets 位点对账（`${{ secrets.* }}` 展开位点集合≠台账锚集即红，out-of-graph §3.6 判据 1）。
- **断言**：两类注入各自必红（判词点名）；干净对照（现状四文件原树）必绿——现状树本身必须过本守卫。
- **判据载体**：caps-gate 退出码＋判词输出＋台账锚集失配点。

**SL-4b（领班图外写口）**：

- **注入**：workflow 文本夹具注入领班席图外写口形态——lead 会话步产物落点出现在 `team/lead-plan-segments/` 登记面之外（如 lead 步直写 `team/status/<pid>.json` 或工作区任意路径）。
- **执法体**：caps-gate 文本断言层（`out-of-scope-write` 判词的 workflow 文本投影）＋包装器写预授权对平测试（session-config artifacts 面与门清单逐键一致，seat-gates §4.3）。
- **断言**：图外落点注入必红（判词点名）；干净对照必绿。
- **判据载体**：caps-gate 退出码＋判词输出。

### 2.5 SL-5 补卷守卫四条件违约矩阵（根治 1 倒影；对应 failure-specs §5 判据③）

- **注入**：对守卫四条件逐条构造违约 pack（4 变体）：①merged=false；②F-1 越界（pack 内有卡外文件）；③checks-exit.json 有非零 exit（红 checks）／marker 按内容红但 claims 绿（BLK-1 面违约）；④会话正常终止（exit-0＋outcome ok＋无 marker——control 形态）；另加组合违约（红 checks＋marker 内容红但缺 evidence 件=BLK-1 边界：marker problems 仅缺件不拒，守卫仍因③拒）。
- **执法体**：`scripts/team/worker_salvage.py` 守卫本体（fail-closed，`worker_salvage.py:13` docstring 四条件）。
- **断言**：①五变体全部**不补卷**（salvage 拒，pack 维持缺件）；②exit-0+ok 形态永不被翻案为 done（control 钉子，`tests/test_worker_salvage.py:293` 语义——补卷永不掩盖服从性失败）；③红 checks 工人永不被补成 done（NC-3）；④绿路对照：全条件满足的 pack=补卷成功且 manifest 标 salvaged_from_machine。
- **判据载体**：salvage 退出码＋pack 状态。
- **在树先例**：`tests/test_worker_salvage.py` 在树守卫正反例族（本样本对齐并扩组合违约变体）。

### 2.6 SL-6 板面翻板回归桩（对应 failure-specs §6 判据③；59 轮四问题③回归）

- **注入**：模拟「写板终态后板面漂移」输入——构造墙 closeout 切片（project_state_written=true＋终态枚举）＋板面读桩（返回 Status≠终态＝漂移态，模拟 Item closed 翻板后的板面，翻板实证三单 `docs/板面关单翻板-最小操作指引.md:12-14`）。
- **执法体**：v3.0 board_drift 对账步（F3 §2.1 图内再同步：PAT 读板回查→记 board_drift→重写板→仍漂移硬评论报警）。
- **断言**：①漂移态输入→board_drift 事件必产（对账步必红）；②重写板动作被调用（PAT 单点写终态一次）；③仍漂移→硬评论报警分支触发；④**零漂移对照**：板面读桩返回终态=零事件零重写（对账不误报）。
- **判据载体**：对账步退出态＋board_drift 事件字段＋墙 closeout 切片。
- **诚实边界**：本样本测的是**图内发现与纠正机制**（对真实板面零依赖、零写面——板面读全部桩化）；板侧翻板根因的禁绝（大哥板侧操作）不在 CI 可测面（结构盲区，failure-specs §8 第 3 条）——本样本不冒充「阻断翻板」，只证明「翻板必被发现必被纠正」。

### 2.7 SL-7 图外写口桩（写入口收口门；对应 failure-specs §2 lead 判据③、§6）

- **注入**：workflow 文本夹具注入四类图外写口形态：①生产 workflow 出现 PAT 前缀族字面（ghp_ 哑值）；②生产 workflow 出现 I8_LIVE_B 夹具分支残留；③verdict 系文件落点在白名单外路径（repo 树内）；④席位门清单外令牌展开位点（`${{ secrets.* }}` 位点≠台账锚集，out-of-graph §3.6 判据 1 形态）。
- **执法体**：caps-gate 文本断言层（生产 workflow 四文件正文扫描）＋verdict 合法落点白名单校验＋secrets 位点对账（orphan-secret-expansion 判词）。
- **断言**：四注入各自必红（判词点名）；干净对照（现状四文件原树）必绿——**现状树本身必须过本守卫**（守卫不冤枉现状，只对未来违约红）。
- **判据载体**：caps-gate 退出码＋判词输出。
- **在树先例**：图外件守卫负例指针（out-of-graph §2.2 守卫负例、§3.6 五判据）。

### 2.8 SL-8 缺席注入族（缺席即事件门；对应 failure-specs §7 判据①、§1 判据⑤、§3 判据③；59 轮四问题④回归；failure-specs §7 判据①引用的「缺席报警桩」＝本节 SL-8a）

四变体（缺席面 × 承载席）＋一变体（evidence manifest 面，INV-7 承载——本批补齐使 §1.4 表缺席行与 INV 清单对齐）：

| 变体 | 注入 | 执法体 | 断言 |
|---|---|---|---|
| SL-8a recorder 缺席 | 桩 validator 会话全程零 recorder 调用、零 partial 落盘 | 包装器采样器＋墙 recorder_call_count＋硬评论报警 | 告警事件必产（首步窗口与全程窗口各测）；告警含席位/窗口/缺席面字段；recorder_call_count=0 上墙 |
| SL-8b delta 缺席 | worker 会话死且零 delta 写出（fork-orphan 极端形态） | prep 门（prep_should_run 面按缺 delta 走缺件路径）＋缺席告警 | 缺件路径触发＋缺席事件上墙（delta 缺席≠会话 ok） |
| SL-8c verdict 封章缺席 | partial 存在但 final=false（未封章） | adopt 采认步（adoptable 判据，`salvage_verdict.py:45-47`） | 不采认＋round 重验路径触发＋缺席告警（窗口截止时 sealed 缺席） |
| SL-8d 收口 patch 缺席 | 桩链跑完但 final_status_card patch 未产 | foreman lint 静态面＋runtime 缺席告警（assemble 窗口） | lint 红（现状执法）＋v3.0 告警事件（补 per-run 面） |
| SL-8e evidence manifest 缺席 | prep 产出 evidence.tar.gz 而 manifest sha 字段缺席（INV-7 面——packs 树不齐或 sha 链断裂） | validate 入口 manifest sha 门（fail-closed 拒）＋缺席告警 | sha 门拒（现状执法）＋v3.0 告警事件（prep→validate 交接窗口内 manifest 缺席必有人知道） |

- **延迟采样**：缺席类=告警产出时延上界（§1.2 末段口径）。
- **判据载体**：告警事件对象（墙缺席面字段＋硬评论 mock 面断言）。

### 2.9 SL-9 交接接口违约族（枚举门；handoff-schemas §2.1/§3.1/§4.1/§5.1 违约表的常驻化）

> 实例级正/负断言已常驻 `tests/test_wall_v3_design_contract.py::TestHandoffSchemaInstances`（scrutiny round-1 BLK-1 修正：从本姊妹件提取四 schema 样本，把 W-1..W-6/V-1..V-6/P-1..P-4/H-1..H-3 表中可由 jsonschema 承载的行跑成正/负实例；构造权/悬挂引用/叙事判据类违约仍按本节登记，归施工面 caps-gate/解析器承载）。

- **注入**：四 schema 违约表全量注入（W-1..W-6 / V-1..V-6 / P-1..P-4 / H-1..H-3，共 19 变体——内存对象构造，零文件面）。
- **执法体**：四 schema jsonschema 校验（负对照与生产共用同一校验器实现，handoff-schemas §7.2 牙齿一致纪律）＋证据登记解析（悬挂引用）＋构造权校验（§6 白名单）。
- **断言**：19 变体全拒＋合法对照件（四 schema 各一合法样本）全绿。
- **判据载体**：校验器异常面逐条点名。
- **落位说明**：本族是 handoff-schemas 已设计违约表的验收线登记——**违约表定义归 handoff-schemas（F2 交付），本件只登记其常驻负例形态与判据载体**，不重复 schema 细节。

### 2.10 SL-10 caps-gate 判词负例族（工具/制品/事件/状态读面判词；caps-gate 十判词的 1/4/5/6 号）

> 注入面照既有文本层族（SL-4/SL-7）形制：workflow 文本夹具注入＋caps-gate 真跑（守卫在岗断言）＋判词点名红＋现状树干净对照绿。四样本与判词一一对应，判词枚举见 seat-gates §1.3 表。

- **SL-10a（`unregistered-tool-call`）**：
  - **注入**：workflow 文本夹具给某席位步新增门清单 `api`/`local_uses` 白名单外的会话工具调用面（例：worker 步注入 `gh api repos/.../issues --method POST` 写调用——worker 门清单工具面只有 prompt 单源/delta 写面，无 gh api）。
  - **执法体**：caps-gate 文本断言层（席位步调用面 × 门清单 api/local_uses 集合比对）。
  - **断言**：注入必红（判词点名：席位×工具未登记）；现状四文件原树同场跑=绿（守卫不冤枉现状）。
  - **判据载体**：caps-gate 退出码＋判词输出（席位/工具/调用行锚）。
- **SL-10b（`undeclared-artifact`）**：
  - **注入**：席位步新增登记 artifacts 面外产物落点（例：replan 步直写 `team/status/<pid>.json`——其 artifacts 登记面只有 team-plan-v2.json；或 worker 步产物落点含顶层 verdict 路径——件④白名单外形态复用）。
  - **执法体**：caps-gate 文本断言层（写面/上传面路径 × 该席 artifacts 登记集比对）。
  - **断言**：注入必红（判词点名：席位×制品路径未登记）；对照绿。
  - **判据载体**：caps-gate 退出码＋判词输出。
- **SL-10c（`undeclared-event`）**：
  - **注入**：席位步新增登记 events 名单外事件面（例：prep 步注入 issue close 调用——prep 门清单 events_produced 只有备料报告评论/墙 patch/git push，无关单权；validator 步注入 issue 评论调用——其 events_produced 只有墙 patch/files 面）。
  - **执法体**：caps-gate 文本断言层（issue/comment/close 调用面 × 该席 events 登记集比对）。
  - **断言**：注入必红（判词点名：席位×事件面未登记）；对照绿。
  - **判据载体**：caps-gate 退出码＋判词输出。
- **SL-10d（`undeclared-state-read`）**：
  - **注入**：席位步新增登记 state_reads 面外状态读取面（例：recorder 承载步注入跨席 packs 树读调用——recorder 门清单 state_reads=本会话中间态；assemble 步注入 worker 分支树读——其 state_reads 只有墙）。
  - **执法体**：caps-gate 文本断言层（读面路径 × 该席 state_reads 登记集比对）。
  - **断言**：注入必红（判词点名：席位×读面未登记）；对照绿。
  - **判据载体**：caps-gate 退出码＋判词输出。

### 2.11 SL-11 登记面升级闸族（schema 漂移/声明缺失/构造权越权；caps-gate 十判词的 7/9/10 号）

- **SL-11a（`evidence-construct-violation`）**：
  - **注入**：内存对象构造违约交接物——lead/worker/replan/assemble 席产物内含证据对象字段（构造权白名单四主体：机器守卫步/validator 会话经 recorder 工具/prep 补卷器/adopt 采认步之外，handoff-schemas §6）。
  - **执法体**：caps-gate 构造权校验（交接物 created_by × 构造权白名单比对）＋schema 侧构造权字段校验（verdict.v2 evidence 对象构造权标注）。
  - **断言**：越权构造必红（判词点名：席位非构造权主体）；validator 会话合法构造对照绿。
  - **判据载体**：caps-gate 退出码＋判词输出。
  - **与 SL-2 的分工**：SL-2 测「无证据出叙事」（validator 面叙事门），SL-11a 测「越权造证据」（构造权门）——两门两判词，样本分立。
- **SL-11b（`caps-schema-drift`）**：
  - **注入**：内存变异 foreman-caps 登记段——增删键（如删 `authorization` 键）/改词表（如判词枚举加新值）而不同批改契约测试（对位引擎要点 3 同批改锁形制，form-basis 要点 3 原物锚 `key-registry.toml:14-16` 铁律）。
  - **执法体**：caps-gate schema 校验器（键集/词表硬编码比对，负对照与生产共用同一实现）。
  - **断言**：漂移必红（exit 1＋判词点名：漂移键名/漂移词值）；合法登记对照绿。
  - **判据载体**：caps-gate 退出码＋漂移面点名。
- **SL-11c（`mixed-registry-change`）**：
  - **注入**：变更集文本夹具改 `foreman-caps.v1.toml` 门清单行（如改 lead 写目标路径）而不带 `wall-registry-change: true` 声明行。
  - **执法体**：caps-gate 升级闸判词（登记面变更×声明行检测，常量对位引擎 `check_module_wall.py:131` `REGISTRY_CHANGE_DECLARATION` 形制）。
  - **断言**：无声明变更必红（判词点名）；带声明行对照绿（声明通道畅通性正对照）。
  - **判据载体**：caps-gate 退出码＋判词输出。
  - **接线锁对位**：本样本的常驻载体本身接 foreman-wall-ci 恒跑（seat-gates §1.4 接线锁契约测试钉住）——对位引擎 NEW-2 闭合后形态（form-basis §11.1 更新口径）：判词存在且接线，两件事都有测试锁。

### 2.12 SL-12 钥匙面判词族（旁路面/钥匙升级闸；钥匙面五判词的 4/5 号——判词枚举 out-of-graph §3.6）

- **SL-12a（`unregistered-bypass-surface`）**：
  - **注入**：文本夹具新增旁路面而台账无登记——生产 workflow 新增直写 `~/.factory/settings.json` 的位点（件③收口后声明体单点之外的第二写位），或 verdict 白名单外落点且 `[[orphan]]` 表无对应行。
  - **执法体**：钥匙面守卫（旁路面清单 × 台账 `[[external_face]]`/`[[orphan]]`/`[[dangling_name]]` 三表比对）。
  - **断言**：未登记旁路必红（判词点名：旁路面锚）；已登记面（memory 树/runner 会话配置/探针 workflow 族——`[[external_face]]` 现有三条）对照绿。
  - **判据载体**：钥匙面守卫退出码＋判词输出。
- **SL-12b（`mixed-key-registry-change`）**：
  - **注入**：变更集文本夹具改台账文件（foreman-keys.toml 键行/词表行）或钥匙守卫本体而不带 `key-registry-change: true` 声明行。
  - **执法体**：钥匙面守卫升级闸判词（台账变更×声明行检测，升级闸常量对位引擎 `check_module_wall.py:131` 形制，out-of-graph §3.7）。
  - **断言**：无声明变更必红；带声明行对照绿。
  - **判据载体**：钥匙面守卫退出码＋判词输出。

**钥匙面五判词覆盖声明**：判词 1-3（`orphan-secret-expansion`/`anchor-drift`/`value-leak`）的必死样本=SL-7 第①/④注入（§2.7 既有设计，判据 1/2 的文本层）；判词 4-5=SL-12a/b（本节新增）——五判词逐条有样本，零「CLI-only 判词」类目（§0b 禁抄项义务：全部判词落 CI 恒跑腿）。

### 2.13 SL-13 席位 probe 必死样本族（seat-gates §2 五 probe 的专属载体；round-2 补齐——probe→SL 显式映射见 §1.4 第三张表）

> 五样本各对应 seat-gates §2 一个此前无样本的 probe 子句（lead 接线锁 / prep 候选分支越权 / validator D-2 封章粘滞 / assemble human_stop 消费 / assemble pick fail-closed 变体）。形制同既有族：确定性注入＋守卫在岗断言＋现状树干净对照绿，零网络零真树污染；目标态载体=`tests/test_wall_v3_design_contract.py`＋`tests/fixtures/wall-v3/`（F5 落树）。

- **SL-13a（lead 接线锁——门清单键缺失→包装器拒启）**：
  - **注入**：内存变异门清单（对位引擎要点 3 同批改锁的负对照形制）：①删 `[seat.lead]` 整段；②保留段但 budgets 键不齐（缺 `droid_wall_sec`）；③`entry` 键空数组。
  - **执法体**：包装器 caps load fail-loud 校验（seat-gates §2.1 probes 接线锁面：会话配置生成时读门清单，键缺失即拒启——exit 2，永不静默绿、永不禁用默认放行）。
  - **断言**：三变体全部拒启（退出码 2＋拒绝理由点名缺失键/段）；**零会话启动**（无 droid 进程被拉起、零哨兵、零产物落盘）；合法门清单对照=会话配置四节正常生成（红绿对照对全）。
  - **判据载体**：包装器退出码＋拒绝清单＋session-config.json 缺席证明。
- **SL-13b（prep 候选分支越权写——非 prep 席 push 候选分支→F 类守卫红）**：
  - **注入**：workflow 文本夹具注入非 prep 席位步的候选分支 push 形态（例：worker 会话步后新增 `git push origin team/issue-N/candidate-R` 行；lead 步同形态第二变体——候选分支 git-push 权只登记在 prep 门清单 artifacts 面，seat-gates §2.3）。
  - **执法体**：caps-gate 文本断言层（席位步 git push 面 × 门清单 artifacts `op=git-push` 登记集比对——`undeclared-artifact`/`out-of-scope-write` 判词）。
  - **断言**：两类注入各自必红（判词点名：席位×候选分支未登记）；现状树对照绿（现状仅 prep/pull 类步持候选分支 push）。
  - **判据载体**：caps-gate 退出码＋判词输出。
- **SL-13c（validator D-2 封章粘滞——verdict 半套→封章拒过）**：
  - **注入**：verdict 半套两变体：①`final=true` 章在而 judged[] 仅覆盖部分 judgeable 件（coverage 不齐）；②partial 文件在封章后被晚期写翻动（内容变更，模拟粘滞破坏者）。
  - **执法体**：adopt 采认步 D-2 面——adoptable 判据（`salvage_verdict.py:45-47`，final＋齐覆盖双条件）＋sealed 粘性（`salvage_verdict.py:93-94`：sealed 后晚期写不得翻封）。
  - **断言**：①半套不达 adoptable=adopt 拒采＋round 重验路径触发；②晚期写被粘性拒绝（文件内容维持 sealed 版）＋翻写尝试在案（审计面）。
  - **判据载体**：adopt 退出码＋重验标记＋sealed 版内容比对。
- **SL-13d（assemble human_stop 消费——human_stop 在墙→提前停分支必被消费）**：
  - **注入**：墙 closeout 切片注入 `human_stop` 事件（schema `:33` 面），收口步读桩返回正常 pick 语义（模拟现状缺口：human_stop 不被消费照常收口）。
  - **执法体**：v3.0 assemble 消费分支（seat-gates §2.6 probes human_stop 消费门：human_stop 在墙=提前停路径必须触发——跳过 pick/写板/关单，收口为停止态）。
  - **断言**：注入必红（收口步未消费 human_stop=判词红）；消费正对照：human_stop 在墙且提前停分支被走=零板面写零 PR 零关单＋停止态上墙。
  - **判据载体**：消费分支退出态＋板面/PR/关单零动作证明＋停止态墙字段。
- **SL-13e（assemble pick fail-closed 变体——validation 切片整片不可采认→pick 拒=全链零写）**：
  - **注入**：墙 validation 切片存在但整片 adoptable=false（全部 partial 未封章——缺切片正例已在树，本样本补「切片在场但全不可采」变体）。
  - **执法体**：`pick_verdict_from_wall` fail-closed（`team.yml:4420`——现有执法本体，负对照共用生产校验路径）。
  - **断言**：pick 拒＝零板面写、零 PR create、零关单（fail-closed 全链收口）；合法切片对照=正常 pick+写板（红绿对照对全）。
  - **判据载体**：pick 退出码＋板面/PR/关单零动作证明。
  - **在树先例**：pick fail-closed 在树契约面（assemble 测试族，NC-6 留痕 §二表）——本样本补变体与红绿对照，不重复既有断言。

---

## §3 执法延迟实测口径落位（每面执法墙的采样矩阵）

| 执法墙 | 预算面 | 采样源样本 | 设计上界（护栏） | CI 报告形态 |
|---|---|---|---|---|
| lead 会话墙 | droid_wall_sec=600（T0=会话预算到期；软超时=job_timeout−400=500s 基座面，job 15m——seat-gates §2.1 budgets） | SL-1 | 全样本 L ≤ 宽限(10s)＋SIGKILL 完成期(10s 采样护栏)=20s | `SL-1 enforcement-latency upper-bound=<n>s` |
| worker 会话墙（v3.0 包装器） | 900（T0=会话预算到期） | SL-3（fork-orphan 主采样） | 同上＋**孤儿整组收断言**（L 上界含 KILL 传播） | `SL-3 enforcement-latency upper-bound=<n>s（kill_path 逐采样）` |
| validator 会话墙 | 480＋adopt 储备 120（`foreman_run_lib.py:42-45`；软超时=job 15m−400=500s 外层哨兵线——seat-gates §2.4 budgets 注：480 是包装器第一道墙、500 是体外监督者外层哨兵线，双预算各守一层） | SL-3 同构参数化 | 同上 | 同形态报告 |
| replan 会话墙 | 480（`foreman_run_lib.py:48-50`） | SL-3 同构参数化 | 同上 | 同形态报告 |
| 缺席即事件告警面 | 窗口=budgets 键（§4） | SL-8a-e | 告警时延≤窗口宽限＋上墙余量 | `SL-8x alert-latency upper-bound=<n>s` |

**采样纪律**（§1.2 细则的落位）：每墙 N≥5（三抗死形态各≥1＋普通≥2）；取上界；逐采样行落 `wall-v3-latency.json`（目标态 artifact）；实测超护栏=该墙建成判据红（§1.3 第 2 条）。

**诚实声明**：延迟实测测量的是**包装器执法路径**（桩进程组），不是生产 droid 会话的真实死亡时延——生产会话的死亡面由墙 patch 上墙字段承载（session_outcome 三字段），两者是不同测量对象。设计上界护栏值对桩与生产同构成立的前提=执法通道与被管进程形态解耦（组信号整组收），这正是桩要证明的。

---

## §4 缺席即事件不变量检查设计（硬规则⑥落位）

### 4.1 不变量清单（逐席逐面）

| # | 不变量 | 观察点 | 窗口 | 缺席后果 |
|---|---|---|---|---|
| INV-1 | recorder 调用数>0（validator/worker 会话） | 包装器采样器（tool_call 计数） | 首步窗口=会话开始后首个分析单元；全程窗口=budgets.droid_wall_sec | 告警事件＋recorder_call_count=0 上墙＋硬评论 |
| INV-2 | verdict-partial 首步落盘（逐件纪律的机器面） | 落点存在性（PARTIAL_NAME，`salvage_verdict.py:18`） | 首步窗口 | 告警＋G-3 登记维度缺失标记 |
| INV-3 | sealed 封章在窗口内达成 | adoptable 判据（`:45-47`） | droid_wall_sec＋adopt_reserve_sec | 不采认＋round 重验＋告警 |
| INV-4 | worker-delta 每 pid 恰一条 | merge 面并集对账（`team.yml:885`） | workers-wall-merge 窗口 | 缺件路径＋缺席告警 |
| INV-5 | plan-v2 落单（should_replan=true 时） | 落单步产物存在性（`team.yml:2420-2423` 面） | replan budgets 窗口 | 告警＋链终态 failure |
| INV-6 | final_status_card patch | 墙 closeout 切片 | assemble 窗口 | lint 红＋v3.0 告警 |
| INV-7 | evidence.tar.gz manifest 齐 | validate manifest sha 门（锚件 2 §3 入口面） | prep→validate 交接窗口 | sha 门拒＋告警 |

### 4.2 不变量检查的执法形态

- **观察点实现**：全部不变量的观察点只有两类——包装器采样（会话面：INV-1/2）与墙/产物存在性读取（产物面：INV-3..7）；**零 prompt 依赖**（措辞类约束无运行时效力，P-2 终裁口径 `V-3-closeout-收档报告.md:56`——缺席执法不得建立在措辞上）。
- **窗口定义单一来源**：窗口值住席位门清单 `budgets` 键（seat-gates §2 各段），缺席检查器读门清单，不读 workflow 字面量（与预算同源纪律，seat-gates §4.2）。
- **缺席≠失败豁免**：缺席告警不改变链采认语义（inv 缺席的链该 fail 仍 fail——例如 INV-3 缺席=不采认）；告警是**可见性执法**（从无人知道变必有人知道），不是替代处置。59 轮四问题④的教训正是「缺席既无处置也无可见」——v3.0 先补可见性，处置面由守卫既有 fail-closed 承载。
- **告警必含定位字段**：席位/窗口名/缺席面/观测值——告警不可定位=告警无效（RS-4 断言面）。

---

## §5 59 轮四问题回归样本设计（RS 族；architecture §8 硬规则⑦落位）

> 四问题机制级证据底座＝锚件 2 §10（①replan 虚构死因/②900s 不执法/③板面翻板/④recorder 缺席）。RS 样本设计原则：**每样本先钉死当年的错误行为，再断言反转后的正确行为**——「钉子反转」不仅是 replan 文案一处，四问题各有一个「当年被钉错/没人钉」的面，RS 逐个反转。回归样本常驻全套件门，四问题任何一处回退即红。

### RS-1 replan 虚构死因钉子反转样本（四问题①）

- **当年错误行为的钉子**：`tests/test_replan_context_and_skipped_outcome_r53c.py:190-205`——断言「F-1 检查拒绝」文案**必须逐字出现**于 replan prompt（分支缺席即推断 F-1 拒绝，无机器佐证；机制锚 `team.yml:2259` 起推断注释、`:2278-2279` 文案赋值，锚件 2 §10-①）。
- **反转断言（三段，handoff-schemas §9.2 同批施工）**：
  1. **无证据不出文案**：分支缺席＋无 origin=f1 机器证据 → prompt 死因面呈现「未明（无机器证据）」，F-1 文案零出现（反转 :201-:202 逐字断言为 count==0 条件断言）。
  2. **有证据才出文案**：构造合法机器证据对象（origin=f1 的 machine_guard_record，F-1 拒绝事件发生时登记）→ prompt 含 F-1 文案且恰好一次（:205 count==1 断言保留但条件化——文案从「无条件推断」变「机器证实才可说」）。
  3. **schema 面**：worker-delta v2/plan-v2 的 cause 枚举校验＋f1_rejected_machine_confirmed 构造权校验（SL-3b' 断言面复用）。
- **归责面对位**：attribution_reason 分支（`attribution_reason.py:75` neutral_attribution）按 delta cause 枚举渲染——wall_kill↔中性归因措辞、self_crash↔非机器判定措辞、unknown↔缺料措辞（归责措辞与死亡事实对齐，根治第 4 层语义，`docs/第58轮-D单追认口径与replan归责缺陷立号.md:32` 表）。
- **验收判据**：反转后三段断言全绿＋旧钉子测试不存在（同批删除/改造，不双轨）。

### RS-2 900s 不执法反转样本（四问题②）

- **当年错误行为**：执法与会话同体——裸跑 `timeout ... 900s droid exec`（`team.yml:599`；worker2 `:2784`），孤儿子进程持管道使 step 拖到 25m job 墙（45B 实测：名义 900s、实际 1800s，锚件 2 §10-②）；budgets lint 明文豁免该形态（`lint_workflow_budgets.py:43-51` worker/900s 豁免分支）。
- **反转断言**：
  1. **形态反转**：caps-gate BARE_DROID 探针——workflow 文本出现裸跑形态即红（豁免废止后对 7 席一律红，seat-gates §4.2 lint 同步反转）。
  2. **执法反转**：SL-3 fork-orphan 桩对 v3.0 包装器——进程组整组收（孤儿不存活）＋延迟上界数字（§3 采样矩阵）；同一注入对裸跑形态的失败剖面已由 45B 实证登记（证据锚：任务书口径，机制证据=锚件 2 §10-②），本样本不重建裸跑对照（不施工旧形态），以 SL-3 正解面收口。
  3. **预算反转**：预算从门清单读的接线断言——workflow 文本零 `900s` 字面量（BARE_DROID 正则同面）＋包装器读 `[seat.worker.budgets]` 的对平测试（session-config 与门清单逐键一致，seat-gates §4.3）。
- **验收判据**：三段断言绿＋SL-3 延迟上界≤护栏（§3 行 2）。
- **第 3 层边界**（不可施工面引用，failure-specs §0.4）：回合级熔断不在本仓施工——本样本的反转上限=会话级体外整组终止＋补卷回收；「回合预算/收束/续作」三能力为上游立项前置（登记件 :19-:24），任何把本样本解读为回合级执法承诺的表述即违反登记口径。

### RS-3 板面翻板回归样本（四问题③）

- **当年错误行为**：PAT 写板「已验收」→人工关单→1–2 秒 Status 被翻回「施工中」，演员 `github-project-automation`（三单实测 #761/#763/#764，`docs/板面关单翻板-最小操作指引.md:12-14`）；repo 侧零可拦截写入点（`:24` 结论）。
- **反转断言**：
  1. **发现面**：SL-6 漂移注入→board_drift 事件必产＋重写必发生＋仍漂移硬评论必报（§2.6）。
  2. **板侧禁绝判据**（人工面，CI 不可测，登记判定）：板侧 Disable/终态选项改造完成后的 timeline 判据（专档 :37）——下一单关单后 1–2 分钟查 timeline 零 `github-project-automation` 翻板事件；env-check 探测项 WARN 登记面在树（F3 §2.1 第 2 步）。
  3. **repo 侧写点收口**：板面写 PAT 单点断言（caps-gate：板面写非 project_state_write 单点=token-scope-violation 红，seat-gates §2.6 probes）。
- **验收判据**：1 段常驻绿；2 段按三态纪律登记（板侧动作=blocked 待大哥，F3 §4 表①——**不虚称 cleared**）；3 段常驻绿。
- **诚实边界**：repo 内机制是发现与纠正不是阻断（结构盲区，failure-specs §8 第 3 条）；「关单即终态」的完全解在板侧，呈裁清单随主设计稿（out-of-graph §2.1 选项 A/B）。

### RS-4 recorder 缺席报警回归样本（四问题④）

- **当年错误行为**：必落字段与约定首步静默缺席无人知晓——生产首验 4 会话中 2 个调用 recorder、逐件落盘服从率 0/4、墙杀场景回收 0/2（`docs/V-3-closeout-收档报告.md:11` Opus 终审引文）；工人席对应口径：13 次工具调用零次以 handoffs/status 为目标（`docs/第58轮-死亡账分型登记-58D归第1类.md`；机制链 `worker_salvage.py:4-9` docstring）；per-run 无 recorder 调用数墙字段、无报警（锚件 2 §10-④）。
- **反转断言**：
  1. **缺席必报警**：SL-8a 桩零调用→告警必产＋recorder_call_count=0 上墙（§2.8）。
  2. **正样本门**（G-2 制度，`V-3-closeout-收档报告.md:15`——「让模型调用某工具才生效」的机制上线前必须有真实会话流 tool_call 正样本）：recorder 执法机制上线判据=受控会话正样本在案（V-3 门重跑面，发版前置人工门保留）＋离线重放只算回收链测试（本 RS 样本属机器面，不冒充正样本门）。
  3. **死亡账登记维度**（G-3，`:44`）：validator 墙杀必记「结论是否已形成/recorder 调用数/删失尾秒数」——墙 validation 切片扩字段断言（施工随 schema 演进同批）。
- **验收判据**：1、3 段常驻绿；2 段按 G-2 门登记（人工门状态显式，不虚称常驻自动化）。
- **措辞边界**（P-2 终裁，`:56`）：措辞类约束无运行时效力——本 RS 的执法面是采样与告警（§4.2 零 prompt 依赖），prompt 单源增量落盘引导（根治第 2 层）只作边际压制、不入判据。

### RS 族与 SL 族互锁

| RS | 依赖的 SL 面 | 互锁断言 |
|---|---|---|
| RS-1 | SL-3b'（枚举/构造权/悬挂引用） | 钉子反转三段＋SL-3b' 四断言同批绿 |
| RS-2 | SL-3（恒挂＋孤儿）＋SL-7（裸跑形态探针） | 整组收＋延迟上界＋零裸跑字面量 |
| RS-3 | SL-6（翻板桩）＋SL-7（PAT 单点探针） | board_drift 必产＋单点违例必红 |
| RS-4 | SL-8a-c（缺席族） | 告警必产＋字段可定位＋墙字段在 |

---

## §6 验收线总表（墙/门 × 必死样本 × 延迟口径 × 缺席不变量 × 回归样本）

| 墙/门 | 必死样本 | 延迟口径 | 缺席不变量 | 回归样本 | 常驻载体 |
|---|---|---|---|---|---|
| lead 会话墙 | SL-1 | §3 行 1 | — | — | v3.0 契约测试（F5） |
| worker 会话墙＋体外执法 | SL-3 | §3 行 2（主采样源） | INV-4 | RS-2 | 在树守卫族＋v3.0 契约测试 |
| 写目标门（F-1 判词化） | SL-3b | —（静态守卫无时间面） | — | RS-1（结局面） | 在树 F-1 族＋caps-gate |
| 证据授权门 | SL-2、SL-3b'、SL-11a | — | INV-2/3 | RS-1 | v3.0 契约测试＋在树 salvage 族 |
| 补卷守卫 | SL-5 | — | INV-4 关联 | RS-2/RS-4 关联 | 在树 `tests/test_worker_salvage.py` |
| 板面终态门 | SL-6、SL-7 | — | — | RS-3 | v3.0 契约测试 |
| 令牌 scope 门 | SL-4 族（越权令牌注入，SL-7 载体同面） | — | — | — | caps-gate |
| 交接口枚举门 | SL-9（19 变体） | — | — | RS-1 | v3.0 契约测试 |
| 缺席即事件门 | SL-8a-e | §3 末行（告警时延） | INV-1..7 | RS-4 | v3.0 契约测试 |
| lead 图外写口 | SL-4b | — | INV-6 关联 | — | caps-gate 文本层 |
| caps-gate 判词负例门（工具/制品/事件/状态读） | SL-10a/b/c/d | — | — | — | caps-gate 文本层 |
| 登记面升级闸门（schema 漂移/声明缺失） | SL-11b/c | — | — | — | caps-gate（恒跑接线，§1.4 锁） |
| 钥匙面升级闸与旁路面 | SL-12a/b、SL-7 第①④注入 | — | — | — | 钥匙面守卫（恒跑） |
| 席位 probe 专属门（lead 接线锁／prep 候选分支越权／validator D-2 封章粘滞／assemble human_stop 消费＋pick 变体） | SL-13a-e（probe→SL 逐条映射见 §1.4 第三张表） | —（消费类无时间面） | INV-3 关联（SL-13c 封章缺席面） | — | 包装器 caps load＋caps-gate＋adopt/pick 在树执法本体 |

**门口径声明**：本表「墙/门」覆盖硬规则①③④⑤⑥⑦②的执法面；规则⑧（失败规范）载体=failure-specs 底稿本件不重复；规则⑨（钥匙）面 SL 样本=SL-7 第④注入（secrets 位点对账）＋SL-12a/b（旁路面/升级闸），延迟/缺席不适用；规则⑩（无兜底）面 SL-7 全部注入＋SL-11c＋RS-3 板侧三态登记。十条硬规则与验收线的逐条对位随主设计稿总装（architecture §8 映射表为准绳）；判词×样本满映射表（§1.4 第二张表）是「每判词至少一条必死样本」的机器可查索引；席位 probe→SL 显式映射表（§1.4 第三张表）是「每 probe 至少一条专属或点名样本」的机器可查索引（毯式句废止，round-2 纪律）。

---

## 附A 本件 file:line 锚清单（供锚解析器）

| 锚 | 解析判据（该行应含） | 来源 |
|---|---|---|
| `team.yml:599` | `900s`（裸跑行） | 转引 seat-gates 附A |
| `team.yml:731` | `reset --soft` | 转引 |
| `team.yml:885` | `merge_worker_deltas` | 转引 |
| `team.yml:1223` | `worker_salvage`（接线区段起） | 转引 |
| `team.yml:2420` | 落单步机器校验区段起 | 转引 handoff-schemas 附表 |
| `team.yml:2784` | `900s`（worker2 裸跑） | 转引 |
| `scripts/team/foreman_run_lib.py:38` | `"droid_wall_sec": 600`（lead） | ★ |
| `scripts/team/foreman_run_lib.py:42` | `"validator": {` | 转引 failure-specs 附A |
| `scripts/team/foreman_run_lib.py:48` | `"replan": {` | 转引 failure-specs 附A |
| `scripts/team/worker_salvage.py:13` | `The guard is machine-judged and fail-closed` | 转引 |
| `scripts/team/worker_salvage.py:5` | 死亡链机器侧重建 docstring（hslconv 案；docstring 自 :5 起，:4 为空行） | ★ |
| `scripts/team/salvage_verdict.py:18` | `PARTIAL_NAME` | 转引 |
| `scripts/team/salvage_verdict.py:45` | `final` is the D-2 seal 语义行 | 转引 failure-specs 附A（本件快照核实） |
| `scripts/team/salvage_verdict.py:47` | adoptable 语义行 | 转引 failure-specs 附A |
| `scripts/team/write_worker_delta.py:45` | `def classify_session_outcome` | 转引 |
| `scripts/team/attribution_reason.py:75` | `def neutral_attribution` | 转引 failure-specs 附A |
| `scripts/team/validator_prompt_template.py:97` | `HARD RULE — a red mandated check is never a pass` | 转引 failure-specs 附A |
| `scripts/team/lint_workflow_budgets.py:43` | worker/900s 豁免分支 | 转引 failure-specs 附A |
| `scripts/team/worker_prompt_template.py:13` | `Incremental persistence guidance` | 转引 failure-specs 附A |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:190` | 钉子测试定义 | 转引 failure-specs 附A |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:201` | F-1 文案逐字行起（跨 :201-:202——:201 分支缺席行、:202 F-1 拒绝括注行；:198-:200 为桩调用与循环行） | 转引 failure-specs 附A |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:205` | `prompt.count(line) == 1` | 转引 failure-specs 附A |
| `tests/test_worker_salvage.py:293` | exit-0+ok 墙不被补卷翻案守卫负例 | ★ |
| `tests/fixtures/worker-r58d/worker-delta-wall-killed.json` | 墙杀夹具文件存在性 | ★ |
| `docs/回合熔断上游特性需求登记-droidCLI.md:19` | 上游三能力表 | 转引 failure-specs 附A |
| `docs/R58D-收尾决策留痕-NC6与遗留决策点.md:5` | 十文件子集维持现状裁定 | 转引 failure-specs 附A |
| `docs/V-3-closeout-收档报告.md:11` | 服从率 0/4 终审引文 | 转引 failure-specs 附A |
| `docs/V-3-closeout-收档报告.md:15` | G-2 触发面正样本上线门 | 转引 failure-specs 附A |
| `docs/V-3-closeout-收档报告.md:44` | G-3 登记维度＋L-3 | 转引 failure-specs 附A |
| `docs/V-3-closeout-收档报告.md:56` | P-2 措辞无运行时效力终裁行 | ★ |
| `docs/第58轮-死亡账分型登记-58D归第1类.md:21` | hslconv 死法行 | 转引 failure-specs 附A |
| `docs/第58轮-D单追认口径与replan归责缺陷立号.md:32` | 归责模板分支化表行 | 转引 failure-specs 附A |
| `docs/板面关单翻板-最小操作指引.md:12` | 三单实测表 | 转引 out-of-graph 附A |
| `docs/板面关单翻板-最小操作指引.md:24` | repo 不可拦截结论 | 转引 failure-specs 附A |
| `docs/板面关单翻板-最小操作指引.md:37` | timeline 验证判据 | 转引 out-of-graph 附A |
| 引擎：`src/infra_core/engine/droid_review/run_lead.sh:55` | LEAD_KILL_GRACE_SEC 默认值 | 转引 form-basis 附表（:52-:55 区段） |
| 引擎：`src/infra_core/engine/droid_review/run_lead.sh:9` | 哨兵先行终止序列头注 | 转引 form-basis 附表 |
| 引擎：`src/infra_core/engine/droid_review/run_lead.sh:282` | `kill -TERM "-$exec_pid"` | 转引 form-basis 附表 |
| 引擎：`src/infra_core/engine/droid_review/run_lead.sh:286` | `kill -KILL` | 转引 form-basis 附表 |
| 引擎：`tests/test_lead_engine.py:1041` | TestRunLeadBoundedExitE2E 类定义 | 转引 form-basis 附表 |
| 引擎：`tests/test_lead_engine.py:1044` | hang→soft_timeout 遗书断言 | 转引 form-basis 附表 |
| 引擎：`tests/test_lead_engine.py:794` | fake droid 桩 mode="hang" 分支 | 转引 form-basis 附表 |

## 附B 十条硬规则 × 验收线索引（主设计稿 §6→§8 对位的底稿侧映射）

| 硬规则 | 验收线承载 |
|---|---|
| ①逐席位门清单＋工人收进包装器 | SL-3＋RS-2（裸跑形态反转＋包装器接线对平） |
| ②交接物全结构化＋证据引用 | SL-9＋SL-2/SL-3b'（枚举/证据/构造权全量负例） |
| ③执法在体外 | SL-1/SL-3（进程组整组收断言＝体外性的行为证明） |
| ④每墙必死样本＋执法延迟实测 | 全 SL 族＋§1.3 四条活验数字判据＋§3 采样矩阵 |
| ⑤写入口收口 | SL-3b/SL-4b/SL-7（越界写＋图外写口必红） |
| ⑥缺席即事件 | SL-8 族＋INV-1..7 |
| ⑦事故样本回归＋V-3 口径正样本门 | RS-1..4＋G-2 门登记（RS-4 第 2 段） |
| ⑧逐席位失败规范 | failure-specs 底稿（本件附B 反向索引互锁） |
| ⑨钥匙总管理 | SL-7 第④注入（secrets 位点对账）＋out-of-graph §3.6 五判据 |
| ⑩无兜底、不留图外 | SL-7 全注入＋RS-3 板侧三态登记（blocked 不虚称 cleared） |
