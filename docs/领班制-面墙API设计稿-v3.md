# 领班制－面墙 API 设计稿 v3.0

> **版本**：v3.0（2026-11-27 总装）。**前身**：v2.7 蓝图（`docs/领班制-整面API墙方案.md`）。
> **性质**：设计稿，零施工——本文只定义目标态与验收判据，不改任何 workflow/scripts/schemas/既有测试。施工另立 mission，批后另行。
> **真源**：引擎形制锚件 `docs/wall-v3/form-basis.md`（**引擎锚以 infraro-core main@460922c 为基准**，2026-11-28 实读复验）；现状行号锚件 `docs/wall-v3/as-is-capability-inventory.md`（R58-D 收尾态基线 564ce30 快照，2026-11-27）；三件套底稿 `docs/wall-v3/seat-gates.md`、`docs/wall-v3/out-of-graph-artifacts.md`、`docs/wall-v3/failure-specs.md`＋`docs/wall-v3/acceptance-line-map.md`＋`docs/wall-v3/handoff-schemas.md`。
> **锚纪律**：本稿引用的每个 file:line 锚经实读核实（文件在、行号不越界、锚定内容含预期关键词），机器可解析断言见 `tests/test_wall_v3_design_contract.py`。行号随树演化漂移时以实读为准；**引擎仓为只读参照，其锚一律以 main 当前树实读为准（验证时先比对 `git -C <引擎仓> diff <写作时点 rev> main -- <被锚文件>`），引擎侧锚点漂移不得被「测试子串仍命中」掩盖**（round-1 实证：`ci.yml:425` 的判据前缀在引擎改写后存活而被引内容已变）。
> **零密钥值铁律**：全文只记 secret 名与元数据，任何字段禁止出现密钥值本体（照引擎 M2 口径 `docs/specs/key-registry.toml:11` 引擎仓）。I8-B 夹具位点只锚变量名，不转录值。

---

## §0 版本口径声明

1. **本稿 v3.0 起版**，是「领班面墙 API」的唯一权威设计口径。
2. **作废 v2.7~v2.10 的账面墙口径**。作废对象（账面墙指认）：v2.7 蓝图起「整面 API 墙」挂名（`team.yml:7` 版本注记原文 v2.7.0）后，README 交付段先后标 v2.9（验收协议根治）与 v2.10（工人席落盘根治）——版本口径三处漂移（锚件 2 §0/§9 第 3 条）。挂名的「API 面墙」实际是**产物与采认语义墙**：ForemanRun 墙只记结局不记授权（`schemas/foreman-run.v1.schema.json:146-157` by-pid 三映射，零能力面字段），59 轮四问题（虚构死因/900s 不执法/板面图外写口/纪律缺席无报警）全部落在该判据集之外（锚件 2 §9 第 2 条）——**纸面有门、执法缺位**，故账面口径整体作废，能力授权面自本稿 v3.0 重立。
3. v2.7 蓝图中被本稿继承的件（ForemanRun 墙、采认链、env-check 门、五 lint 面）不因作废口径失效，其现状锚与目标态门清单在 §2 逐条对位；v2.8/v2.9/v2.10 三段根治成果（分段装配、I-5/I-6、根治 1+2+4）按其现状锚并入 §5/§6，不再以版本号挂墙。

## §0b 引擎未闭合项禁抄声明

**引擎锚版本口径**：本稿（含全部锚件）引用引擎仓形制与事实一律以 **infraro-core main@460922c（2026-11-28 00:33 +0800，PR #883）为权威基准**，全部引擎锚按该树实读复验（引擎仓只读，验证方法＝锚判据逐条实读比对；写作后引擎 main 再演化时按锚纪律头部条款重比对，不凭测试子串存活下结论）。引擎墙（hdot123/infraro-core）登记过的未闭合缺口项处置如下——**已闭合的缺口不是禁抄项，是形制演进的实例**；**上游已闭合的缺口更不允许领班侧复刻纸面门形态**：引擎把墙修到真执法的过程恰恰证明「判词存在但不接 CI」的形态撑不过对抗验证，领班侧任何门从第一天就按「须执法、禁纸面」设计。

| 项 | 引擎当前事实锚（main@460922c 实读） | 本稿对应面的执法设计（非纸面门） |
|---|---|---|
| VAL-M4-004 之 NEW-1：governance owner 门停用（登记时点态，`evidence/step5-api-unification/closeout/01-closeout-pack.md:94`「显式未闭合（CI 执法面）」） | 历史档口径；U-4 已把登记面纳入保护面（`src/infra_core/governance.py:26` DEFAULT_PROTECTED_PATTERNS 七模式，含 `docs/specs/**`＋`.github/workflows/**`＋守卫本体）；workflow 页面门态属引擎运营变量，本稿不引其为形制 | 领班域登记面（`foreman-caps.v1.toml`＋守卫本体＋CI 守卫段）的升级闸判词 `mixed-registry-change` **必须接 foreman-wall-ci 恒跑**（§1.4 接线锁），接线语义由契约测试锁住（对位引擎接线锁形制，引擎仓 `tests/test_module_wall_ci_wiring.py`）——「守卫判词存在但不接 CI」的形态在领班域按禁抄项处理 |
| VAL-M4-007／NEW-2：`--changes` 专属判词（rename 改界、mixed-registry-change）不接 CI——**登记时点态，已上游闭合** | 引擎 main@460922c 已接线：`.github/workflows/ci.yml:439-458`「Module wall changeset guard (PR only)」步实跑 `check_module_wall.py --changes`（`:458`），声明通道在场（`:454-456` PR body `wall-registry-change: true` 注释行注入），接线语义由引擎接线锁测试钉住（`tests/test_module_wall_ci_wiring.py:99` `test_changes_guard_step_wired_pr_only`）；`ci.yml:425-427` 注释现文「已接线 PR 腿 changeset 步」。当年「本流水线未接线」注释（写作时点 09a82fb 前的旧文）已不存在 | 本稿全部判词（§2.0 十判词＋§3.6 钥匙面五判词）施工时一律落 CI 恒跑腿（形态对位引擎闭合后的两步面：恒跑步＋事件语境步各按其判据执行），无「CLI-only 判词」类目；任何判词不落 CI 即显式未闭合，不冒充已执法。**禁抄原则保留并改述**：上游用一次真接线闭合了此缺口——领班侧更不允许复刻任何「纸面有门、执法缺位」形态，包括引用引擎历史缺口文本冒充「引擎也这样」 |
| R-29 两门口径演化史（契约三门 vs 实执法两门） | 引擎仓 `evidence/step5-api-unification/closeout/05-risk-register.md:70` | 本稿引用引擎放行门口径一律按 R-29 已裁**两门**（quality-gate / substrate-gate-suite，droid-review 已退；PR #870 收口）；领班面墙自身门数按其守卫面独立裁定（§1.5），不受两门/三门演化牵连，**任何挂名未执法的门都按本节禁抄项处理** |

## §0c 换入总纲与全文导读

**终局形态**：领班是候选模块，引擎层（hdot123/infraro-core）现有开发模块 M-CAP 占编排槽位；领班测过后**整模块换入**替换之。换入三判据（§7 详）：门清单不变、旧封印测试整套全过、失败规范对位。本文内「§1.4 接线锁／§1.5 放行门单源」指领班侧形制条款，承载与逐键形制细节见底稿 `docs/wall-v3/seat-gates.md` §1（该件 §1.4＝CI 恒跑接线锁、§1.5＝ruleset 单源、§3.5＝缺门补齐汇总）；「§3.6 钥匙面五判词」指钥匙台账对账判据节，承载见底稿 `docs/wall-v3/out-of-graph-artifacts.md` §3.6。

**十章结构**（三件套落位）：

| 章 | 内容 | 对应交付件 |
|---|---|---|
| §0/§0b/§0c | 版本口径、禁抄声明、换入总纲 | 本文 |
| §1 | 总纲与硬规则落位映射 | 本文＋form-basis |
| §2 | 逐席位门清单＋对位表＋交接物 schema（三件套之一） | seat-gates＋handoff-schemas |
| §3 | 写入口收口、图外件清零清单、钥匙总管理（三件套之二） | out-of-graph-artifacts |
| §4 | 执法设计（体外执法） | 本文＋form-basis §10 |
| §5 | 逐席位失败规范、缺席即事件、结构盲区（三件套之三·判据侧） | failure-specs |
| §6 | 逐条规则验收线（三件套之三·验收侧） | acceptance-line-map |
| §7 | 换入判据 | 本文 |
| §8 | 待大哥裁决清单 | 本文 |
| 附A | 锚清单 | 本文＋fixture |

---

## §1 总纲与硬规则

### 1.1 default-deny 总纲

**领班制每个席位的能力以门清单登记为全集，清单之外不存在。** 三条推论一次定死：

1. **登记即全集**：席位能做的每件事（入口、工具、写目标、事件、读面、令牌）都必须出现在其门清单段内；未登记＝违约（守卫判词 §2.0），不存在「合理默认放行」。
2. **多出的能力默认删**：现状存在而门清单不登记的能力（图外写口、全树读、假 PAT 夹具），处置=默认删；要保留逐条单独呈大哥裁（§2.4 总表、§8 清单）。
3. **无兜底**：任何门没有「兜底通道」——体外执法失败不是回退到信任会话的理由，是墙建成失败（§6.1 四条活验数字判据）。图外件清零后的世界没有图外旁路（§3）。

### 1.2 形制基准十要点（照抄清单，引擎仓原物锚）

领班面墙形制照抄引擎 M-CAP 模块墙十要点（全锚经实读核实，详 `form-basis.md`）：

| # | 要点 | 引擎原物锚（引擎仓相对路径） |
|---|---|---|
| 1 | 双 TOML 登记真源＋守卫零硬编码（fail-loud exit 2） | `docs/specs/modules.toml:19`、`docs/specs/module-capabilities.toml:77`、`scripts/check_module_wall.py:12` |
| 2 | 每模块一段门清单，字段固定（十键＋v5 三锚） | `docs/specs/module-capabilities.toml:574`（M-CAP 段起） |
| 3 | schema 一次定死＋同批改锁 | `docs/specs/key-registry.toml:14`（铁律原文） |
| 4 | 判词只增不改＋退出码三态（0/1/2） | `scripts/check_module_wall.py:90`（RULE_UNREGISTERED 起） |
| 5 | CI 恒跑接线锁（零 if、零 continue-on-error、两腿同面） | `.github/workflows/ci.yml:428-429`（Module wall guard 恒跑步）＋`:439-458`（Module wall changeset guard PR-only 步——`--changes` 判词已接线，PR-only 条件门是事件语境本身而非软出口，接线锁测试 `tests/test_module_wall_ci_wiring.py:99` 钉住） |
| 6 | 放行门单源 ruleset，不在代码养第二套标准 | `scripts/board_sync_parse.py:97`（单源声明原文） |
| 7 | 登记面升级闸＋governance 受保护路径 | `scripts/check_module_wall.py:131`（声明常量）、`src/infra_core/governance.py:26` |
| 8 | 封印＝sha256 指纹快照＋--verify 对平（确定性） | `scripts/hardening_baseline.py:1`（工具头注）、`:303`（对平 docstring） |
| 9 | 钥匙零值登记＋三态词表（use/cap_change；active/dormant/zombie/revoked） | `docs/specs/key-registry.toml:25`（词表）、`:38`（schema_version） |
| 10 | 失败规范＝点位普查表（触发面/handler/三态定级/缺口/机器判据） | `docs/guides/exception-point-inventory.md:23`（18 点清单）、`:27`（表头） |

**禁抄项**＝§0b 三行（VAL-M4-004/007 未闭合态、R-29 演化史），对应面已改为真实执法设计。

### 1.3 十条硬规则逐条落位映射

十条硬规则全部入稿，每条有唯一落位章节＋必死样本对位（样本族定义 §6）：

| # | 硬规则 | 落位章节 | 验收线必死样本 |
|---|---|---|---|
| ① | 逐席位门清单＋工人席收进包装器 | §2（七席门清单＋§2.5 包装器） | SL-3 恒挂＋孤儿桩；SL-10 缺登记面族（a-d）；SL-11b schema 漂移；RS-2 裸跑形态反转 |
| ② | 交接物全结构化＋因果结论枚举化＋证据引用强制 | §2.6（四 schema＋构造权单源） | SL-9 枚举违约族（19 变体）；SL-2/SL-3b' 伪造叙事桩；SL-11a 构造权越权 |
| ③ | 执法在体外 | §4（监督者＋进程组终止序列） | SL-1/SL-3 进程组整组收断言 |
| ④ | 每墙配必死样本＋执法延迟实测 | §6.2（延迟口径）＋§6.1（活验四数字） | SL-1..SL-12 全族；延迟上界 CI 出实测数 |
| ⑤ | 写入口收口（状态机单入口） | §3.1（写入口面）＋§2.2 各席 artifacts | SL-3b/SL-4b/SL-7 图外写口桩；SL-10b 未登记制品路径 |
| ⑥ | 缺席即事件 | §5.2（INV-1..7 不变量） | SL-8 缺席注入族（a-e）；RS-4 recorder 缺席报警 |
| ⑦ | 事故样本回归＋V-3 口径正样本门 | §6.3（RS-1..4 回归样本） | RS 族四样本；G-2 门登记 |
| ⑧ | 逐席位失败规范（并入已批根治 1+2+4） | §5.1（七席规范） | SL-5 补卷守卫倒影矩阵 |
| ⑨ | 钥匙总管理（引擎 M2 口径） | §3.4（foreman-keys 台账） | SL-7 第④注入（secrets 位点对账）；SL-12 钥匙面判词族（a/b） |
| ⑩ | 无兜底、不留图外 | §3（图外件清零）＋§1.1 推论 3 | SL-7 全注入；SL-11c 登记面变更无声明；RS-3 板侧三态登记 |

落位自洽性：每条规则唯一落位，规则间无冲突——①是授权面总纲，②是交接面，③④是执法面，⑤⑥⑩是边界面，⑦⑧是回归与失败面，⑨是凭证面；验收线（§6）对十条的承载见 §6.4 总表。

## §2 逐席位门清单与对位表（三件套之一）

### 2.0 形制与登记真源

**双登记真源**（照引擎要点 1）：授权面登记 `foreman-caps.v1.toml`（目标态，施工落 repo 根）——席位能做什么；结局面登记 `schemas/foreman-run.v1.schema.json`（现状在树）——席位做了什么。ForemanRun 墙字段（`session_outcome_by_pid` 三映射 `:146-157`、`human_stop` `:33`、`budget_slice` `:59`、`closeout_slice` `:210-215`）与门清单分离，一个记结局一个记授权，互不越界。

**键集一次定死**（照引擎要点 2＋3，M-CAP 段原物 `module-capabilities.toml:574` 起）：每席一段 `[seat.<id>]`，键集＝引擎 **12 键**（MODULE_KEYS 实测：entry/api/guard_test/events_consumed/events_produced/artifacts/state_reads/local_uses/probes/callers/authorization/verification，`tests/test_module_capabilities_contract.py:55-68`）＋领班域扩展一键 `budgets`；别名声明保留（「十键＋三锚」「协作五键＋v5 三键」皆指此 12 键集）：

```
entry / api / guard_test / events_consumed / events_produced / artifacts /
state_reads / local_uses / probes / callers / authorization / verification / budgets
```

`budgets` 是唯一域扩展键（承载会话墙/job 墙预算，预算唯一来源，§2.5 接线）；增删键必须同批改契约测试 `tests/test_foreman_caps_contract.py`（目标态新增），禁止守卫或登记单边漂移（铁律原文对位 `key-registry.toml:14` 引擎仓）。

**caps-gate 守卫判词枚举**（初版一次定死，只增不改；对位引擎判词纪律 `check_module_wall.py:90` 起）：

| 判词 | 语义 |
|---|---|
| `unregistered-tool-call` | 会话调用门清单外工具 |
| `out-of-scope-write` | 写目标越 artifacts 登记面 |
| `token-scope-violation` | 使用 authorization.token_scope 外令牌/权限 |
| `undeclared-artifact` | 产出未登记制品 |
| `undeclared-event` | 消费/产出未登记事件 |
| `undeclared-state-read` | 读门清单外状态树 |
| `narrative-without-evidence` | 因果结论无证据对象佐证 |
| `evidence-construct-violation` | 非核查环节构造证据对象 |
| `caps-schema-drift` | 门清单 schema 键集/词表漂移且未同批改契约测试 |
| `mixed-registry-change` | 改登记面未带 `wall-registry-change: true` 声明 |

退出码三态：0 clean / 1 violations / 2 环境错误（fail-loud 永不静默绿，对位 `check_module_wall.py:12-14` 引擎仓）。

### 2.1 席位名单与二轮镜像口径

**7 席**：领班 lead、工人 worker、验收 validator、改计划 replan、备料 prep、装配 assemble、写板 recorder。

- **写板席（recorder）**是目标态独立席：现状无独立 job，职能由两处承载——validator prompt 纪律（`team.yml:1515` build_validator_prompt 单源）＋prep 补卷器机器兜底（`team.yml:1223-1226` worker_salvage 接线区段）。立席=对「纪律缺席无报警」（四问题④）的结构化收编（§5.1 §7）。
- **二轮镜像**：worker2（`team.yml:2697`）/ prep2（`:3107`）/ validate2（`:3618`）/ revalidate2（`:4010`）为一轮对应席镜像，**门清单按一轮对应席同构适用**，差异点仅分支后缀 `-r2`、validate2 flips 翻案记账（`team.yml:3948`）。
- **辅助面**：workers-wall-merge（`team.yml:851`）是无 droid 纯脚本合并 job，登记为工人席墙出口合并面，不占席位；env-check（`team.yml:37` 引用）是零号门（非席位），其凭证面收口归 §3.3 图外件⑤。

**现状对位行号**（全部实读核实）：lead=`team.yml:52`、worker=`:503`（裸跑 `:599`）、prep=`:936`、validate=`:1382`（双 token 置空 `:1390-1391`/`:1502-1503`）、revalidate=`:1779`、replan=`:2141`（会话零 token `:2210-2211`、落单 `:2420-2423`）、assemble=`:4389`（PAT `:4431`）。

### 2.2 七席位门清单（TOML 段样例）

七席各一张门清单（`foreman-caps.v1.toml` 目标态样例，**设计稿底稿非施工**），全文见底稿 `docs/wall-v3/seat-gates.md` §2。本节逐席给 default-deny 全集口径（段样例结构以底稿为准，四要素→键映射：入口=entry、出口=events_produced＋artifacts、工具=api＋local_uses、写目标=artifacts、令牌=authorization.token_scope）：

**lead**（现状包装入口 `team.yml:202-204`：`FOREMAN_RUN_PATCH=1 … run_droid_session.py --wall foreman-run.json --role lead`，预算 600s `foreman_run_lib.py:38`）——写目标收窄为 `team/lead-plan-segments/*.json` 唯一工作区面；现状「repo 工作区任意文件写（无机器守卫，仅 prompt 纪律）」与「repo 全树读」（锚件 2 §1）**多出的门默认删**（§2.4 表 1/3）。**default-deny 声明：本席可用工具、可写目标、可发事件、可读状态、可持令牌以门清单段为全集，清单之外不存在。**

**worker**（现状矩阵 `team.yml:503`，timeout 25m `:508`；会话**裸跑** `:599`——worker2 同款 `:2784`）——收口=收进包装器（§2.5），写目标=卡面 allowed 集合（F-1 载体，`team.yml:731` reset --soft 对比面）＋handoffs/status/delta 三路径；verdict.json/md 顶层孤儿路径不是本席制品，默认删（§3.2 件④）。令牌：会话步零 GH token（最小面维持），commit 步 github.token（`:710`）。**default-deny 声明：会话可写文件以卡面 allowed＋handoffs/status 为全集、可调工具以包装器白名单为全集、可持令牌以 token_scope 为全集——清单之外不存在；裸跑形态不是本席的门，是待废止越权形态。**

**prep**（`team.yml:936`，纯脚本零 droid 零 BYOM；补卷接线 `:1223-1226`）——写面=候选分支＋补卷器 packs 缺失件；步级超时 600s/300s 入 budgets 键。**default-deny 声明：零 droid 会话、零 BYOM；可写面=候选分支＋packs 缺失件——清单之外不存在。**

**validator**（`team.yml:1382`；job 级与步级双 token 显式置空 `:1390-1391`/`:1502-1503`；包装 `:1534`，预算 480＋adopt 储备 120 `foreman_run_lib.py:43-44`）——全链唯一零 GitHub 权席；可写面=verdict 系列＋证据对象；可读面=证据包＋墙；预算三键（会话墙 480/会话总预算键 480s/软超时 500，双 480 语义区分与 job 墙对平见底稿 seat-gates §2.4 budgets 注）。**default-deny 声明：零 GitHub 写权；可写面=verdict 系列＋证据对象——清单之外不存在。**

**replan**（`team.yml:2141`；包装 `:2405-2406`；落单步 `:2420-2423`）——**两会话面拆门**：现状「无 token 会话步（`:2210-2211`）与全权 issue 写落单步（`:2423` GH_TOKEN）同 job 混合」是多出的门，默认删后拆为「无 token 会话门＋落单写门」两个子门分别授权独立审计；死因叙事只能挂证据对象或取「未明」（§2.6）。**default-deny 声明：可写面=team-plan-v2.json＋拆门后独立授权的落单写；无证据不出因果结论——清单之外不存在，「未明」是唯一合法缺省。**

**assemble**（`team.yml:4389`，纯脚本零 droid；墙权威 pick `:4420`；PAT 写板单点 `:4431`→`:4441` project_state_write）——GitHub 写面=板面 PAT 单点＋PR create（`:4448`）＋issue 关闭/评论（`:4659`）三登记面；两令牌按写目标分面禁混用；human_stop（schema `:33`）消费门补齐（§2.3 probes）。**default-deny 声明：零 droid；写面=板面 PAT 单点＋PR＋issue 三登记面——清单之外不存在。**

**recorder**（目标态立席；承载点 `team.yml:1515`/`:1223-1226`；D-2 封章粘性 `salvage_verdict.py:121` sealed）——可写面=verdict-partial（`salvage_verdict.py:18` PARTIAL_NAME）＋status 骨架＋补卷记录三路径；零跨席读、零 GitHub 写；**缺席（该写不写）不是豁免，是告警事件**（§5.2 INV-1/2）。**default-deny 声明：可写面=三路径——清单之外不存在。**

### 2.3 与引擎 M-CAP 的对位表（7 席 × 键集满覆盖）

引擎 M-CAP 门清单段逐键原物锚（引擎仓 `docs/specs/module-capabilities.toml:574` 起；`entry=:579`、`api=:588` 双形态、`guard_test=:596`、`events_consumed=:598`、`state_reads=:601`、`callers=:604`、`authorization=:618` 三面、`verification=:623`、`probes=:630`）。

**键集口径**：本表键集＝引擎 **12 键**（MODULE_KEYS，`tests/test_module_capabilities_contract.py:55-68`：entry/api/guard_test/events_consumed/events_produced/artifacts/state_reads/local_uses/probes/callers/authorization/verification；mission 文档通称「十键＋三锚」「协作五键＋v5 三键」「十一显式键」皆为历史别名，均指此 12 键集）＋域扩展 budgets；M-CAP 段内 events_produced/artifacts/local_uses 三键现状缺席属词表可选键合法缺省（缺席≠删除，引擎契约注释原物 `tests/test_module_capabilities_contract.py:159` 区段），对位按「形制同构（可选缺省）」判定。

**对位判定词**：同构收编（现状已有同形面，收编登记）／多出默认删（现状能力超出应登记面，删；保留须单独呈裁）／多出呈裁（职能面超出形制键集应登记面，登记后保留项呈裁）／缺门补齐（应登记面现状缺失，列补齐方案）。

| 键 | lead | worker | prep | validator | replan | assemble | recorder |
|---|---|---|---|---|---|---|---|
| entry | 同构收编 | 缺门补齐（包装器） | 同构收编 | 同构收编 | 同构收编 | 同构收编 | 缺门补齐（立席） |
| api | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 |
| guard_test | 缺门补齐 | 同构收编 | 同构收编 | 同构收编 | 同构收编 | 同构收编 | 同构收编 |
| events_consumed | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 |
| events_produced | 多出呈裁 | 多出呈裁 | 同构收编 | 同构收编 | 多出呈裁 | 多出呈裁 | 同构收编 |
| artifacts | 多出默认删 | 多出默认删 | 同构收编 | 同构收编 | 同构收编 | 多出呈裁 | 同构收编 |
| state_reads | 多出默认删 | 同构收编 | 同构收编 | 同构收编 | 同构收编 | 同构收编 | 同构收编 |
| local_uses | 缺门补齐 | 缺门补齐 | 同构收编 | 同构收编 | 同构收编 | 同构收编 | 同构收编 |
| probes | 缺门补齐 | 同构收编 | 同构收编 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 |
| callers | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 |
| authorization | 多出默认删 | 多出呈裁 | 同构收编 | 同构收编 | 多出默认删 | 多出呈裁 | 缺门补齐（立席） |
| verification | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 | 缺门补齐 |

**动门＝边界事件声明**：对门清单任何增删改都是席位能力边界变更，必须走登记面升级闸（`wall-registry-change: true` 声明＋`mixed-registry-change` 判词 CI 执法）＋契约测试同批改＋多出门保留项呈大哥裁；换入判据「门清单不变」（§7）由此保障——动门即破坏「不变」前提，必须显式过闸。

### 2.4 多出的门总表（默认删；保留须单独呈裁）

| # | 门 | 席 | 现状锚 | 处置 |
|---|---|---|---|---|
| 1 | repo 工作区任意文件写（无机器守卫） | lead | 锚件 2 §1（会话步 `team.yml:202-204`） | 默认删；写面收窄 lead-plan-segments |
| 2 | I8-B 假 PAT 活验分支内嵌生产 workflow | lead | `team.yml:419`（夹具变量）、`:429`（标题命中）、`:430`（export 换 token） | 默认删；夹具仓化归 §3.2 件②；保留须呈裁（物理隔离方案） |
| 3 | repo 全树读授权（会话默认全读） | lead | 锚件 2 §1 | 默认删；读面登记 state_reads |
| 4 | verdict.json/md 顶层孤儿写路径 | worker | worker prompt 单源（checks 副产物自删纪律） | 默认删；包装器预授权不含＋探针判红（§3.2 件④） |
| 5 | verify 步全仓 subprocess 无超时 | worker | 锚件 2 §2（verify 面） | 默认删；收口卡面 checks 白名单＋300s 步超时 |
| 6 | 会话面与落单写面同 job 混合 | replan | `team.yml:2210-2211`（会话零 token）vs `:2423`（落单 GH_TOKEN） | 默认删；两会话面拆门（§2.2 replan） |
| 7 | 5 secrets 全量入 env-check 环境 | env-check（零号门） | `env-check.yml:82-86`（gate 步五注入）、`:238-240`（wall 步三件重复） | 默认删；按消费分离注入收口（§3.3 件⑤） |
| 8 | 板面终态图外写入口（Item closed 自动化翻板） | assemble（板侧） | `docs/板面关单翻板-最小操作指引.md:12-14`（三单实测）、`:24`（repo 不可拦截结论） | 默认删的落点在板侧 Disable/终态选项改造（人工，呈裁清单 §8）；repo 侧配合=board_drift 终态一致性复核（§3.2 件①） |

**呈裁口径**：任一默认删的门若有保留理由，必须逐条单独呈大哥裁，呈裁件须含：门的现状锚、保留理由、收窄后的执法设计、caps-gate 判词——不允许「先保留后补登记」。缺的门补齐方案汇总（8 条）见底稿 seat-gates §3.5，其中能力面登记文件、caps-gate 守卫与契约测试、工人包装器接线、recorder 立席四项是本稿 §2/§4 已定义设计，其余按底稿执行。

### 2.5 工人席收进包装器（硬规则①落位）

**废止对象**（现状）：裸跑形态 `timeout --signal=TERM --kill-after=30s 900s ~/.local/bin/droid exec --auto high …`（`team.yml:599`；worker2 同款 `:2784`）。三点不合规：①不经包装器（run_droid_session.py 的墙预算/心跳/patch 面对工人席不存在；budgets lint 明文豁免——`lint_workflow_budgets.py:17-18` BARE_DROID 正则、`:43-51` worker/900s 豁免分支）；②900s 硬编码在 workflow 文本，墙上账面值（`foreman_run_lib.py:53-54` worker droid_wall_sec=900）不被执行路径读取——预算是账面非执法；③执法与会话同体（45B 实证：孤儿子进程持管道拖到 25m job 墙，锚件 2 §10-②）。

**接线设计**（目标态）：worker job 改经 `run_droid_session.py --role worker --caps foreman-caps.v1.toml`——caps load（schema 校验畸形即 exit 2）→预算推导（软超时 = job_timeout_sec − 400，基座＝门清单 budgets 键的 job timeout——公式照引擎 `run_lead.sh:6` timeout−400s 口径，该口径的 timeout 即 job timeout：`droid-review-lead.yml:35-37` 明文 margin 400s 保证哨兵先于 GitHub 硬杀；droid 墙预算是包装器 T0 计时面，不进公式）→体外执法启动（§4 终止序列）→墙 patch（write_worker_delta 既有分类器复用，`team.yml:836` 上墙）。**预算从门清单读——预算唯一来源=门清单 `[seat.worker.budgets]`**，workflow 文本零预算字面量；裸跑字面量废止后，caps-gate BARE_DROID 探针与 budgets lint 同判词双载体执法，`lint_workflow_budgets.py:43-51` 豁免分支同批废止——裸跑形态对 7 席一律红，零豁免。

**会话级配置从门清单生成**（确定性生成、可复演）：①工具白名单注入（api＋local_uses → 会话 tools 白名单；形制对位引擎 `run_lead.sh:67` LEAD_ENABLED_TOOLS 单行默认值）；②写目标预授权（artifacts workspace-write 面 → F-1 allowed 集合，越界写事中拒绝）；③令牌 scope 最小化（token_scope → 环境注入最小集）。生成物落 `session-config.json`（预算/白名单/写目标/令牌四节），caps-gate 对平测试断言「会话配置与门清单逐键一致」。**包装器即执法点**：四面执法动作都发生在包装器进程内，会话本体无自授途径。worker2 同构收进。

### 2.6 结构化交接物 schema（硬规则②落位）

四类交接物的目标态 JSON Schema 全文见底稿 `docs/wall-v3/handoff-schemas.md` §2-§5（worker-delta.v2／verdict.v2／plan-v2.v1／handoff.v1）。四原则一次定死：

1. **因果结论枚举化**：死因/归因/冲突判定只能取枚举值（worker-delta.v2 `cause` ∈ {self_completed, wall_kill, job_wall_cancel, self_crash, unknown}；verdict.v2 judged[].cause ∈ {checks_red, evidence_incomplete, out_of_card_conflict, aligned_pass, unknown}；plan-v2 `cause` 增 `f1_rejected_machine_confirmed`）。
2. **证据引用强制**：因果结论非 `unknown` 必挂非空 `evidence_refs`（`$eid:<id>` 引用，解析到已登记证据对象，悬挂引用拒）；`unknown` 时必须为空数组。
3. **「未明」缺省**：无证据时唯一合法取值 `unknown`（枚举显式成员，required 强制）。
4. **自由文本不承载判定**：reason/summary/narrative 只给人看；机器判定只读枚举与证据引用，两判定通道字段级物理隔离。

**证据对象构造权单源**：证据对象（id/kind/origin/path/line/sha256/excerpt/created_by/墙引用）只能由核查环节构造——机器守卫步（F-1/caps-gate/budgets lint/delta 分类器）、validator 会话（经 recorder 工具）、prep 补卷器、adopt 采认步四个白名单；lead/worker/replan/assemble 会话零构造入口（包装器不暴露登记通道）。执法=caps-gate `evidence-construct-violation` 判词＋`narrative-without-evidence` 判词。确定性纪律：证据对象无墙钟时戳、用 run_id/job/step 墙引用（对位引擎封印确定性形制要点 8）。

## §3 写入口收口、图外件清零清单与钥匙总管理（三件套之二）

### 3.1 写入口收口（硬规则⑤）

全链写面单点化：**板面**=assemble PAT 单点（`team.yml:4431`→`project_state_write` `:4441`；板面权威审计镜像声明 `:4599`）；**repo 工作区**=各席 artifacts 登记面（§2.2）；**issue/评论**=各席 events_produced 登记面；**墙**=包装器/守卫机器写。任何席位出现登记面外写目标=caps-gate `out-of-scope-write` 红；板面写非单点=`token-scope-violation` 红。写入口收口与图外件清零是同一原则的两个面：图内收口（本节）＋图外清零（§3.2）。

### 3.2 图外件清零清单（六件，硬规则⑩落位）

判定口径与逐件四要素全文见底稿 `docs/wall-v3/out-of-graph-artifacts.md` §0-§2（图内=门清单登记面覆盖；图外=登记面之外的自动化/会话/凭证面）。六件一张表（每件四要素：现位置锚／图外性判定／收编或禁绝／责任席位；件③收口面=11 位点：team.yml 8＋droid.yml 1＋droid-probe.yml 1＋probe6.yml 1）：

| # | 图外件 | 现位置锚 | 图外性 | 收编/禁绝 | 责任席位 |
|---|---|---|---|---|---|
| ① | 板面 Item closed 自动化（关单翻板） | 板侧 Projects #33 内建规则（非 repo 树）；证据 `docs/板面关单翻板-最小操作指引.md:12-14`（演员 `github-project-automation`，三单实测） | 触发面/执行体/写目标三重图外（专档 `:20` 仓内零写入点、`:24` repo 不可拦截） | 禁绝（板侧 Disable 或终态选项改造，操作指引 `:26` 起；验收判据 `:37` timeline 零翻板）＋收编（装配席 board_drift 对账：漂移记账→PAT 单点重写→仍漂移硬评论报警；env-check 探测项 WARN 登记） | 板侧=大哥；对账=装配席；探测=零号门 |
| ② | I8-B 标题键控假 PAT 夹具 | `team.yml:419`（`I8_LIVE_B_INVALID_GH_TOKEN` 变量，ghp_ 前缀族哑值——只记名不转录）、`:418`（夹具注释）、`:429-432`（标题命中→export 换 token→echo→收尾 fi） | 执行条件图外（issue 标题是活验编排信号非门面输入）＋生产消费为零＋值住生产文本违反零值登记 | 禁绝三步：夹具仓化（对位在树 C 型夹具 `.github/workflows/i8-zero-escape-live-c-fixture.yml` 独立文件形制）→生产文本净化（删 `:418`/`:419`/`:429-432`）→活验断言改道探针；守卫负例常驻（生产 workflow 出现 `I8_LIVE_B` 或 PAT 前缀族即红） | lead 席默认删行（§2.4 表 2）＋大哥退役批；探针改道=验收席面。workflow 文本编辑是治理行为（走 wall-registry-change 通道），不在任何会话席门清单——recorder 门清单（零 workflow 编辑权）不承接本件 |
| ③补 | probe 族 BYOM 位点（件③的锚集扩展，非新增图外件） | `droid.yml:25`（Write BYOM settings，replica pattern）＋`:62`（FACTORY_API_KEY）、`droid-probe.yml:13`＋`:46`、`probe6.yml:10`＋`:44`——生产/探针 workflow 的同形 BYOM 声明体，与 team.yml 8 位点同构（headers 键位×ci-key/cf-aig-authorization/apiKey） | 同件③三型：重复展开无登记＋无席位差异声明＋写文件位 `~/.factory/settings.json` 图外；硬规则⑨「全部凭证」口径下凭证收口面不因 workflow 文件归属（非领班席）而遗漏 | 收编随件③一并执行：11 位点改 `write_byom_settings.py` 单行调用；对账判据 1 的位点扫描覆盖全生产 workflow 树（4 文件锚集）；probe 族凭证最小集随 §8 裁决项 3 一并呈裁 | 写板席（声明体）＋大哥（scope 裁定）＋caps-gate（对账，锚集含三件锚） |
| ③ | BYOM 三件＋FACTORY_API_KEY 11 位点重复展开 | team.yml 8 个「Write BYOM settings」步（`team.yml:117/:529/:1460/:1880/:2176/:2723/:3702/:4113`）＋非领班生产/探针面 3 个同形步（`droid.yml:25`、`droid-probe.yml:13`、`probe6.yml:10`）；FACTORY_API_KEY 独立注 team.yml 8 处（`:157/:568/:1501/:1916/:2209/:2757/:3738/:4147`）＋`droid.yml:62`/`droid-probe.yml:46`/`probe6.yml:44` | 重复展开≠登记（11 份平行配置零对账）＋无席位差异（四角色同拿三件）＋写文件位（`~/.factory/settings.json`）图外＋生产/探针面同形声明体游离于领班收口面之外（硬规则⑨「全部凭证」口径） | 收编：单点声明体 `write_byom_settings.py`（11 位点改单行调用——team.yml 8 步按席收口，`droid.yml`/`droid-probe.yml`/`probe6.yml` 3 步同形收口）＋按席差异化 scope 矩阵（呈裁两条见 §8，probe 族纳入裁定面）＋台账「1 条登记＋N 条消费锚」（§3.4，对账锚集含三件锚） | 写板席（声明体）＋大哥（scope 裁定）＋caps-gate（对账） |
| ④ | verdict.json/md 顶层孤儿件 | mission 工作区顶层两件（非 repo 树、非 tracked；生成演员不在链内） | 位置孤儿（链上 verdict 有唯一语义与合法落点）＋生成演员未登记＋墙权威 pick 口径下的冒充风险 | 禁绝（清理，人工——本 mission 边界条款禁动）＋收编（recorder 席 verdict 合法落点白名单＋caps-gate 防复活负例：树内白名单外 verdict 落点即红；诚实边界：工作区顶层无 CI 执法点，人工巡检判据登记） | 写板席（命名空间）＋人工（清理） |
| ⑤ | env-check 五 secrets 全量入环境 | `env-check.yml:82-86`（gate 步五注入 S_* 面）、`:238-240`（wall 步三件重复展开）、presence 布尔消费 `:155-163` 区段、板面探测 PAT 真消费 `:194-200`、`env_check_wall.py:65-67`（wall 步布尔重复取值） | wall 步重复展开（布尔与 gate 步重复）＋值在场暴露面未登记＋注入位点无对账 | 收编：wall 步归零（`env_check_wall.py` 改读 gate 步 tsv 继承，零 os.environ secret 读值）＋gate 步暴露面登记进台账＋位点对账守卫（`${{ secrets.* }}` 展开位点集合≠台账锚集即红） | 零号门＋写板席＋caps-gate |
| ⑥ | memory/ 运行态图外会话面 | repo `memory/` untracked 运行态树＋`~/.memory-core/` hook 态根（memory-core 运行态，本 mission 不碰） | hook 进程图外运行＋会话记录不进墙不采认＋untracked 结构性图外 | 收编接口不收编运行：图外记录作死因佐证必须先入库转图内证据对象（§2.6 构造权单源）；全部席位门清单显式禁写 memory/；台账 `[[external_face]]` 登记 | 改计划席（输入面）＋写板席（入库规范）＋领班席（编排声明） |

**清零判据汇总**（「图外=0」的机器定义，逐件负例载体与三态纪律 cleared／cleared-with-declaration／blocked）见底稿 out-of-graph §4 表：六件判据全部可断言；板侧动作（件①）按三态纪律登记 **blocked 待大哥**，不虚称 cleared。每件清零后的归宿都落在对应席位门清单内（①归装配席/零号门、②归 lead 席默认删行＋大哥退役批——workflow 编辑是治理行为，recorder 门清单不含 workflow 文本、④归写板席命名空间、③归各席 token_scope（收口面 11 位点，见本节表③行）、⑤归零号门、⑥归改计划席/写板席）。

### 3.3 图外件⑤的凭证面锚集（凭证面唯一口径）

env-check 凭证面锚集以底稿 out-of-graph §2.5 为准，四个区段行号锚（全部实读核实）：

- **gate 步五注入**：`env-check.yml:82-86`——`S_FACTORY_API_KEY`/`S_WORKER_CI_KEY`/`S_GW_TOKEN_KNOWN`/`S_GO_GITHUB_RUN_TOKEN`/`S_PROJECTS_STATE_PAT` 五行 env 展开（presence 布尔消费＋PAT 真消费的机制性最小暴露）。
- **workflow_call 声明面**：`env-check.yml:24-34`（五 secrets 声明）。
- **板面探测真消费**：`env-check.yml:194-200`——`S_PROJECTS_STATE_PAT` 优先作 PROJECT_TOKEN 探板。
- **wall 步重复展开**：`env-check.yml:238-240`——三件再注入，`env_check_wall.py:65-67` 布尔读值与 gate 步 tsv 重复；⑤收口后 wall 步归零，台账三锚删除。

### 3.4 钥匙总管理台账（硬规则⑨落位，引擎 M2 口径）

**承载文件（目标态）**：`docs/specs/foreman-keys.toml`——形制照抄引擎 `docs/specs/key-registry.toml`：零密钥值（铁律原文 `key-registry.toml:11` 引擎仓）、schema 一次定死＋同批改锁（`:14` 引擎仓）、三态词表 use/cap_change × active/dormant/zombie/revoked（`:25` 引擎仓）。**现状登记面（七条，零值预填，全文见底稿 out-of-graph §3.3）**：①FACTORY_API_KEY（use，8 会话步锚）②WORKER_CI_KEY（use，BYOM `x-ci-key` 位）③GW_TOKEN_KNOWN（use，`cf-aig-authorization` 位）④GO_GITHUB_RUN_TOKEN（use，BYOM `apiKey` 位）⑤PROJECTS_STATE_PAT（**cap_change**——板面 Status 是链终态权威面，写板=改终态能力；锚 `team.yml:4431`/`:4441`＋env-check `:86`/`:195`/`:240`）⑥github.token（platform_builtin 参考条目，按席 token_scope 已在 §2.2 登记）⑦I8_LIVE_B_INVALID_GH_TOKEN（**zombie**——件②拆除后消费面=0，探针退役批回读验证后转 revoked，防幽灵复活牺牲品样本）。另登记 `[[orphan]]`（件④）、`[[external_face]]`（memory 树／runner 会话配置／探针 workflow 族）、`[[dangling_name]]`（⑦退役落位）。

**对账判据（五判＋牺牲品链）**：①展开位点对账（生产 workflow `${{ secrets.* }}` 展开行集合=台账 consumes 锚集——位点扫描覆盖全生产 workflow 树（含 `droid.yml`/`droid-probe.yml`/`probe6.yml` 等非领班席工作流，硬规则⑨「全部凭证」口径），多出=orphan-secret-expansion 红、失配=anchor-drift 红）②值泄漏扫描（前缀族全文件扫描，清零前唯一登记例外位=件②夹具哑值，限期消除）③旁路检出（声明体单点/顶层孤儿=0/PAT 时间线演员单点三面巡检）④牺牲品样本（件②假 PAT 走 zombie→回读→revoked→dangling 全链演练）⑤名单对账（在役 repo secrets=5；载体呈大哥裁：季度人工 `gh secret list` 留痕 or PAT 权限实测后机器对账）。**升级闸**：改台账＋守卫本体的变更集须带 `key-registry-change: true` 声明行，否则 `mixed-key-registry-change` 红；钥匙面守卫与对账判据全部接 foreman-wall-ci 恒跑（§0b 禁抄项义务）。对账流水 append-only（`docs/wall-v3/key-ledger.md` 目标态；「无回读不得记完成」对位引擎 gate-ledger 口径，引擎仓 `docs/governance/gate-ledger.md:12`）。

### 3.4a 零号门（env-check）门清单——零 GitHub 权限位与凭证最小面

env-check 是零号门（非席位），其门清单随本稿总装单列如下（全部锚经实读核实，`env-check.yml`）：

| 项 | 门清单登记 |
|---|---|
| entry | `env-check.yml:12` workflow_call（被 `team.yml:46` 以 uses 调用）＋`:45` workflow_dispatch（独立手动跑）——双入口 |
| 权限面 | `env-check.yml:58-61` permissions 三键最小集：`contents: read`＋`issues: write`（体检评论）＋`actions: read`（在飞 run 探测）——**零 secrets 权限位、零板面写权**（Projects 探测走 PROJECTS_STATE_PAT 注入而非 GITHUB_TOKEN） |
| 出口 | `env-check.yml:35-44` workflow_call outputs 三键（ok/foreman_ok/hard_fail_count）→ `team.yml:37` 门消费 foreman_ok；`env-check.yml:68-71` job outputs 三键（`:69/:70/:71`） |
| 凭证暴露面（件⑤收口前的机制性最小面） | gate 步五注入 `:82-86`（presence 布尔＋PAT 真消费）、wall 步三注入 `:238-240`（⑤收口后归零）、workflow_call 声明 `:24-34`（五件）；板面探测真消费 `:194-200`；逐件对账归 §3.3/§3.4 台账 |
| 体检面 | 七检查项（`env-check.yml:93/:110/:133/:155/:164/:190/:213`——工作流在册/令牌权限块/仓库设置/Secret 名单/工单完整/板面配置/并发队伍）＋边界明示口径（GITHUB_TOKEN 读不到的项报 WARN 非通过，如 `:190` 板面配置项） |
| 墙承载 | `env-check.yml:234-249`（Build ForemanRun wall 步，`env_check_wall.py` 读 gate 步 tsv 出墙切片）＋`:251`（墙 artifact 上传） |
| 探针（probes） | hard-fail 计数=0 放行（foreman_ok）； secrets 位点对账守卫（件⑤判据 3）与板面内建规则探测项（件①判据 2）施工后入本门检查序列 |
| budgets | job 墙 `timeout-minutes: 5`（`env-check.yml:67`）——零 droid 会话零 BYOM，无软超时公式面 |

**零门与席位门清单的关系**：零号门不是席位，不占 7 席名额（§2.1）；其凭证面暴露与收口归 §3.3（件⑤），其检查项扩展（板面探测/位点对账）走零号门自身升级通道（改 env-check.yml＝治理行为，带 wall-registry-change 声明，§3.6 升级闸口径）。

## §4 执法设计（执法在体外，硬规则③落位）

**原则**：任何门的执法通道不依赖被管进程配合。形制照抄引擎 run_lead.sh 终止序列（引擎仓 `src/infra_core/engine/droid_review/run_lead.sh:9-10` 头注原文「哨兵：lead-terminated.reason 先行（写哨兵 → SIGTERM 组 → 宽限 → SIGKILL）……哨兵在案 = findings 不采信（强制失败优先）」；实码 `:282` `kill -TERM "-$exec_pid"` 负 PID 组信号、`:286` `kill -KILL` 同形态）。

**双进程形态**：每席 droid 会话必须经包装器（lead/validator/replan 现状已包装——`team.yml:202-204`/`:1534-1535`/`:2405-2406`；worker 收进=§2.5），包装器＋监督者双进程：会话启动即从门清单生成会话级配置（§2.5 三步），监督者持预算计时器与哨兵权。

**终止序列**（照抄，执法通道与被管进程解耦）：预算到期（T0）→写哨兵（`session-terminated.reason`，T1）→SIGTERM 进程组→宽限（目标态 10s，对位引擎 `run_lead.sh:55` LEAD_KILL_GRACE_SEC 默认）→SIGKILL 进程组（T2 进程组真死）。**哨兵在案＝该席产物不采信**（delta/verdict/plan-v2 一律强制失败优先）。进程组整组收=45B 孤儿拖管道形态的根除：组信号不挑进程，孤儿子进程随组终结。

**有界退出预算面**（照引擎 `run_lead.sh:5-6` 头注纪律）：轮数封顶＋软超时（job_timeout_sec−400 公式注入——基座＝**budgets 键的 job timeout**（`job_wall_min`×60），与引擎口径对应：`run_lead.sh:6`「workflow 按 timeout−400s 公式推导注入」的 timeout 即 job timeout，`droid-review-lead.yml:35-37` 明文「margin 400s 保证哨兵先于 GitHub 硬杀」；droid 墙预算（droid_wall_sec）是包装器 T0 计时面，不进公式）＋心跳采样（纯观测不杀进程）；重试共享绝对墙钟预算（对位引擎 `run_lead.sh:318` LEAD_TOTAL_DEADLINE_EPOCH 绝对上限口径），最坏墙钟恒 ≤ soft＋宽限，不击穿 job timeout。**第 3 层回合熔断不可施工**（大哥已裁登记：droid CLI 无回合预算接口／外层早杀对工件保护更差／无续作能力——`docs/回合熔断上游特性需求登记-droidCLI.md:13-17`；上游三能力立项前置 `:19`）——v3.0 体外执法粒度上限=会话级进程组终止＋落盘产物机器回收，本稿任何章节不得把回合级执法表述为可施工承诺。

**CI 接线**：caps-gate 守卫接 foreman-wall-ci 恒跑（push 与 PR 两腿同面，零 if 零 continue-on-error）；放行门单源=ruleset required_status_checks（照引擎要点 6，两门口径 §0b），不在代码养第二套门表。

## §5 逐席位失败规范、缺席即事件与结构盲区（三件套之三·判据侧）

### 5.1 七席位失败规范（硬规则⑧落位）

七席各一份失败规范，照引擎点位普查表形制（引擎仓 `docs/guides/exception-point-inventory.md:27` 表头五字段）四字段成文——**怎么死／死了谁知道／谁处置／机器判据**（＋缺口定级）。全文见底稿 `docs/wall-v3/failure-specs.md` §1-§7，本节登记各席主判据与定级（判据只引三类机器载体：墙上机器记录／守卫退出态／stream 机器事件；会话自述不进判据）：

| 席 | 怎么死（主型） | 机器判据（主） | 现状定级 | v3.0 收口 |
|---|---|---|---|---|
| worker | A 墙杀（裸跑 900s，exit 124/137 机器杀印）；B 落盘未遂（58-D hslconv 主型）；C 自崩 | delta 三字段机器分类（`write_worker_delta.py:45` classify_session_outcome；124/137→wall_killed）；补卷守卫四条件 ALL-of（`worker_salvage.py:13` docstring，fail-closed） | 部分 | 收进包装器＋体外执法（§2.5）；必死样本 SL-3 |
| lead | 墙杀/计划残缺/越权写/门未过 | 包装器墙 patch＋stitch 退出码＋caps-gate `out-of-scope-write` | 部分（③无信号面——lead 会话写无机器守卫） | caps-gate 三探针；SL-1/SL-4b |
| validator | 墙杀（协议致延迟落盘主型）/停滞/证据包破/判定残缺 | D-2 封章粘性（`salvage_verdict.py:45-47` D-2 seal 语义＋adoptable；粘性实码 `:121` sealed）＋红章判死（`validator_prompt_template.py:97` HARD RULE）＋manifest sha 门 | 部分（③缺席报警无 per-run 载体） | recorder_call_count 入墙＋缺席告警；SL-2 |
| replan | 墙杀/**叙事违约**（脚本内置推断，四问题①）/落单违约/归责错位 | 死因只能取枚举＋证据强制（f1_rejected_machine_confirmed 只能由机器守卫记录构造）；钉子反转（r53c `:190-205` 现状钉子逐字断言→条件断言）；落单机器闸（`team.yml:2420-2423`） | 部分（②③缺口） | 钉子反转＋plan-v2 schema；SL-3b' |
| prep | 步级超时/merge 失败/守卫拒 | timeout 退出码 124＋git 退出码＋守卫四条件 | **有** | 守卫四条件接受失败矩阵测试（SL-5 倒影） |
| assemble | pick 拒/板面写失败/翻板/收口残缺 | fail-closed pick（`team.yml:4420`）＋closeout 布尔（schema `:214`）＋board_drift 对账＋lint 收口断言 | 部分（③翻板无信号——板侧 blocked） | board_drift＋human_stop 消费门；SL-6/SL-7 |
| recorder | **缺席**（逐件落盘缺席/承载会话死/封章缺席） | 包装器采样 recorder_call_count＋PARTIAL_NAME 落点存在性（`salvage_verdict.py:18`）＋sealed 粘性 | **无**（7 席唯一零信号席——四问题④正席） | 立席＋缺席即事件；SL-8a/RS-4 |

**根治 1+2+4 并入声明**（不再单独立项；批准范围锚 `docs/R58D-收尾决策留痕-NC6与遗留决策点.md:5` 十文件子集口径）：第 1 层补卷守卫/补卷器（`worker_salvage.py:13` 四条件）并入 worker/recorder 席处置列；第 2 层模板单源（`worker_prompt_template.py:13` Incremental persistence guidance，P-2 口径预期封顶——措辞无运行时效力）并入缺口列；第 4 层死亡上墙＋归责根治（`team.yml:836` delta 上墙、`team.yml:885` merge_worker_deltas、schema `:146-157` 三映射、`attribution_reason.py:75` neutral_attribution 分支化）并入 worker「死了谁知道」与 replan「机器判据」。**规格明文**：补卷覆盖面 ≠ 中性归因覆盖面——补了卷不等于归因已中性化。

### 5.2 缺席即事件（硬规则⑥落位）

**口径**：某席位的必交件/必落字段/约定首步在判定窗口内未出现，即视为一次事件（not "nothing happened"）；判据形态统一为「观察点在窗口截止时点读取授权计数器/落点存在性，计数=0 或落点缺席→告警事件（墙记缺席面＋硬评论）」——零 prompt 依赖（P-2 终裁口径 `docs/V-3-closeout-收档报告.md:56`：措辞类约束无运行时效力）。

**不变量清单 INV-1..7**（窗口值单一来源=席位门清单 budgets 键）：INV-1 recorder 调用数>0（validator/worker 会话，首步窗口＋全程窗口）；INV-2 verdict-partial 首步落盘；INV-3 sealed 封章窗口内达成（超窗=不采认＋round 重验＋告警）；INV-4 worker-delta 每 pid 恰一条；INV-5 plan-v2 落单（should_replan=true 时）；INV-6 final_status_card patch；INV-7 evidence manifest 齐。缺席告警不改链采认语义（该 fail 仍 fail）——告警是可见性执法，处置由守卫既有 fail-closed 承载；告警必含定位字段（席位/窗口/缺席面/观测值）。59 轮四问题④的教训正是「缺席既无处置也无可见」——先补可见性（INV-1/2），per-run 报警由此门承载；V-3 门（受控会话达标证明）保留为发版前置人工门（G-2 制度，`docs/V-3-closeout-收档报告.md:15`）。

### 5.3 结构盲区（显式列出，照引擎普查表 `exception-point-inventory.md:94` 盲区范式）

五项显式登记：①第 3 层回合熔断（结构性不可见——回合是 agent-loop 内部概念，§4 不可施工口径）；②请求级停滞（死亡账第 5 类，网关侧成因，机内零信号，登记仓外成因另案）；③板面关单后翻板（触发面图外，run 结束后无触发器可挂——板侧禁绝主责＋图内发现与纠正，不冒充阻断）；④工作区顶层孤儿件（repo 外无 CI 执法点，人工巡查判据）；⑤memory/ 运行态面（untracked 结构性图外，接口收口不收编运行）。逐项定性见底稿 failure-specs §8。

## §6 逐条规则验收线（三件套之三·验收侧）

### 6.1 「没有活验数字不算建成」判据（硬规则④收口条款）

> **墙的建成判据不是「守卫存在」「lint 全绿」「文档成文」，而是四条活验数字，缺一即未建成：**
>
> 1. **必死样本全红率**：SL 族每个样本对其目标守卫的红灯率=100%（对违约输入必红，对合法输入必绿——红绿对照对全）。
> 2. **执法延迟上界实测数**：每面执法墙本次 CI 的 L 上界数字存在且 ≤ 设计上界；该数字必须是本次运行实测值（非历史值、非常量）。
> 3. **哨兵在案不采信率**：违约会话的产物采认率=0%（强制失败优先）。
> 4. **缺席报警触发率**：缺席注入样本的告警触发率=100%，且告警含可定位字段。
>
> 四条全部由 CI 常驻测试输出数字，任何人复跑 `pytest tests/ -q` 可复现。没有这四组数字的墙一律按「未建成」登记——纸面有门不执法的形态按 §0b 禁抄项处理。

### 6.2 必死样本设计与执法延迟口径（硬规则①③④⑤⑥⑨⑩的验收面）

**必死样本三要素**：确定性注入（fake-droid 桩——恒挂/吞 TERM/fork 孤儿/越界写/伪造叙事，零网络零真树污染）；守卫在岗断言（真跑守卫本体，断言退出态不是源码存在性）；必杀断言（执法类墙断言违约会话进程组真死＋产物不采信）。桩协议与十二族样本（SL-1..SL-12）逐样本六要素设计全文见底稿 `docs/wall-v3/acceptance-line-map.md` §1-§2；SL 族与 59 轮回归样本（RS-1..4）互锁表见其附B。族一览：

| 样本族 | 对象墙/门 | 注入→断言（要点） |
|---|---|---|
| SL-1 | lead 会话墙 | 恒挂桩→哨兵在案＋进程组真死＋分段卡不产（fail-closed）＋预算 patch 上墙 |
| SL-2 | 证据授权门（validator 面） | 伪造叙事（cause=checks_red 无证据／枚举外值／reason 内嵌判定）→schema 拒＋adopt 拒采＋判定通道不读 reason |
| SL-3 | worker 会话墙（包装器） | fork-orphan 桩（45B 形态复现）→**进程组整组收**（父子与孤儿全不存在）＋delta 不采信＋wall_killed 分类正确 |
| SL-3b/SL-3b' | 写目标门＋证据授权门（replan 面） | 越界写→守卫拒＋delta files 双红；伪造死因（枚举外 F-1 文案／无机器证据的 f1 断言）→拒＋钉子反转正样本 |
| SL-4 族 | lead 图外写口＋令牌 scope 门 | 图外写口/越权令牌注入→caps-gate 判词红＋现状树干净对照绿（守卫不冤枉现状） |
| SL-5 | 补卷守卫（根治 1 倒影） | 四条件逐条违约（merged=false/F-1 越界/红 checks/exit-0+ok control）→全部不补卷；exit-0+ok 永不翻案（在树先例 `tests/test_worker_salvage.py:293`） |
| SL-6 | 板面终态门 | 漂移态注入（板面读桩）→board_drift 必产＋重写板一次＋仍漂移硬评论＋零漂移对照不误报 |
| SL-7 | 图外写口（文本层） | 四注入（PAT 前缀族字面/I8_LIVE_B 残留/verdict 白名单外落点/secrets 位点失配）→判词点名红＋现状树绿 |
| SL-8a-e | 缺席即事件门 | 五缺席变体（recorder 零调用/delta 缺席/封章缺席/收口 patch 缺席/evidence manifest 缺席）→告警必产＋字段可定位＋墙字段在 |
| SL-9 | 交接口枚举门 | 四 schema 违约表 19 变体→全拒＋合法对照全绿 |
| SL-10a-d | caps-gate 判词负例门（工具/制品/事件/状态读面） | 四注入（会话调用未登记工具/产出未登记制品路径/消费未登记事件/读未登记状态树）→各判词点名红＋干净对照绿（文本层注入，形制照既有 SL-4/SL-7 族） |
| SL-11a-c | 登记面与钥匙面升级闸门 | 三注入（非核查环节构造证据对象/门清单 schema 键集漂移未同批改契约/登记面变更无 wall-registry-change 声明）→evidence-construct-violation/caps-schema-drift/mixed-registry-change 判词红 |
| SL-12a/b | 钥匙面判词负例门 | 两注入（旁路面未登记入台账/钥匙台账变更无 key-registry-change 声明）→unregistered-bypass-surface/mixed-key-registry-change 红 |

**执法延迟实测口径**（逐字对位任务书）：延迟 = **超时点到进程组真死的时间差**。三时点机器可测：T0=预算到期（包装器注入预算 epoch，桩读单调钟差）；T1=哨兵写入时刻；T2=进程组最后成员退出（wait 收尸＋exit-stamp）。**上界口径**：L=T2−T0 ≤ **宽限＋SIGKILL 完成期**（T0 后包装器立即走哨兵→TERM→宽限→KILL 序列，只有哨兵写入＋宽限等待＋KILL 传播三段耗时；400s 软超时余量是「哨兵先于 job 硬杀」的作业窗口——引擎 `droid-review-lead.yml:35-37` margin 口径——不是执法延迟上界）。**多次采样取上界**：每面执法墙每次 CI 跑 N≥5 采样会话（立即死/TERM 后拖延/吞 TERM 靠 KILL 三种抗死形态各≥1＋普通≥2），取最大值为该墙本次延迟报告值；实测数落 CI 报告段＋逐采样行落 artifact（`wall-v3-latency.json` 目标态）；实测超设计上界（全样本 ≤ 宽限 10s＋SIGKILL 完成期 10s 采样护栏，宽限对位引擎 `run_lead.sh:55`）=墙建成失败。缺席类事件延迟口径=告警事件产出时延（同采样纪律）。诚实声明：延迟实测对象是包装器执法路径（桩进程组），生产会话死亡面由墙 patch 字段承载——两者是不同测量对象，上界护栏对两者同构成立的前提（组信号整组收）正是桩要证明的。

### 6.3 59 轮四问题回归样本（硬规则⑦落位）

四问题逐个「先钉死当年错误行为，再断言反转后的正确行为」，机制证据底座=锚件 2 §10：

**四问题①（replan 虚构死因）→ RS-1**：当年钉子=`tests/test_replan_context_and_skipped_outcome_r53c.py:190-205`（逐字断言「F-1 检查拒绝」文案必现于 prompt；机制锚 `team.yml:2259` Round-53 fix 推断注释起、`:2276` branch_present 判定、`:2278-2279` 文案赋值——分支缺席被推断为死因，F-1 真实机器记录从不进 replan 输入面）。反转三段：①无证据不出文案（分支缺席＋无 origin=f1 证据→prompt 死因面呈现「未明」，F-1 文案 count==0）；②有证据才出文案（合法机器证据对象在场→文案恰一次，count==1 条件化）；③schema 面 cause 枚举＋`f1_rejected_machine_confirmed` 构造权校验。归责对位：attribution_reason 分支按 cause 枚举渲染（`:75`）。

**四问题②（900s 墙不执法）→ RS-2**：当年=裸跑形态执法与会话同体（`team.yml:599`；45B 实测名义 900s 拖到 1800s job 墙；budgets lint 豁免 `lint_workflow_budgets.py:43-51`）。反转三段：①形态反转（BARE_DROID 探针零豁免）；②执法反转（SL-3 整组收＋延迟上界数字）；③预算反转（workflow 文本零 `900s` 字面量＋包装器读 `[seat.worker.budgets]` 对平）。第 3 层边界引用 §4 不可施工口径。

**四问题③（板面图外写口）→ RS-3**：当年=写板终态被板侧内建自动化 1–2 秒翻回（`docs/板面关单翻板-最小操作指引.md:12-14` 三单实测；`:24` repo 不可拦截）。反转三段：①发现面（SL-6 board_drift 必产）；②板侧禁绝判据（timeline 零翻板，`:37` 判据；三态登记 blocked 待大哥）；③repo 侧写点收口（板面写 PAT 单点违例=token-scope-violation 红）。

**四问题④（纪律缺席无报警）→ RS-4**：当年=逐件落盘服从率 0/4、墙杀回收 0/2、13 次工具调用零次以 handoffs/status 为目标、per-run 无报警字段（`docs/V-3-closeout-收档报告.md:11` 终审引文；G-3 登记维度 `:44`；54A/C 删失尾实测 `:47-48`）。反转三段：①缺席必报警（SL-8a→recorder_call_count=0 上墙＋告警）；②正样本门（G-2 制度 `:15`——机制上线前须真实会话流 tool_call 正样本在案，发版前置人工门保留）；③死亡账登记维度（墙 validation 切片扩 recorder_call_count 字段，schema 演进同批改锁）。

### 6.4 验收线总表（硬规则 × 样本 × 口径）

| 硬规则 | 验收线承载 |
|---|---|
| ①门清单＋包装器 | SL-3＋SL-10a-d（缺登记面族）＋SL-11b＋RS-2 |
| ②交接物结构化 | SL-9＋SL-2/SL-3b'＋SL-11a（构造权越权） |
| ③执法体外 | SL-1/SL-3（进程组整组收=体外性行为证明） |
| ④必死样本＋延迟实测 | 全 SL 族（SL-1..SL-12）＋§6.1 四数字＋§6.2 延迟口径 |
| ⑤写入口收口 | SL-3b/SL-4b/SL-7＋SL-10b |
| ⑥缺席即事件 | SL-8 族（a-e）＋INV-1..7 |
| ⑦事故回归＋V-3 正样本门 | RS-1..4＋G-2 门登记 |
| ⑧失败规范 | §5.1 七席规范＋SL-5 倒影 |
| ⑨钥匙总管理 | SL-7 第④注入＋SL-12a/b＋§3.4 五判据 |
| ⑩无兜底不留图外 | SL-7 全注入＋SL-11c＋RS-3 板侧三态登记（blocked 不虚称 cleared） |

## §7 换入判据

**终局形态**（§0c）：领班是候选模块，测过后整模块换入引擎编排槽位替换 M-CAP。换入三判据，每条与引擎侧载体逐条对位（全锚实读核实）：

### 7.1 判据一：门清单不变

**口径**：换入时点领班模块的门清单（`foreman-caps.v1.toml` 七席段）与送审封印时点逐字节一致；换入后引擎编排槽位消费的门清单与送审版一致——「换的是模块实现，不是能力边界」。

**对位引擎载体**：门清单登记真源形制（引擎仓 `docs/specs/module-capabilities.toml:574` M-CAP 段起，schema_version=5 `:77`）；动门=边界事件过闸（§2.3 末）保障「不变」前提——换入窗口内任何 `wall-registry-change: true` 变更集都重置换入流程。

### 7.2 判据二：旧封印测试整套全过

**口径**：领班模块的封印快照（管辖文件清单＋每文件 sha256＋测试资产清点）在换入目标环境用**同一套规则**重算并逐项对平（exit 0），且旧封印所含契约测试整套在新模块树全过——不是抽样，是整套。

**对位引擎载体**：封印=sha256 指纹快照＋--verify 对平（引擎仓 `scripts/hardening_baseline.py:1` 工具头注「16 模块指纹基线工具……终态对平（--verify）用同一套规则重算并逐项比对落盘快照，模块管辖面未变即退出码 0」；对平实现 `:303`「重算目标 tree 指纹并与落盘快照逐项比对」；`verify: OK` 判定 `:388`）。快照确定性纪律（无时戳、无绝对路径、同 tree 重跑逐字节相同）照抄；施工期落领班域对应工具（foreman-caps 指纹快照＋verify 对平）。

### 7.3 判据三：失败规范对位

**口径**：换入后七席失败规范（§5.1）逐席对平——每席的怎么死/死了谁知道/谁处置/机器判据四字段在新模块环境仍然成立；引擎侧对应面=失败规范点位普查表（引擎仓 `docs/guides/exception-point-inventory.md:23`「全部活跃 workflow 失败点位清单（18 点）」、`:27` 表头五字段、`:94` 盲区范式）。

**字段级对平表（7 席 × 引擎点位，随本稿成文；不再推迟施工）**——领班域失败点位到引擎普查表点位的映射口径：同型死法对位（CI 红/执行器死/并发丢弃等），引擎 handler 形态是**形制参照**（承接件指纹/幂等卡/恢复闭环），领班侧承载照 §5.1 逐席处置列，不照抄引擎具体 workflow 名（两域触发面不同构）：

| 领班席 | 失败点位（领班域主型） | 引擎普查表对位点位（`exception-point-inventory.md` 行号） | 对位判定 | 对不平的登记 |
|---|---|---|---|---|
| lead | 会话墙杀（A）/计划残缺（B）/越权写（C）/门未过（D） | #2（main push 后 CI 红，`:30`）；#4（QG 真 FAILURE，`:32`） | 同型对位：墙杀/门红在两域都是「CI 面 job 红」家族；计划残缺对位 QG 真 FAILURE（判定产出不可采认） | lead C 类（越权写）在引擎表无对位行——引擎域对应面是 module wall 守卫（ci.yml 恒跑），按「形制对位（守卫红）」登记，不强行映射普查表行 |
| worker | 墙杀（A）/落盘未遂（B）/自崩（C） | #6（执行器 execute 步失败，`:34`）；#2（`:30`） | 同型对位：执行器步红=会话执行面死；落盘未遂的处置（补卷器）是领班域特有 handler，对位引擎「现有 handler」列的统一承接件形态 | 补卷守卫（根治 1）在引擎域无对位物——显式登记「领班域 handler 超集」，换入时以领班四条件全过为准 |
| validator | 墙杀（A）/停滞（B）/证据包破（C）/判定残缺（D） | #6（`:34`）；#4（`:32`）；盲区 §6.2（timed_out 恢复路径，`:95-97` 区段） | 同型对位；validator B 类（请求级停滞）与引擎盲区 2 同型——两域同列为结构性盲区，不对位到 handler 行 | 停滞类按引擎盲区范式登记（两边都不冒充有 handler） |
| replan | 墙杀（A）/叙事违约（B）/落单违约（C）/归责错位（D） | #6（`:34`）；#4（`:32`） | 同型对位（执行死/判定产出死） | 叙事违约与归责错位是领班域交接物死法，引擎域无同型行——按「领班域特有点位」登记，判据=plan-v2 schema＋钉子反转测试，换入时整族带过 |
| prep | 步级超时（A）/merge 失败（B）/守卫拒（C） | #3（ci-ok 聚合污染，`:31`——聚合步红家族）；#8（Board Sync 直合失败/403，`:36`——金标准幂等卡＋恢复闭环） | merge 失败对位 #8（git 面 403/冲突，引擎金标准 handler＝幂等哨兵＋计数＋升级——领班 prep 拒面按同形「fail-closed＋显式留痕」收口） | 步级超时（timeout 124）在引擎表无独立行——对位 #2 家族（job 红承载），显式登记 |
| assemble | pick 拒（A）/板面写失败（B）/翻板（C）/收口残缺（D） | #4（`:32`）；#9（Board Sync 非 r2merge 腿红，`:37`——聚合/判定步红无承接的空档面）；#12（Release announce 投递失败，`:40`——写外部面失败通知只留痕） | 板面写失败对位 #12 同型（写外部权威面失败）；收口残缺对位 #9（收口步红） | 翻板（C 类）在引擎域无对位——引擎域板面由 board-sync 承载且是金标准（#8），领班域翻板是板侧图外件（§3.2 件①，blocked 待大哥）——按「领班域特有盲区」登记，换入时带 §5.3 盲区 3 口径 |
| recorder | 缺席（A/B/C 三型） | 盲区 §6.1（并发丢弃 run——结构性不可见、schedule 对账承接，`:35` 行＋`exception-point-inventory.md:96-98` 盲区行） | 同型对位：缺席=「该发生的事件无产物」，与引擎并发丢弃同构（无信号面，靠体外对账/采样补可见性）——引擎用 schedule 扫描补洞，领班用包装器采样＋墙字段补洞，形制同构 | recorder 是领班域立席（引擎域无此席）——点位行本身按「领班域新增席」登记，对位只取盲区承接形制 |
| （盲区对位） | §5.3 五盲区（回合熔断/请求停滞/板面翻板/顶层孤儿/memory 面） | 引擎 §6 四盲区（并发丢弃/timed_out/非 r2merge 腿/check_run 事件盲区，`:94-98` 区段） | 两域盲区清单互不覆盖但同范式（结构性不可见显式列出）——换入判据=两边盲区清单各自完整且不冒充已承接 | 双方盲区行在换入对平表中各自成行，禁止互相消解 |

**对平执行方案（换入时点）**：以本表为起点，逐行复核引擎普查表在换入时点 main 的当前版（普查表随引擎 main 演化，点位行会增删——换入对平必须按当时实读重验，方法同锚纪律）；领班七席规范逐席对平四字段；对不平的点位=换入阻塞，显式登记不冒充。

## §8 待大哥裁决清单

以下裁定项按依赖序排列；每项含现状锚、选项与建议。裁决前施工面不得推进对应件（blocked 三态纪律）：

| # | 裁决项 | 现状锚 | 选项与建议 |
|---|---|---|---|
| 1 | **多出的门逐条保留与否**（§2.4 表 8 项默认删门） | 各行现状锚见表 | 建议全数默认删（本稿立场）；任一项要保留须按 §2.4 呈裁口径单独呈裁（现状锚＋保留理由＋收窄执法设计＋判词） |
| 2 | 板侧 Item closed 自动化处置（件①） | `docs/板面关单翻板-最小操作指引.md:26` 起（操作节）、`:37`（验收判据） | A=Disable 整条规则或删 Set Status 步；B=Set Status 目标改为「已验收」终态；「保留原样」不在可行集（与写板终态直接冲突，翻板实证）——建议 B（关单即终态，语义最贴链终态权威） |
| 3 | BYOM 按席 scope 裁定两条（件③） | team.yml 8 位点 `:120/:531/:1463/:1883/:2178/:2725/:3705/:4115`＋非领班面 3 位点（`droid.yml:25`、`droid-probe.yml:13`、`probe6.yml:10`，共 11 位点） | ①validator 族 BYOM 三件最小集（尤其 `cf-aig-authorization`/`apiKey` 位对该席会话必要性）；②FACTORY_API_KEY 与 BYOM `apiKey` 位（GO_GITHUB_RUN_TOKEN）双轨冗余裁定——裁前保守登记现状全量（11 位点），裁后收窄＋caps-gate 对账同步收紧；probe 族（droid.yml/droid-probe.yml/probe6.yml）的凭证面去留随裁定一并处理 |
| 4 | I8-B 夹具退役批（件②收尾） | `team.yml:419`/`:418`/`:429-432`；假 PAT 变量台账条目⑦ | 探针改道+夹具仓化施工（lead 席默认删行落地，§2.4 表 2）后，回读验证（哑值打不开）→revoked→dangling 表；退役批时点大哥定 |
| 5 | verdict.json/md 顶层孤儿件清理（件④） | mission 工作区顶层两件（非 repo 树；本 mission 边界条款禁动） | 移入证据档案面或删除（人工一次）；防复活负例施工后常驻 |
| 6 | secrets 名单对账载体（§3.4 判据 5） | repo secrets 五件（CI 内 github.token 无列名单权限） | a=季度人工 `gh secret list` 对账留痕；b=PROJECTS_STATE_PAT 权限实测后若具 admin 读面则机器对账——建议先 a 后实测定 b |
| 7 | **交接物 schema 兼容窗口**（§2.6 演进规则） | schema v1→v2 演进 | 旧版本读取兼容窗口一次裁定期，窗口外旧版本拒收——不做无限兼容；建议单 run 窗口（同批切换） |
| 8 | caps-gate 门归属（进 ruleset 时点） | foreman-wall-ci 恒跑面（两门口径 §0b） | caps-gate 施工落地后加进 ruleset required_status_checks（单源正道，不在代码养门表）；时点与门名大哥定 |

---

## 附A 锚清单与可解析断言

本稿与六件锚件引用的全部 file:line 锚（测试仓约 130 处＋引擎仓约 50 处）登记于机器可读清单 `tests/fixtures/wall-v3/design-contract.json`（`anchors` 数组：文件/行号/解析判据/采样窗口），由 `tests/test_wall_v3_design_contract.py` 逐锚断言可解析（文件在、行号不越界、锚定行内容含预期关键词）。代表性锚快照（全表以 fixture 为准）：`team.yml:7`（v2.7.0 注记）、`:202-204`（lead 包装调用区段）、`:599`（worker 裸跑 900s）、`:1390-1391`（validator 双置空）、`:2259-2282`（死因推断段）、`:4431`（PAT 单点）；`env-check.yml:82-86/155-163/194-200/238-240`（凭证面四区段）；`droid.yml:25`/`droid-probe.yml:13`/`probe6.yml:10`（件③新增 BYOM 锚）；`salvage_verdict.py:45-47`（D-2 封章＋adoptable）；引擎（main@460922c 基准）`module-capabilities.toml:574`、`ci.yml:439/:458`（--changes 接线步）、`run_lead.sh:282/:286`、`hardening_baseline.py:1`、`exception-point-inventory.md:23`。运行态锚排除：`memory/log/2026-11-27-sessions.md:586`（memory-core 运行态，非契约面，只作四问题①证据指针）。

**锚修正留痕**：底稿 failure-specs 附A 曾将 adoptable 语义行锚记为 `worker_salvage.py:47`，本稿总装实读裁决更正为 `salvage_verdict.py:45-47`（`final` is the D-2 seal 语义＋adoptable 判据；`worker_salvage.py:47` 实际是补卷产品清单行）——以本稿与 fixture 为准。
