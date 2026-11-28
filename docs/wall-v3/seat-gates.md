# 逐席位门清单＋对位表（seat-gates 底稿）

> 底稿 1/2（mission F2/seat-gates 产出；主设计稿 §2 素材）。本件定义领班制 7 席位的**能力授权面**：每席一张门清单（TOML 段样例，形制照抄引擎 M-CAP 12 键——MODULE_KEYS 实测）、与引擎 M-CAP 门清单的逐键对位表、工人席收进包装器设计。结构化交接物 schema 设计见姊妹底稿 `handoff-schemas.md`（§5 索引）。
>
> **真源声明**：引擎形制以 `docs/wall-v3/form-basis.md`（锚件 1）为准；测试仓现状行号以 `docs/wall-v3/as-is-capability-inventory.md`（锚件 2）为准——本件引用 team.yml 现状一律转引锚件 2，不直查 team.yml 重数行号。本件全部 file:line 锚经实读核实（2026-11-27 快照，测试仓 R58-D 收尾态）。
>
> **禁抄项**（form-basis §11，round-2 更新口径）：引擎墙未闭合缺口中仍在册的缺口态不抄入本件（`--changes` 判词不接 CI 的登记时点态已于引擎 main@460922c 上游闭合；NEW-1 governance 门现状＝enabled 在役执法、剩余真实缺口＝非 required status check 不阻断合并——禁止沿用过期 R-18 行「governance owner 门停用态」表述指称引擎现状）；本件所有门都是**须执法的门**，不允许纸面有门。引用引擎放行门口径一律按 R-29 已裁**两门**（quality-gate / substrate-gate-suite）。
>
> **版本口径**：本件属设计稿 v3.0 体系，作废 v2.7~v2.10 账面墙口径；现状 team.yml:7 标 v2.7.0、README 交付段另标 v2.9/v2.10 的三处漂移（锚件 2 §0）由 v3.0 统一收口。

---

## §0 席位名单与口径

**7 席**：领班 lead、工人 worker、验收 validator、改计划 replan、备料 prep、装配 assemble、写板 recorder。

- **写板席（recorder）**是目标态独立席位（任务书席位表含「写板」）。现状无独立 job，职能由两处承载：①validate 席 prompt 纪律（`team.yml:1515`，validator prompt 单源）；②prep 补卷器机器兜底（`team.yml:1223-1226`，salvage 接线）——口径见锚件 2 §0/§7。v3.0 把写板立为独立席位=对「纪律缺席无报警」（59 轮四问题④）的结构化收编。
- **二轮镜像口径**：worker2 / workers2-wall-merge / prep2 / validate2 / revalidate2 / revalidate2 是一轮对应席（worker / merge / prep / validate / revalidate）的镜像（锚件 2 §0）。**二轮席门清单按一轮对应席同构适用**，本件不重复出段；差异点（分支后缀 `-r2`、validate2 flips 翻案记账 `team.yml:3948`）随主设计稿总装入 §2 差异附录。
- **辅助面**：workers-wall-merge（`team.yml:851`）是无 droid 纯脚本合并 job，登记为工人席的墙出口合并面，不占席位名额；env-check（`team.yml:37`）是零号门（非席位），其门清单随主设计稿总装单列（五 secrets 全量入环境的收口归 F3 图外件清零）。
- **席位↔job 现状对位**（行号转引锚件 2 附表）：lead=`team.yml:52`、worker=`team.yml:503`（worker2=`:2697`）、prep=`team.yml:936`（prep2=`:3107`）、validate=`team.yml:1382`（revalidate=`:1779`、validate2=`:3618`、revalidate2=`:4010`）、replan=`team.yml:2141`、assemble=`team.yml:4389`。

**四要素↔键映射**（VAL-GATES-001 的「入口/出口/可用工具/写目标＋令牌 scope」落在键集上的位置）：

| 四要素 | 承载键 |
|---|---|
| 入口 | `entry` |
| 出口 | `events_produced`（issue/评论/墙 patch/事件）＋`artifacts`（制品与文件） |
| 可用工具 | `api`（脚本/符号面）＋`local_uses`（本地可复用件，含会话工具白名单注入源） |
| 写目标 | `artifacts`（制品路径面，含工作区写目标）＋`events_produced`（GitHub 写面） |
| 令牌 scope | `authorization.token_scope`（对位引擎 v5 authorization 三面之一） |

---

## §1 形制总则（照抄引擎 M-CAP 键集，一次定死）

**1.1 双登记真源、授权与结局分立**。引擎形制＝双 TOML 登记真源＋守卫零硬编码（form-basis 要点 1，原物锚 `docs/specs/modules.toml:19`、`docs/specs/module-capabilities.toml:77`、`scripts/check_module_wall.py:12`）。领班域对位：

| 登记文件 | 面 | 现状载体（对照） |
|---|---|---|
| `foreman-caps.v1.toml`（**新增，施工时落 repo 根**） | **授权面**：席位能做什么（本件定义） | 现状不存在——59 轮「无授权能力」的 schema 层根因（锚件 2 §9.1：`schemas/foreman-run.v1.schema.json:146-157` 只记结局） |
| `schemas/foreman-run.v1.schema.json` | **结局面**：席位做了什么（结局/产物/死因事实） | 现状在树（session_outcome 枚举 `:65`、by-pid 三映射 `:146-157`、human_stop `:33`） |

ForemanRun 墌字段（结算/审计用）与门清单分离，一个记结局一个记授权——两文件各自 schema 一次定死，互不越界。键集清单含引擎 12 键全集（verification 在列——各席 `[seat.<id>.verification]` 段即其承载；round-2 版键块漏列该键系笔误，本批补正，与 §1.2 键集口径一致）。

**1.2 键集一次定死**（form-basis 要点 2＋3）。每席位一段 `[seat.<id>]`，键集＝引擎 M-CAP **12 键**照抄（MODULE_KEYS 实测：entry/api/guard_test/events_consumed/events_produced/artifacts/state_reads/local_uses/probes/callers/authorization/verification，引擎仓 `tests/test_module_capabilities_contract.py:55-68`；「十键＋三锚」「协作五键＋v5 三键」为历史别名，均指此 12 键集）＋领班域扩展一键：

```
entry / api / guard_test / events_consumed / events_produced / artifacts /
state_reads / local_uses / probes / callers / authorization / verification / budgets
```

- `budgets` 是**唯一的域扩展键**（引擎键集之外）：承载会话墙预算与 job 墙预算，是 VAL-GATES-004「预算从门清单读」的承载面。扩展声明在此一次定死；增删键必须同批改契约测试（`tests/test_foreman_caps_contract.py`，目标态新增），禁止守卫或登记单边漂移（形制要点 3，铁律原文对位 `docs/specs/key-registry.toml:14-16`）。
- 全部值带 file:line 锚；锚漂移即红（caps-gate anchor lint，对位引擎 `[anchor]` 面，形制要点 1）。
- `api` 双形态照抄引擎：str＝席位级整面；`{path: [符号]}`＝符号级（对位引擎 `module-capabilities.toml:588-595` M-CAP api 双形态原物）。

**1.3 判词只增不改＋退出码三态**（form-basis 要点 4，判词常量对位 `scripts/check_module_wall.py:90-113`）。caps-gate 守卫判词枚举（初版一次定死，只增不改）：

| 判词 | 语义 |
|---|---|
| `unregistered-tool-call` | 会话调用门清单外工具 |
| `out-of-scope-write` | 写目标越 artifacts 登记面（F-1 类守卫的判词化） |
| `token-scope-violation` | 使用 authorization.token_scope 外令牌/权限 |
| `undeclared-artifact` | 产出未登记制品 |
| `undeclared-event` | 消费/产出未登记事件（issue/评论/墙 patch 名单外） |
| `undeclared-state-read` | 读门清单外状态树 |
| `narrative-without-evidence` | 因果结论无证据对象佐证（handoff-schemas §6 执法） |
| `evidence-construct-violation` | 非核查环节构造证据对象（handoff-schemas §6） |
| `caps-schema-drift` | 门清单 schema 键集/词表漂移且未同批改契约测试 |
| `mixed-registry-change` | 改登记面未带 `wall-registry-change: true` 声明（照抄引擎，常量对位 `scripts/check_module_wall.py:131`） |

退出码三态：0 clean / 1 violations / 2 环境错误（fail-loud 永不静默绿，对位 `scripts/check_module_wall.py:13-14`）。

**1.4 CI 恒跑接线锁**（form-basis 要点 5）。caps-gate 接线进 foreman-wall-ci 恒跑（push 与 PR 两腿同面，零 if、零 continue-on-error）；「守卫确实接在 CI 上」由接线锁契约测试断言。**任何判词不落 CI＝显式未闭合，不冒充已执法**（form-basis §11.1 义务条款）。

**1.5 CI 接线缺口与登记面升级闸（两事分称，round-3 术语裁决）**：全稿两处语境用词定死——**「接线缺口」**＝守卫判词存在但未接 CI 恒跑的形态（引擎 NEW-2 登记时点态，已上游闭合，禁复现；本件 §1.4 语境）；**「升级闸违例」**＝改登记面未带声明行的判词红（`mixed-registry-change`，本件 §1.6 语境）——两者不再混称「接线锁」。

**1.6 登记面升级闸＋保护面**（form-basis 要点 7）。改 `foreman-caps.v1.toml`＋caps-gate 守卫本体的变更集必须带 `wall-registry-change: true` 声明行，否则 `mixed-registry-change` 红；登记面路径列入受保护面。**与引擎的差异（禁抄项义务）**：升级闸判词必须接 CI 恒跑、保护面必须是运行时执法——引擎 NEW-1 现状＝enabled 在役执法、剩余真实缺口＝governance 门非 required status check 不阻断合并（不阻断≠停用，现状口径照 form-basis §11.1）；NEW-2 已上游闭合。两缺口态均不得在本件复现。

**1.7 执法在体外**（form-basis §10 补遗 b）。任何门的执法通道不依赖被管进程配合：监督者写哨兵→SIGTERM 进程组→宽限→SIGKILL 进程组（引擎终止序列照抄，原物锚 `src/infra_core/engine/droid_review/run_lead.sh:282`（`kill -TERM "-$exec_pid"` 负 PID 组信号）与 `:286`（`kill -KILL` 同形态））。哨兵在案＝该席产物不采信（强制失败优先，对位 `run_lead.sh:10`）。

**1.8 放行门单源 ruleset**（form-basis 要点 6；原 §1.5，round-3 起顺延——§1.5 改记术语裁决）。合并放行门唯一单源＝GitHub ruleset required_status_checks，代码不养第二套门表常量；引用引擎口径一律两门（quality-gate / substrate-gate-suite，R-29 已裁）。caps-gate 进门走同一正道：加进 ruleset，不在代码养门表。

---

## §2 七席位门清单（TOML 段样例）

> 以下各段是 `foreman-caps.v1.toml` 的目标态样例（**设计稿底稿，非施工**）。段内 file:line 锚＝现状锚（锚件 2 口径）；标注「目标态」的载体施工时新增。每段末尾的 **default-deny 声明**逐席成立：清单之外不存在。

### 2.1 领班席（lead）

```toml
# foreman-caps.v1.toml —— [seat.lead]
[seat.lead]
entry = [
    ".github/workflows/team.yml:52（lead job；needs.env-check.outputs.foreman_ok=='true' 门放行）",
    "scripts/team/run_droid_session.py（会话唯一入口，零旁路；旁路=unregistered-tool-call）",
]
api = [
    "scripts/team.lead_plan_segments.stitch_plan_file（分段卡缝合，lead_plan_segments.py:161）",
    "scripts/team.run_droid_session.run_session（包装器会话执行体，含 prompt 组装；独立 build_lead_prompt 载体施工时新建——prompt 组装面现行住 run_droid_session.py）",
    "scripts/team.foreman_run_patch.main（墙 patch 上墙，FOREMAN_RUN_PATCH=1 面；wall_patch 独立符号施工时新建或迁入）",
    { "scripts/team/run_droid_session.py" = ["main", "run_session"] },
]
guard_test = [
    "tests/test_foreman_caps_contract.py（目标态新增）",
    "tests/test_wall_v3_design_contract.py",
]
events_consumed = { wall_outputs = ["env-check.foreman_ok（team.yml:52）", "dup 去重面"], issue_comment = ["@team-droid 点名（team.yml:31-34 触发面）"] }
events_produced = { wall_patch = ["budgets.session_outcome", "plan（lead-plan-slice）", "plan_dispatch"], issues = ["[计划] 计划单", "[工序] 子单", "派单评论（post_comment_hard --wall-patch plan_dispatch）"] }
artifacts = [
    { name = "lead-plan-segments", op = "workspace-write", path = "team/lead-plan-segments/*.json", consumers = ["worker", "replan"], note = "写目标唯一工作区面；越界=out-of-scope-write" },
    { name = "team-plan-json", op = "upload", path = "team/team-plan.json", consumers = ["worker", "replan", "assemble"] },
]
state_reads = ["team/foreman-run.json（墙 artifact 下载面）"]
local_uses = ["scripts/team/run_droid_session.py（包装器，FOREMAN_RUN_PATCH=1）"]
probes = "caps-gate 负向三探针：会话写 team/lead-plan-segments/ 外文件->out-of-scope-write 必红；令牌越 token_scope->必红；未登记工具->必红（现状缺口：lead 会话写无机器 F-1 类守卫，锚件 2 §1——本门即补齐该缺口的执法设计；必死样本=SL-4b＋SL-10a，acceptance-line-map §2.4b/§2.10）＋接线锁探针：包装器启动前置自检——会话配置生成时读门清单，键缺失（如 [seat.lead] 段缺席或 budgets 键不齐）即拒启（fail-loud exit 2，永不禁用默认放行）；必死样本=SL-13a（acceptance-line-map §2.13）"
callers = { internal = ["workers-wall-merge（读 lead.outputs.processes，team.yml:851）"], external = ["无（领班席零仓外消费）"], workflow = [".github/workflows/team.yml:52"] }

[seat.lead.authorization]
governance_face = "受保护路径面（docs/specs 类登记面与 .github/workflows/** 不可写；写=治理行为，走 wall-registry-change 通道）"
audit_face = "caps-gate 全仓审计＋foreman-wall-ci 恒跑（接线锁契约测试在树）"
token_scope = "GH_TOKEN=github.token（issues: write / PR: read / contents: read）＋BYOM 三件＋FACTORY_API_KEY（会话模型面）。现状锚：team.yml:120（WORKER_CI_KEY）、:157（FACTORY_API_KEY）、:79/:241（GH_TOKEN=github.token）。I8-B 假 PAT 夹具分支（:419 假值变量、:429-431 标题命中换 token）不在本门清单内=多出的门，默认删（收编方式见对位表 §3.4 多出的门总表与 F3）"

[seat.lead.budgets]
droid_wall_sec = 600
job_wall_min = 15
# 软超时公式基座＝budgets 键的 job timeout（job_wall_min 推成秒），非 droid 墙：
# 引擎口径 run_lead.sh:6「workflow 按 timeout−400s 公式推导注入」的 timeout 即 job
# timeout（droid-review-lead.yml:35-37：margin 400s 保证哨兵先于 GitHub 硬杀）。
# 本键对平引擎口径：软超时 = job_timeout − 400 = 900 − 400 = 500s（lead job 15min）；
# droid 墙 600s 是包装器会话预算（T0 计时面），不进公式。
soft_timeout_formula = "job_timeout_sec - 400（基座=本键 job_wall_min*60；引擎 run_lead.sh:6/droid-review-lead.yml:35-37 口径）"
soft_timeout_sec = 500

[seat.lead.verification]
contract_tests = ["tests/test_foreman_caps_contract.py（目标态新增）", "tests/test_wall_v3_design_contract.py"]
probes = "caps-gate 负向探针（见 probes 键，必死样本=SL-4b＋SL-10a，acceptance-line-map §2.4b/§2.10）＋接线锁（caps-gate 步在 foreman-wall-ci 恒跑断言；必死样本=SL-13a，acceptance-line-map §2.13）"
probe_notes = "lead 现状经包装器（team.yml:203-204）——预算/接线已合规；本席 v3.0 的主收口是写目标机器守卫（workspace-write 面 F-1 化）与 token_scope 收窄"
```

**default-deny 声明（lead）**：本席可用工具、可写目标、可发事件、可读状态、可持令牌**以本段清单为全集，清单之外不存在**。现状「repo 工作区任意文件写（无机器守卫，仅 prompt 纪律）」（锚件 2 §1）不在清单内，即多出的门——按 §3.4 默认删。二轮镜像席无。

### 2.2 工人席（worker，矩阵 max-parallel 3；镜像 worker2）

```toml
# foreman-caps.v1.toml —— [seat.worker]
[seat.worker]
entry = [
    ".github/workflows/team.yml:503（worker job；needs.lead.outputs.processes 矩阵，每卡一会话）",
    "scripts/team/run_droid_session.py --role worker（目标态唯一会话入口；现状裸跑 team.yml:599 于 §4 废止）",
]
api = [
    "scripts/team.worker_prompt_template（prompt 单源）",
    "scripts/team.write_worker_delta",
    { "scripts/team/write_worker_delta.py" = ["classify_session_outcome", "main"] },
]
guard_test = [
    "tests/test_foreman_caps_contract.py（目标态新增）",
    "tests/test_worker_wall_contract.py（工人墙守卫测试族——施工时新建并归集 F-1/守卫面负例；现树对应面散在 tests/test_foreman_wall_contract.py 等在树族，不以其现存口径引用）",
]
events_consumed = { wall_outputs = ["lead.processes 矩阵"] }
events_produced = { wall_patch = ["workers 切片（session_outcome/droid_exit_code/stream_tail_marker by-pid）", "handoff 评论（母单＋子单）"], issues = ["handoff 评论"], git = ["分支 team/issue-N/run-R/<pid> push"] }
artifacts = [
    { name = "card-deliverables", op = "workspace-write", path = "卡面 allowed 集合（F-1 载体，team.yml:731 reset --soft 后逐文件比对）", consumers = ["prep", "validate"], note = "写目标唯一工作区面" },
    { name = "handoff-md", op = "workspace-write", path = "team/handoffs/<pid>.md", consumers = ["prep", "validate", "recorder"] },
    { name = "status-json", op = "workspace-write", path = "team/status/<pid>.json", consumers = ["prep", "validate"] },
    { name = "worker-delta", op = "workspace-write", path = "worker-delta.json（write_worker_delta.py，team.yml:836 上墙）", consumers = ["workers-wall-merge"] },
]
state_reads = ["team/foreman-run.json（墙）", "卡面 checks 脚本面"]
local_uses = ["scripts/team/run_droid_session.py（目标态包装器，零旁路）"]
probes = "F-1 越界写守卫（现行载体 team.yml:712-743 区段，越界即拒；必死样本=SL-3b，acceptance-line-map §2.4）＋caps-gate 三探针（未登记工具/token 越界/裸跑 droid exec=unregistered-tool-call 必红；必死样本=SL-10a 族＋SL-4 族＋SL-3/RS-2 裸跑载体，acceptance-line-map §2.10/§2.4b/§2.3+§5）"
callers = { internal = ["workers-wall-merge（delta 并集，team.yml:885 merge_worker_deltas）", "prep（分支 merge 面）"], external = ["无"], workflow = [".github/workflows/team.yml:503"] }

[seat.worker.authorization]
governance_face = "受保护路径面（.github/workflows/**、schemas/**、scripts/team/ 守卫本体不可写；越界=F-1 拒＋out-of-scope-write 双红）"
audit_face = "caps-gate 全仓审计＋delta 上墙机器分类（write_worker_delta.py 死因三字段）"
token_scope = "会话步零 GitHub 令牌（现状即最小，锚件 2 §2）；commit 步 GH_TOKEN=github.token（contents: write，push 分支用，team.yml:710）＋BYOM 三件＋FACTORY_API_KEY（team.yml:531/:568，会话模型面）"

[seat.worker.budgets]
droid_wall_sec = 900
job_wall_min = 25
# 软超时公式基座＝budgets 键的 job timeout（job_wall_min=25 → 1500s）：
# 软超时 = job_timeout_sec − 400 = 1100s（引擎 run_lead.sh:6「timeout−400s」的
# timeout 即 job timeout，droid-review-lead.yml:35-37 margin 语义：哨兵先于
# GitHub 硬杀）。droid 墙 900s 是包装器会话预算（T0 计时面），不进公式。
soft_timeout_formula = "job_timeout_sec - 400（基座=本键 job_wall_min*60；引擎口径）"
soft_timeout_sec = 1100
verify_step_timeout_sec = 300
note = "预算唯一来源=本段（§4 接线设计）；现状墙上账面值 foreman_run_lib.py:53-54 区段与裸跑硬编码 900s 数值偶合而不接线，v3.0 由本键取代两处"

[seat.worker.verification]
contract_tests = ["tests/test_foreman_caps_contract.py（目标态新增）"]
probes = "caps-gate 裸跑探针：workflow 文本出现 BARE_DROID 形态（timeout…droid exec 不经包装器）即红——lint_workflow_budgets.py:43-51 的 worker/900s 豁免分支废止后，本探针与 budgets lint 同判词双载体；必死样本=SL-3/RS-2（acceptance-line-map §2.3/§5，工人席禁跑 probe 的独立载体行；BARE_DROID 形态探针判词面=SL-3＋caps-gate 载体，互锁表 RS-2 行同口径）"
probe_notes = "worker 是 59 轮四问题②的所在席：900s 执法与会话同体（45B 实证孤儿子进程拖到 25m job 墙）——收口=§4 包装器＋体外执法"
```

**default-deny 声明（worker）**：本席会话可写文件以卡面 allowed 集合＋handoffs/status 三路径为全集，可调工具以包装器白名单为全集，可持令牌以 token_scope 为全集——**清单之外不存在**。现状裸跑形态（`team.yml:599`；worker2 同款 `:2784`）不是本席的门，是待废止的越权形态（§4）。verify 步全仓 subprocess 无超时面（锚件 2 §2）收口为卡面 checks 白名单＋300s 步超时（budgets.verify_step_timeout_sec）。

### 2.3 备料席（prep；镜像 prep2）

```toml
# foreman-caps.v1.toml —— [seat.prep]
[seat.prep]
entry = [
    ".github/workflows/team.yml:936（prep job；workers-wall-merge.outputs.prep_should_run=='true'，I1 读墙 completed_pids）",
    "纯脚本席：无 droid 会话（validator never merges 纪律）",
]
api = [
    "scripts/team.worker_salvage（补卷器）",
    "scripts/team.merge_worker_deltas（delta 并集面，merge_worker_deltas.py）——候选分支合成面（team.yml:1093 git merge --no-ff 步）现状内嵌 prep job heredoc；merge_worker_branches 独立声明体施工时新建或由该步抽取",
    { "scripts/team/worker_salvage.py" = ["main"], note = "守卫四条件机器判定 fail-closed（:13 docstring：merged true＋F-1 clean＋checks 全绿且 marker 按内容判红＋会话异常终止）；salvage_pack 独立符号施工时随声明体重构（现行聚合在 worker_salvage.py:430 salvage_packs）" },
]
guard_test = ["tests/test_worker_salvage_*.py（在树测试族）", "tests/test_foreman_caps_contract.py（目标态新增）"]
events_consumed = { wall_outputs = ["prep_should_run（team.yml:860）", "workers completed_pids（team.yml:885）"] }
events_produced = { wall_patch = ["prep 切片", "salvage 记账（salvaged_from_machine 标记）"], issues = ["备料报告评论（母单＋计划单）"], git = ["候选分支 team/issue-N/candidate-R push"] }
artifacts = [
    { name = "candidate-branch", op = "git-push", path = "team/issue-N/candidate-R", consumers = ["validate"] },
    { name = "evidence-pack", op = "upload", path = "evidence.tar.gz（manifest sha256 权威）", consumers = ["validate", "revalidate", "validate2", "revalidate2"] },
    { name = "salvage-evidence", op = "workspace-write", path = "packs/<id>/（补卷器机器写，只补缺失件、不碰 worker 已写件）", consumers = ["validate"] },
]
state_reads = ["team/foreman-run.json（墙）", "worker 分支树"]
local_uses = ["git（merge/ls-remote）", "pytest（全量 600s 超时）", "卡面 checks 复跑（300s 超时）"]
probes = "原子 probe 逐条登记（round-3 拆原子）：①补卷守卫四条件负例（任一不满足=不补卷，载体=SL-5）；②caps-gate droid 会话禁入探针：prep 出现 droid 会话=unregistered-tool-call 必红（纯脚本席禁 droid，载体=SL-13f，acceptance-line-map §2.13 SL-13f——零 droid 席探针独立载体，prep 面）；③候选分支越权写探针（载体=SL-13b，round-2 已配行）"
callers = { internal = ["validate（needs.prep.result）"], external = ["无"], workflow = [".github/workflows/team.yml:936"] }

[seat.prep.authorization]
governance_face = "受保护路径面（同全席基线）"
audit_face = "caps-gate 审计＋evidence manifest sha256 全链防篡改"
token_scope = "GH_TOKEN=github.token（报告/merge 面，team.yml:1321）；无 droid、无 BYOM（锚件 2 §5）"

[seat.prep.budgets]
pytest_timeout_sec = 600
checks_timeout_sec = 300
job_wall_min = 20

[seat.prep.verification]
contract_tests = ["tests/test_worker_salvage_*.py", "tests/test_foreman_caps_contract.py（目标态新增）"]
probes = "补卷守卫四条件逐条负例（在树；必死样本=SL-5，acceptance-line-map §2.5）＋候选分支越权写探针：非 prep 席（worker 会话步/lead 步/assemble 步）push `team/issue-N/candidate-R` 形态即 F 类守卫红（候选分支 git-push 权只登记在本席 artifacts 面；未登记者写入=caps-gate `undeclared-artifact`/`out-of-scope-write` 判词红）；必死样本=SL-13b（acceptance-line-map §2.13）"
probe_notes = "prep 是补卷器（根治第 1 层）与 evidence manifest 防篡改的承载席；注意规格明文：补卷覆盖面 != 中性归因覆盖面（worker_salvage.py docstring）"
```

**default-deny 声明（prep）**：本席零 droid 会话、零 BYOM；可写面＝候选分支＋补卷器 packs 缺失件；**清单之外不存在**。

### 2.4 验收席（validator；镜像 validate2、变体 revalidate）

```toml
# foreman-caps.v1.toml —— [seat.validator]
[seat.validator]
entry = [
    ".github/workflows/team.yml:1382（validate job；needs.prep.result=='success'；revalidate 变体 :1779 哨兵 fail-closed 拒二次）",
    "scripts/team/run_droid_session.py --role validator（team.yml:1534-1535）",
]
api = [
    "scripts/team.validator_prompt_template（prompt 单源，team.yml:1515）",
    "scripts/team.salvage_verdict（recorder 逐件落盘工具）",
    "scripts/team.adopt_verdict（墙采认面）",
    { "scripts/team/salvage_verdict.py" = ["record_verdict", "read_salvage", "salvage_verdict"] },
]
guard_test = ["tests/test_salvage_verdict*.py（在树）", "tests/test_foreman_caps_contract.py（目标态新增）"]
events_consumed = { wall_outputs = ["prep 切片", "workers by-pid 死因三映射"], evidence = ["evidence.tar.gz（manifest sha 门）"] }
events_produced = { wall_patch = ["validation 切片（run_adopt_step.py 采认，team.yml:1721）"], files = ["verdict-partial.json -> verdict-droid.json/md -> verdict.json/md"] }
artifacts = [
    { name = "verdict-partial", op = "workspace-write", path = "work/verdict-partial.json（salvage_verdict.py:18 PARTIAL_NAME）", consumers = ["recorder", "replan"] },
    { name = "verdict-final", op = "workspace-write", path = "verdict-droid.json / verdict-droid.md", consumers = ["assemble", "replan"] },
    { name = "evidence-ref-objects", op = "workspace-write", path = "verdict 内 evidence 对象（构造权单源，handoff-schemas §6）", consumers = ["replan", "lead", "assemble"] },
]
state_reads = ["packs/<id>/（证据包，只读）", "team/foreman-run.json（墙）"]
local_uses = ["scripts/team/run_droid_session.py（包装器）", "recorder 工具（salvage_verdict CLI）"]
probes = "会话可执行任意命令但零 GitHub 写权（双 token 显式置空）＋caps-gate：validator 出现 GH 写调用=token-scope-violation 必红（必死样本=SL-4 族越权令牌注入，acceptance-line-map §2.4b）；证据防篡改=事后 manifest sha 逐文件复验（必死样本=SL-13c 半套/晚期写翻动变体同面——verdict 粘滞注入即 tamper 面，acceptance-line-map §2.13）"
callers = { internal = ["replan（should_replan 投影输入）", "assemble（墙 validation 切片）", "revalidate（should_revalidate）"], external = ["无"], workflow = [".github/workflows/team.yml:1382"] }

[seat.validator.authorization]
governance_face = "受保护路径面（同全席基线）＋证据包不可变面（judge only from the evidence，validator prompt 单源 :101 行内纪律）"
audit_face = "caps-gate 审计＋adopt 采认链（fail-closed pick）"
token_scope = "**零 GitHub 令牌**：job 级与步级 GITHUB_TOKEN:\"\"/GH_TOKEN:\"\" 双显式置空（team.yml:1390-1391/:1502-1503）＋BYOM 三件＋FACTORY_API_KEY（team.yml:1463/:1501，会话模型面）。全链唯一零 GitHub 权限席"

[seat.validator.budgets]
droid_wall_sec = 480
adopt_reserve_sec = 120
job_wall_min = 15
# 软超时公式基座＝budgets 键的 job timeout（job_wall_min=15 → 900s）：
# 软超时 = job_timeout_sec − 400 = 500s。基座对平现状 workflow job envelope
# （team.yml:1387 timeout-minutes: 15，与 lead/replan 同 15m 档）；口径同 lead/worker
# 注释（引擎 run_lead.sh:6「timeout−400s」的 timeout 即 job timeout，
# droid-review-lead.yml:35-37 margin 语义：哨兵先于 GitHub 硬杀）。
# 预算四键实名＋480/500 对偶（无「会话总预算键」面）：480（droid_wall_sec，
# 包装器第一道墙——会话 T0 计时面，只杀 droid 会话进程组）vs 500（soft_timeout_sec，
# 体外监督者的外层哨兵线——job 预算口径，含 adopt 储备 adopt_reserve_sec=120 与
# 收尾余量；job 墙 job_wall_min=15 是公式基座）。两条墙各守一层，禁止混同（对位
# budget_resolve.py:57-59 注释纪律：ForemanRun 会话切片与 GitHub job envelope
# 两个口径不得互相冒充）。
soft_timeout_formula = "job_timeout_sec - 400（基座=本键 job_wall_min*60；引擎口径）"
soft_timeout_sec = 500

[seat.validator.verification]
contract_tests = ["tests/test_salvage_verdict*.py", "tests/test_foreman_caps_contract.py（目标态新增）"]
probes = "verdict schema 执法负例（枚举外值/无证据引用被拒，handoff-schemas §8；必死样本=SL-2＋SL-9，acceptance-line-map §2.2/§2.9）＋D-2 封章粘滞负例：verdict 半套注入（final=true 章在而部分 judged[].evidence_refs 为空/被晚期写翻动 partial 文件）->封章拒过（sealed 粘性保证 final 章不被晚期写翻掉，salvage_verdict.py:93-94；半套不达 adoptable 判据 adopt 拒采，`salvage_verdict.py:45-47`）——必死样本=SL-13c（acceptance-line-map §2.13）"
probe_notes = "validator 同时是证据对象构造权单源席（handoff-schemas §6）与 recorder 职能承载点①——v3.0 把 recorder 立为独立席（§2.7）后，本席保留核查与构造权，落盘执行面移交 recorder"
```

**default-deny 声明（validator）**：本席零 GitHub 写权；可写面＝verdict 系列＋证据对象；可读面＝证据包与墙；**清单之外不存在**。

### 2.5 改计划席（replan）

```toml
# foreman-caps.v1.toml —— [seat.replan]
[seat.replan]
entry = [
    ".github/workflows/team.yml:2141（replan job；墙 replan_gate.should_replan 投影）",
    "scripts/team/run_droid_session.py --role replan（team.yml:2405-2406）",
]
api = [
    "scripts/team.attribution_reason（归因面，死因叙事按墙面事实分支）",
    "scripts/team.plan_v2_validator（落单步机器校验：覆盖集、claim 不相交、受保护路径——施工时新建独立声明体；校验逻辑现状内嵌 team.yml:2420『Validate plan v2 and file the revision』步 heredoc，抽独立模块即本键对位物）",
    { "scripts/team/attribution_reason.py" = ["blocked_reason", "blocked_report_line", "neutral_attribution"] },
]
guard_test = ["tests/test_replan_*.py（在树族）", "tests/test_foreman_caps_contract.py（目标态新增）"]
events_consumed = { wall_outputs = ["replan_gate.should_replan", "plan 切片", "verdict", "workers by-pid 死因三映射"], evidence = ["verdict 内 evidence 对象（只读引用，无构造权）"] }
events_produced = { wall_patch = ["replan_notice_*"], issues = ["[工序] v2 新 sub-issue＋旧子单关闭（not planned）", "replan 通知评论"], files = ["team-plan-v2.json"] }
artifacts = [
    { name = "plan-v2", op = "workspace-write", path = "team-plan-v2.json（changes 数组；落单步机器校验后生效）", consumers = ["worker2", "assemble"] },
]
state_reads = ["team/foreman-run.json（墙）", "verdict.json（只读）", "evidence（只读）"]
local_uses = ["scripts/team/run_droid_session.py（包装器）"]
probes = "caps-gate：replan 输出因果结论无 evidence_ref= narrative-without-evidence 必红（59 轮四问题①的执法门，handoff-schemas §2/§9；必死样本=SL-3b'，acceptance-line-map §2.4）；「F-1 检查拒绝」推断文案出现即红（钉子反转，handoff-schemas §9.2；必死样本同 SL-3b' 三负例）"
callers = { internal = ["worker2（plan-v2 矩阵）", "assemble（final 卡）"], external = ["无"], workflow = [".github/workflows/team.yml:2141"] }

[seat.replan.authorization]
governance_face = "受保护路径面（同全席基线）"
audit_face = "caps-gate 审计＋死因叙事证据链审计（narrative-without-evidence 判词）"
token_scope = "会话步零 GitHub 令牌（GITHUB_TOKEN:\"\"/GH_TOKEN:\"\"，team.yml:2210-2211）＋BYOM 三件＋FACTORY_API_KEY（:2178/:2209）；落单步 GH_TOKEN=github.token（:2423）——**两会话面拆门**：v2 把「无 token 会话面」与「落单 GitHub 写面」拆为两个子门分别授权（现状同 job 混合=多出的门，§3.4 收口）"

[seat.replan.budgets]
droid_wall_sec = 480
job_wall_min = 15
# 软超时基座=job timeout（900s−400=500s；口径同 lead/worker 注释）。
soft_timeout_formula = "job_timeout_sec - 400（基座=本键 job_wall_min*60；引擎口径）"
soft_timeout_sec = 500

[seat.replan.verification]
contract_tests = ["tests/test_replan_*.py", "tests/test_foreman_caps_contract.py（目标态新增）"]
probes = "死因叙事三负例：①无机器记录佐证的 F-1 推断文案->红；②evidence_ref 指向不存在锚->红；③blocked_cause 枚举外值->红（handoff-schemas §2 违约表；必死样本=SL-3b'，acceptance-line-map §2.4——replan 面伪造死因桩，同席同载体）"
probe_notes = "replan 是 59 轮四问题①所在席：死因叙事含脚本内置推断（分支缺席->F-1 检查拒绝，team.yml:2259-2282，文案落 :2278-2279）且被 tests/test_replan_context_and_skipped_outcome_r53c.py:190-206 逐字钉住——v3.0 反转该钉子（handoff-schemas §9.2），死因只能挂证据对象或取「未明」"
```

**default-deny 声明（replan）**：本席可写面＝team-plan-v2.json＋落单步 GitHub 写（拆门后独立授权）；可读面＝墙/verdict/证据；**无证据不出因果结论——清单之外不存在，「未明」是唯一合法缺省**。

### 2.6 装配席（assemble）

```toml
# foreman-caps.v1.toml —— [seat.assemble]
[seat.assemble]
entry = [
    ".github/workflows/team.yml:4389（assemble job；always()，lead 非 skipped 且非 duplicate）",
    "纯脚本席：无 droid 会话",
]
api = [
    "scripts/team.pick_verdict_from_wall（墙权威 pick，fail-closed，team.yml:4420）",
    "scripts/team.project_state_write（板面写，PAT，:4441）",
    "scripts/team.assemble_chain_facts（chain_facts 收口，:4636）",
]
guard_test = ["tests/test_assemble_*.py（在树族）", "tests/test_foreman_caps_contract.py（目标态新增）"]
events_consumed = { wall_outputs = ["validation 切片", "closeout 输入", "human_stop（schema :33）"] }
events_produced = { wall_patch = ["final_status_card（post_comment_hard --wall-patch）", "chain_facts"], issues = ["最终状态卡评论", "子单/计划单关闭"], projects = ["Projects #33 Status 写（PAT 单点）"], pr = ["PR create（pass 时）"] }
artifacts = [
    { name = "board-state", op = "projects-write", path = "Projects #33 Status 字段（project_state_write.py，PAT 单点 team.yml:4431）", consumers = ["human"], note = "全链唯一板面写点；终态一致性机制归主设计稿 §图外件（Item closed 翻板，F3）" },
    { name = "final-pr", op = "git-push", path = "PR create（github.token，:4448）", consumers = ["human"] },
    { name = "final-status-card", op = "issue-comment", path = "母单评论", consumers = ["human"] },
]
state_reads = ["team/foreman-run.json（墙，pick 权威源）"]
local_uses = ["git（PR 面）", "gh（issue close/comment，:4659）"]
probes = "原子 probe 逐条登记（round-3 拆原子，一子句一 probe 一载体）：①droid 会话禁入探针：assemble 出现 droid 会话=unregistered-tool-call 必红；②板面写单点性探针：板面写非 project_state_write 单点=token-scope-violation 必红（必死样本=SL-14，acceptance-line-map §2.13——覆盖非 project_state_write 写路径注入：gh project 直写/其他 automation 通道）；③human_stop 消费探针：human_stop 在墙（schema :33）而 assemble 收口分支未走提前停路径、照常 pick/写板->red（现状缺口：human_stop 已上墙且机器面有消费（墙 W6 判定 foreman_run_lib.py:232、replan 重试面 adopt_verdict.py:580-583），但 assemble 收口分支的提前停消费缺席——锚件 2 §6/§9 风险 13 现状句按此精化——本探针即补齐该缺口；必死样本=SL-13d，acceptance-line-map §2.13）。SL-13d 会话注入子面（droid 会话禁入的收口步桩化形态）：acceptance-line-map §2.13 SL-13d 的注入步将 fake-droid 桩以 assemble 收口步会话形态注入（桩走 droid exec 调用面冒充收口执行体），断言未消费 human_stop 的收口路径被禁入探针点名红＋消费正对照零板面写——会话注入设计锚 round-2 版 seat-gates probes 子句（git show 888fca0:docs/wall-v3/seat-gates.md :369 原文——888fca0 时该子句在 :369，round-4 验证登记）与 acceptance-line-map §2.13 注入行"
callers = { internal = ["无下游席（链尾）"], external = ["human（状态卡/板面消费者）"], workflow = [".github/workflows/team.yml:4389"] }

[seat.assemble.authorization]
governance_face = "受保护路径面＋板面终态一致性义务（关单翻板面归 F3 清零，repo 侧配合板侧 Disable/终态选项改造）"
audit_face = "caps-gate 审计＋PAT 时间线审计（第 50 轮口径，docs/W-14-写板活验通过判据-修订.md）"
token_scope = "PROJECTS_STATE_PAT（全链唯一使用点，team.yml:4431，板面专用）＋GH_TOKEN=github.token（:4448/:4659，PR/issue 面）——两令牌按写目标分面，禁混用（现状已分离，v3.0 登记并执法）"

[seat.assemble.budgets]
job_wall_min = 10

[seat.assemble.verification]
contract_tests = ["tests/test_assemble_*.py", "tests/test_foreman_caps_contract.py（目标态新增）"]
probes = "墙权威 pick fail-closed 负例（缺 validation 切片=不写板；必死样本同 SL-13e 缺切片断言在树，acceptance-line-map §2.13）＋板面写单点性探针（必死样本=SL-14，acceptance-line-map §2.13——板面写单点性注入面归 SL-14，见 §2.6 ②的映射）＋pick fail-closed 变体探针：墙 validation 切片存在但整片不可采认（adoptable=false：全部 partial 未封章）->pick 必拒=零板面写、零 PR、零关单（fail-closed 全链收口；必死样本=SL-13e，acceptance-line-map §2.13）"
probe_notes = "assemble 是全链最强 GitHub 写面集中席（PAT 写板＋PR create＋issue close＋评论，锚件 2 §6）——v3.0 不削减其职能写面，但逐门登记＋令牌分面＋human_stop 消费门补齐"
```

**default-deny 声明（assemble）**：本席零 droid 会话；GitHub 写面＝板面 PAT 单点＋PR create＋issue 关闭/评论三登记面；**清单之外不存在**。

### 2.7 写板席（recorder——目标态独立席）

```toml
# foreman-caps.v1.toml —— [seat.recorder]
# 现状无独立 job（锚件 2 §0/§7）；v3.0 立席=把「逐件落盘纪律」从 prompt 文字
# 升级为门清单授权＋机器执法（59 轮四问题④的结构化收编）。
[seat.recorder]
entry = [
    "validator/worker 会话内的 recorder 工具调用面（目标态：run_droid_session 包装器按 [seat.recorder] 授权向会话注入 recorder 工具）",
    "scripts/team.salvage_verdict（validator 面承载，team.yml:1515 现状）",
    "scripts/team.worker_salvage（prep 机器兜底面，team.yml:1223-1226 现状）",
]
api = [
    { "scripts/team/salvage_verdict.py" = ["record_verdict", "read_salvage"] },
    { "scripts/team/worker_salvage.py" = ["salvage_packs"] },
]
guard_test = ["tests/test_salvage_verdict*.py（在树）", "tests/test_foreman_caps_contract.py（目标态新增）"]
events_consumed = { session_events = ["逐件分析完成事件（每件分析完即写，52B fix 口径）"] }
events_produced = { wall_patch = ["validation 切片（经 adopt 采认）"], files = ["verdict-partial.json 逐件增量", "team/status/<pid>.json 骨架（工人面）"] }
artifacts = [
    { name = "partial-verdict", op = "workspace-write", path = "work/verdict-partial.json（D-2 封章粘性，salvage_verdict.py:121 sealed）", consumers = ["validator", "replan"] },
    { name = "worker-status", op = "workspace-write", path = "team/status/<pid>.json（增量落盘引导，worker prompt 单源）", consumers = ["prep", "validate"] },
    { name = "salvage-records", op = "workspace-write", path = "packs/<id>/（机器兜底，salvaged_from_machine 标记）", consumers = ["validate"] },
]
state_reads = ["本会话分析中间态（零跨席读）"]
local_uses = ["recorder CLI（salvage_verdict --process/--verdict/--final）"]
probes = "**缺席即事件**：per-run recorder 调用数与首步落盘时点由包装器采样，窗口内零调用/零落盘=告警事件（墙上 recorder_call_count 字段，schema 演进归 handoff-schemas §8）——现状「prompt 文字无运行时效力、无 per-run 报警」（锚件 2 §7/§10-④）由此门收口（必死样本=SL-8a，acceptance-line-map §2.8）"
callers = { internal = ["validator（承载点①）", "worker（增量落盘引导）", "prep（承载点②机器兜底）"], external = ["无"], workflow = ["无独立 job（经承载席 job 出现）"] }

[seat.recorder.authorization]
governance_face = "受保护路径面（同全席基线）"
audit_face = "caps-gate 审计＋缺席即事件告警面"
token_scope = "继承承载席（validator 面：零 GitHub 令牌；worker 面：会话零令牌）；机器兜底面无 secret（锚件 2 §7）"

[seat.recorder.budgets]
note = "无独立墙预算（承载席预算内执行）；首步落盘窗口=会话开始后首个分析单元内（缺席即事件判定窗口）"

[seat.recorder.verification]
contract_tests = ["tests/test_salvage_verdict*.py", "tests/test_foreman_caps_contract.py（目标态新增）"]
probes = "缺席即事件负例：桩会话全程零 recorder 调用->告警必触发（59 轮四问题④必死样本，验收线归 F4；必死样本=SL-8a，acceptance-line-map §2.8）"
probe_notes = "立席口径：recorder 的执法面=「必落字段与约定首步的机器可见性」，不是新增人类审批面；V-3 门（受控会话达标证明）保留为发版前置人工门，per-run 报警由本席 probes 承载"
```

**default-deny 声明（recorder）**：本席可写面＝verdict-partial/status 骨架/补卷记录三路径；零跨席读、零 GitHub 写、**零 workflow 编辑权**（`.github/workflows/**` 属治理行为面，走 wall-registry-change 通道，任何席位门清单不含——图外件② I8-B 夹具的拆除因此派 lead 席默认删行＋大哥退役批，不派写板席，见主设计稿 §2.4 表 2 与 out-of-graph §2.2）；**清单之外不存在**。缺席（该写不写）不是豁免，是告警事件。

---

## §3 门清单对位表（7 席 × M-CAP 键集）

### 3.1 引擎 M-CAP 原物（逐键行号锚，实读核实）

M-CAP 门清单段：`docs/specs/module-capabilities.toml:574`（`[module.M-CAP]`）起。逐键锚：

| 键 | 引擎锚 | 原物要点 |
|---|---|---|
| `entry` | `module-capabilities.toml:579` | 七条公开门（droid-task.yml / inflight_cap.py / guide / credits 断言 / frontdoor / frontdoor_parse / developer.md 帽面） |
| `api` | `:588`（双形态 str＋符号级 dict `:588-595`） | 模块级整面＋六符号登记面 |
| `guard_test` | `:596` | 四契约测试载体 |
| `events_consumed` | `:598` | `{ dispatch = ["droid-task"] }` |
| `events_produced` | 无独立行（M-CAP 段内缺席） | v4 词表可选键：已登记键禁删（缺席≠删除，契约测试对位引擎仓 `tests/test_module_capabilities_contract.py:159-166` 区段注释） |
| `artifacts` | 无独立行（同上） | 同上 |
| `state_reads` | `:601` | `[".evolution/config.yml"]` |
| `local_uses` | 无独立行（同上） | 同上 |
| `probes` | `:630` | 负向三探针（未登记符号内联 import 红／引号体载荷红／内联 -c 载荷必红） |
| `callers` | `:604`（internal `:605-608`、external `:609`、workflow `:610-615`） | v5 三名单全 file:line 锚 |
| `authorization` | `:618`（governance_face `:619`、audit_face `:620`、token_scope `:621`） | 三面语义 |
| `verification` | `:623`（contract_tests `:624-627`、probes `:630`、probe_notes `:631`） | 契约测试＋探针＋注记 |

**键集口径声明**：本表键集＝entry / api / guard_test / events_consumed / events_produced / artifacts / state_reads / local_uses / probes / callers / authorization / verification 十二键（引擎 MODULE_KEYS 实测 12 键，`tests/test_module_capabilities_contract.py:55-68`；mission 文档通称「十键＋三锚」「协作五键＋v5 三键」「十一显式键」皆为历史别名，皆指此 12 键集）；M-CAP 段内 events_produced/artifacts/local_uses 三键现状缺席属 v4 词表可选键的合法缺省（零消费面未写入，缺席≠删除），对位时按「形制同构（可选缺省）」判定，不按缺门处理。

### 3.2 对位总矩阵（判定词：同构收编／多出默认删／多出呈裁／缺门补齐／可选缺省）

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

（矩阵每格判定词的逐条依据见 §3.3～§3.6；「多出」指领班现状能力超出 M-CAP 形制应登记面的部分，「缺」指 M-CAP 形制应登记而领班现状未登记的部分。）

### 3.3 逐键对位详表

**entry（公开门/入口）**

| 席 | 现状（锚件 2 锚） | 判定 | 说明 |
|---|---|---|---|
| lead | `team.yml:52`，包装器入口 `:203-204` | 同构收编 | 双入口（job＋包装器）登记，与 M-CAP 双形态 entry 同构 |
| worker | `team.yml:503`；会话裸跑 `:599` | 缺门补齐 | 现状会话入口不合规（裸跑）——补齐方案=§4 包装器收进，`run_droid_session.py --role worker` 成为唯一会话入口 |
| prep | `team.yml:936` 纯脚本 | 同构收编 | 纯脚本 job 即 entry |
| validator | `team.yml:1382`＋`:1534-1535` 包装 | 同构收编 | — |
| replan | `team.yml:2141`＋`:2405-2406` 包装 | 同构收编 | — |
| assemble | `team.yml:4389` 纯脚本 | 同构收编 | — |
| recorder | 无独立 job（`:1515`/`:1223-1226` 承载） | 缺门补齐 | 补齐方案=立席（§2.7），entry=承载席会话内的 recorder 工具授权面 |

**api（可 import 面/可用工具）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| 全 7 席 | 无登记（「可用工具面」从无机器声明，五 lint 无一覆盖，锚件 2 §12） | 缺门补齐 | 补齐方案：逐席 §2 TOML 段的 api 键（脚本/符号级双形态照抄引擎 `:588-595`）；droid 会话工具白名单由包装器从门清单生成（§4.3），会话外工具调用=unregistered-tool-call 红 |

**guard_test（契约测试载体）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| lead | 领班墙契约测试在树（foreman 系 lint＋契约测试族），无 per-席能力面测试 | 缺门补齐 | 补齐：caps-gate 契约测试 `tests/test_foreman_caps_contract.py`（目标态新增，schema 键集/词表一次定死＋负对照共用生产校验路径） |
| worker | F-1/守卫/.delta 在树测试族 | 同构收编 | 既有族＋caps-gate 契约 |
| prep | worker_salvage 在树测试族 | 同构收编 | — |
| validator | salvage_verdict 在树测试族 | 同构收编 | — |
| replan | replan 在树测试族 | 同构收编 | — |
| assemble | assemble 在树测试族 | 同构收编 | — |
| recorder | salvage_verdict 族复用 | 同构收编 | — |

**events_consumed（消费事件名单）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| 全 7 席 | 无登记（消费面散在 needs/env/output 面无声明） | 缺门补齐 | 补齐：逐席 §2 TOML 段 events_consumed 键（wall_outputs/issue_comment/evidence 名单）；未登记消费=undeclared-event 红 |

**events_produced（产出事件名单）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| lead | 墙 patch＋计划单/子单/派单评论（`:439-443`）＋**I8-B 假 PAT 活验评论分支（`:419`/`:429-431`）** | 多出呈裁 | 职能产出收编；I8-B 活验夹具不是领班职能，是内嵌生产 workflow 的活验件——**默认删**（夹具仓化归 F3），若保留须单独呈裁（呈裁点：活验件与生产 workflow 的物理隔离方案） |
| worker | handoff 评论＋delta 上墙＋分支 push | 多出呈裁 | 职能产出收编；handoff 评论走母单＋子单双通道，双通道是否保留须呈裁（呈裁点：评论冗余面） |
| prep | 备料报告评论＋候选分支 | 同构收编 | — |
| validator | 墙 validation 切片（adopt `:1721`） | 同构收编 | — |
| replan | v2 子单＋旧单关闭＋通知评论 | 多出呈裁 | 职能产出收编；「旧子单关闭（not planned）」的关单权保留须呈裁（呈裁点：关单权与计划单权威面） |
| assemble | 状态卡评论＋子单/计划单关闭＋PR＋板面写 | 多出呈裁 | 全链最强写面（锚件 2 §6）逐门登记，PR create 权与关单权保留须呈裁（呈裁点：链尾写面集权） |
| recorder | verdict-partial 增量＋adopt 采认 | 同构收编 | — |

**artifacts（制品/写目标）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| lead | `team/lead-plan-segments/*.json`＋**repo 工作区任意文件写（无机器守卫）** | 多出默认删 | 登记写目标收窄为 lead-plan-segments 唯一工作区面；「任意文件写」是多出的门——**默认删**；若存在正当场景须单独呈裁（呈裁点：lead 会话的合法写面扩充） |
| worker | 卡面 allowed 集合（F-1，`:712-743` 区段）＋handoffs/status；**verdict.json/md 顶层孤儿写路径**（checks 副产物，worker prompt 单源要求会话自删） | 多出默认删 | 登记面收编；verdict.json/md 顶层路径不是本席制品——**默认删**（禁绝方式：包装器写目标预授权不含该路径＋caps-gate undeclared-artifact 探针，图外件清零归 F3） |
| prep | 候选分支＋evidence.tar.gz＋补卷 packs | 同构收编 | — |
| validator | verdict 系列文件 | 同构收编 | — |
| replan | team-plan-v2.json | 同构收编 | — |
| assemble | 板面 Status＋PR＋评论 | 多出呈裁 | 职能写面收编；板面写保留但收口单点＋终态一致性机制（Item closed 翻板归 F3）；PR create 保留须呈裁（呈裁点：设计稿交付链的 PR 权） |
| recorder | partial/status/补卷记录 | 同构收编 | — |

**state_reads（跨席状态读）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| lead | 墙 artifact 下载＋repo 全树可读（会话默认全读） | 多出默认删 | 收窄为墙＋卡面输入；「repo 全树可读」收窄为 state_reads 登记面——**默认删**全树读授权；确需扩充逐条呈裁（呈裁点：lead 读面扩充） |
| worker | 墙＋卡面 checks 脚本面 | 同构收编 | 会话读面随卡面（F-1 同源） |
| prep | 墙＋worker 分支树 | 同构收编 | — |
| validator | 证据包＋墙（只读） | 同构收编 | — |
| replan | 墙＋verdict＋证据（只读） | 同构收编 | — |
| assemble | 墙（pick 权威源） | 同构收编 | — |
| recorder | 本会话中间态 | 同构收编 | — |

**local_uses（本地可复用件）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| lead | 包装器 run_droid_session.py | 缺门补齐 | 现状仅 lead/validator/replan 经包装器且无登记——补齐：逐席登记 local_uses（包装器/CLI/git/pytest 面），未登记本地件调用=unregistered-tool-call 红 |
| worker | 裸跑无包装 | 缺门补齐 | 补齐=§4 包装器收进 |
| prep | git/pytest/checks | 同构收编 | — |
| validator | 包装器＋recorder CLI | 同构收编 | — |
| replan | 包装器 | 同构收编 | — |
| assemble | git/gh | 同构收编 | — |
| recorder | recorder CLI | 同构收编 | — |

**probes（探针面）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| lead | 无能力面探针（F-1 仅工人席） | 缺门补齐 | 补齐：caps-gate 三探针（写越界/令牌越界/未登记工具），§2.1 |
| worker | F-1 越界守卫＋（废止后）裸跑探针 | 同构收编 | F-1 判词化（out-of-scope-write）＋裸跑探针归 verification |
| prep | 补卷守卫四条件负例 | 同构收编 | — |
| validator | 无 schema 级负例 | 缺门补齐 | 补齐：verdict schema 执法负例（枚举外值/无证据引用被拒，handoff-schemas §8）＋D-2 封章粘性负例 |
| replan | 死因叙事被 r53c 逐字钉成**错误方向**（`:190-206`） | 缺门补齐 | 补齐=钉子反转（handoff-schemas §9.2）：断言改为「无证据不出 F-1 文案＋未明缺省」 |
| assemble | pick fail-closed 负例在树 | 缺门补齐 | 补齐：板面写单点性探针＋human_stop 消费探针 |
| recorder | 无 per-run 断言 | 缺门补齐 | 补齐：缺席即事件负例（桩会话零 recorder 调用→告警必触发） |

**callers（下游消费名单，v5）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| 全 7 席 | 无登记（下游面散在 needs 面无声明） | 缺门补齐 | 补齐：逐席 §2 TOML 段 callers 三名单（internal/external/workflow，全 file:line 锚，对位引擎 `:604-615`）；外部消费一律「无」，领班链是仓内闭环 |

**authorization（三面，v5）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| lead | 令牌实际有（`:120`/`:157`/`:79`/`:241`）＋**工作区任意写授权（无守卫）＋I8-B 假 PAT 面** | 多出默认删 | token_scope 登记收编；「任意写＋假 PAT 夹具」不在清单=**默认删**（I8-B 保留须呈裁）；governance/audit 两面补齐登记 |
| worker | 会话零 GH token＋commit 步 token＋BYOM | 多出呈裁 | token_scope 收编；commit 步 contents:write 保留须呈裁（呈裁点：push 权与 F-1 的先后序——F-1 拒绝后 push 必须不可能发生） |
| prep | github.token 报告面 | 同构收编 | — |
| validator | 双 token 显式置空 | 同构收编 | 全链最小面（零 GitHub 权），v3.0 保留并执法 |
| replan | 会话零 token＋落单步全权 issue 写**同 job 混合** | 多出默认删 | 混合面=多出的门——**默认删**；补齐方案=两会话面拆门（无 token 会话门＋落单写门独立授权独立审计，§2.5 token_scope）；拆门后落单写权保留须呈裁（呈裁点：关单权） |
| assemble | PAT＋github.token | 多出呈裁 | 两令牌分面收编；板面 PAT 权保留须呈裁（呈裁点：板面写权威面） |
| recorder | 无独立授权面 | 缺门补齐（立席） | 补齐=立席（§2.7），token_scope 继承载席 |

**verification（契约测试＋探针，v5）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| 全 7 席 | 五 lint＋契约测试**无一覆盖能力授权/死因佐证/板面终态/recorder 纪律**（锚件 2 §12 结论） | 缺门补齐 | 补齐：caps-gate 契约测试族（schema 键集一次定死＋负对照共用生产校验路径＋接线锁），逐席 verification 键落 §2 各段 |

**budgets（域扩展键）**

| 席 | 现状 | 判定 | 说明 |
|---|---|---|---|
| lead/validator/replan | 包装器写墙预算（600/480/480，foreman_run_lib.py:37-40 区段起）＋job 墙（15/15/15m，team.yml:59/:1387/:2154） | 同构收编 | 数值迁入门清单 budgets 键（唯一来源），包装器改读门清单（§4.2）；validator 双预算对平口径=会话墙 480（包装器第一道墙）/软超时 500（job 15m−400s 外层哨兵线，§2.4 budgets 注） |
| worker | 账面 900 不接线＋裸跑硬编码 | 缺门补齐 | 补齐=§4：预算从门清单读，workflow 文本零预算字面量 |
| prep/assemble/recorder | 步级超时散布 | 同构收编 | 步级超时登记进 budgets 键 |

### 3.4 多出的门总表（默认删；保留须单独呈裁）

| # | 门 | 席 | 现状锚 | 处置 |
|---|---|---|---|---|
| 1 | repo 工作区任意文件写（无机器守卫） | lead | 锚件 2 §1（`team.yml:203` 会话步） | **默认删**；写面收窄 lead-plan-segments |
| 2 | I8-B 假 PAT 活验分支内嵌生产 workflow | lead | `team.yml:419`/`:429-431` | **默认删**；夹具仓化归 F3；保留须呈裁（物理隔离方案） |
| 3 | repo 全树读授权（会话默认全读） | lead | 同 1 | **默认删**；读面登记 state_reads |
| 4 | verdict.json/md 顶层孤儿写路径 | worker | worker prompt 单源（checks 副产物自删纪律） | **默认删**；包装器预授权不含＋探针判红（F3 收编） |
| 5 | verify 步全仓 subprocess 无超时 | worker | 锚件 2 §2（verify 面） | **默认删**；收口卡面 checks 白名单＋300s 步超时 |
| 6 | 会话面与落单写面同 job 混合 | replan | `team.yml:2210-2211` vs `:2423` | **默认删**；拆门（§2.5） |
| 7 | 5 secrets 全量入 env-check 环境 | env-check（零号门） | `env-check.yml:82-86` 五注入行 | **默认删**；按席位差异 scope 收口（F3） |
| 8 | 板面终态图外写入口（Item closed 自动化） | assemble（板侧） | `docs/板面关单翻板-最小操作指引.md` | repo 侧无写点可拦（专档结论原文）——**默认删**的落点在板侧 Disable/终态选项改造（人工操作面，呈裁清单随主设计稿）；repo 侧配合=终态一致性复核门（F3/F4 承载） |

**呈裁口径**：任一默认删的门若有保留理由，必须逐条单独呈裁（大哥裁），呈裁件须含：门的现状锚、保留理由、收窄后的执法设计、caps-gate 判词——不允许「先保留后补登记」。

### 3.5 缺的门补齐方案汇总

| # | 缺口 | 覆盖席 | 补齐方案 | 施工载体（目标态） |
|---|---|---|---|---|
| 1 | 能力面登记文件不存在 | 全 7 席 | 本件 §2 定义 `foreman-caps.v1.toml` schema 与逐席样例 | repo 根 `foreman-caps.v1.toml` |
| 2 | api/local_uses/callers/events 消费产出无登记 | 全 7 席 | 逐席 TOML 段补齐（§2/§3.3） | 同上 |
| 3 | worker 会话无包装器入口 | worker/worker2 | §4 包装器收进 | run_droid_session.py --role worker 接线＋budgets lint 豁免废止 |
| 4 | 能力面契约测试与守卫 | 全 7 席 | caps-gate 守卫＋契约测试（判词 §1.3、接线锁 §1.4） | `scripts/team/check_seat_caps.py`＋`tests/test_foreman_caps_contract.py` |
| 5 | recorder 缺席即事件 | recorder | 立席＋per-run 采样告警（§2.7 probes） | 包装器采样＋墙 recorder_call_count 字段 |
| 6 | 死因叙事证据执法 | replan | verdict/plan-v2 schema 证据引用强制＋钉子反转（handoff-schemas §9） | schema v2＋契约测试反转 |
| 7 | human_stop 消费门 | assemble | probes 补齐（§2.6） | assemble 消费分支 |
| 8 | guard_test/verification 全员面 | 全 7 席 | caps-gate 契约测试族（§3.3 verification 行） | 目标态测试文件 |

### 3.6 动门＝边界事件

**声明**：对门清单的任何增删改（新增门、删除门、改 token_scope/写目标/预算）都是**边界事件**——不是配置微调，是席位能力边界的变更，必须走登记面升级闸（`wall-registry-change: true` 声明＋caps-gate `mixed-registry-change` 判词执法，§1.6）＋契约测试同批改（§1.2）＋大哥呈裁（多出的门的保留项，§3.4 口径）。

**边界事件记录面**：动门事件三要素（谁动了哪个席位的哪个键→旧值→新值）随变更集 PR 留痕；caps-gate 对平测试断言「登记文件变更必带声明行」（对位引擎对账纪律「无回读不得记完成」，form-basis 要点 9）。**换入判据对位**：领班模块换入引擎编排槽位时，「门清单不变」是三判据之一（对位引擎封印形制 form-basis 要点 8：`scripts/hardening_baseline.py:1-5` 指纹快照＋`--verify` 对平）——动门即破坏「不变」前提，故必须以边界事件显式过闸。

---

## §4 工人席收进包装器设计（VAL-GATES-004）

### 4.1 废止对象（现状）

裸跑形态：`timeout --signal=TERM --kill-after=30s 900s ~/.local/bin/droid exec --auto high …`（一轮 `team.yml:599`；worker2 同款 `:2784`）。三点不合规：

1. **不经包装器**：run_droid_session.py 的墙预算/心跳/patch 面对工人席不存在；budgets lint 明文豁免该形态（`lint_workflow_budgets.py:16-18` BARE_DROID 正则＋`:43-51` worker/900s 豁免分支）。
2. **900s 硬编码在 workflow 文本**：墙上账面预算（foreman_run_lib.py:53-54 区段）不被执行路径读取——预算是账面非执法。
3. **执法与会话同体**：GNU timeout 外墙，无回合预算/收束/续作；工具长挂时孤儿子进程持管道可拖到 25m job 墙（45B 实证，锚件 2 §10-②）。

### 4.2 包装器＝执法点之一：预算从门清单读

接线设计（目标态，施工时落）：

```
worker job（team.yml worker 步改造）
  └─ run_droid_session.py --role worker --caps foreman-caps.v1.toml
       ├─ caps load：读 [seat.worker.budgets]（droid_wall_sec=900 / job_wall_min=25）
       ├─ fail-loud 校验：schema 校验（键集/词表一次定死）→ 畸形即 exit 2（永不静默绿）
       ├─ 预算推导：软超时 = job_timeout_sec − 400（基座=job timeout，引擎 run_lead.sh:6
       │    「timeout−400s」的 timeout 即 job timeout——droid-review-lead.yml:35-37 margin
       │    语义＝哨兵先于 GitHub 硬杀；droid 墙预算是 T0 计时面，不进公式）
       ├─ 执法启动：哨兵先行→SIGTERM 进程组→宽限（10s）→SIGKILL 进程组
       │    （终止序列照抄引擎 run_lead.sh:282/:286 负 PID 组信号形态）
       └─ 墙 patch：FOREMAN_RUN_PATCH=1 上墙 session_outcome 三字段（write_worker_delta 既有分类器复用）
```

- **预算唯一来源＝门清单**：workflow 文本零预算字面量；`timeout ... 900s` 字面量废止后，caps-gate 探针（BARE_DROID 形态即红）与 budgets lint 同判词双载体执法。
- **执法在体外**：哨兵＋进程组信号通道不依赖被管进程配合（§1.7）；哨兵在案＝delta 不采信为 ok（强制失败优先）。
- **lint 同步反转**：`lint_workflow_budgets.py:43-51` 的 worker/900s 豁免分支废止——裸跑形态对 7 席一律红，零豁免。

### 4.3 会话级配置从门清单生成

会话启动时，包装器从 `[seat.worker]` 段生成会话级配置（三步，确定性生成、可复演）：

| 步 | 输入键 | 生成的会话配置 | 对位引擎形制 |
|---|---|---|---|
| ①工具白名单注入 | `api`＋`local_uses` | droid 会话 tools 白名单（卡面工具集；Write/Edit 是否入列随卡面 artifacts 授权） | run_lead.sh:67 `LEAD_ENABLED_TOOLS` 白名单形制（引擎锚 `src/infra_core/engine/droid_review/run_lead.sh:67`） |
| ②写目标预授权 | `artifacts`（op=workspace-write 面） | F-1 allowed 集合（卡面文件＋handoffs/status 三路径）；越界写实时拒绝（事中守卫，非现行 commit 步事后守卫） | F-1 判词化（out-of-scope-write） |
| ③令牌 scope 最小化 | `authorization.token_scope` | 环境注入最小集：会话步零 GH_TOKEN（维持现状最小）；commit 步才挂 contents:write | validator 双置空形制（对位 `team.yml:1502-1503`） |

生成纪律：包装器生成的会话配置落 `session-config.json`（内容含预算/白名单/写目标/令牌面四节），caps-gate 对平测试断言「会话配置与门清单逐键一致」——配置漂移即红。**包装器即执法点**：预算（本节）、白名单（①）、写边界（②）、令牌（③）四面的执法动作都发生在包装器进程内，会话本体无任何自授途径。

### 4.4 worker2 同构适用

worker2（`team.yml:2697`；裸跑 `:2784`）按本节同构收进；分支后缀 `-r2`、delta 上墙 `:3017` 等差异点不变。

---

## §5 结构化交接物 schema 设计（索引）

四类交接物（worker-delta / verdict / plan-v2 / handoff）的 schema 设计独立成稿：`docs/wall-v3/handoff-schemas.md`。核心原则与本件 §2 门清单的衔接：

1. **因果结论枚举化＋证据引用强制**：因果结论类字段只能从枚举选＋必须挂 evidence_ref；枚举外值 schema 校验即拒（caps-gate narrative-without-evidence 判词执法）。
2. **证据对象构造权单源**：证据对象只能由核查环节（validator 席＋机器守卫步）构造；lead/worker/replan/assemble 无构造入口。
3. **「未明」缺省**：无证据时唯一合法取值 `unknown`——59 轮四问题①（replan 虚构「F-1 检查拒绝」）的 schema 层收口。
4. **自由文本不承载判定**：reason/summary 类字段只给人看，机器判定只读枚举与证据引用。

落位与执法设计全文见 `handoff-schemas.md` §1～§9。

---

## 附A 本件 file:line 锚清单（供锚解析器）

| 锚 | 解析判据（该行应含） |
|---|---|
| `team.yml:7` | `v2.7.0` |
| `team.yml:31` | `permissions` |
| `team.yml:37` | `env-check` |
| `team.yml:52` | `lead:`（job 头） |
| `team.yml:203` | `run_droid_session.py`（wrapper 调用，跨 :203-204） |
| `team.yml:419` | `ghp_i8livefixture`（I8-B 假 PAT 夹具默认值；值本体不转录） |
| `team.yml:429` | `I8] API墙活验 B`（标题命中行） |
| `team.yml:503` | `worker:`（job 头） |
| `team.yml:599` | `900s`（裸跑行） |
| `team.yml:731` | `reset --soft` |
| `team.yml:836` | `write_worker_delta` |
| `team.yml:851` | `workers-wall-merge:`（job 头） |
| `team.yml:860` | `prep_should_run` |
| `team.yml:885` | `merge_worker_deltas` |
| `team.yml:936` | `prep:`（job 头） |
| `team.yml:1223` | `worker_salvage`（接线区段起） |
| `team.yml:1321` | `GH_TOKEN`（prep 报告步） |
| `team.yml:1382` | `validate:`（job 头） |
| `team.yml:1390` | `GITHUB_TOKEN`（置空行） |
| `team.yml:1515` | `build_validator_prompt` |
| `team.yml:1534` | `run_droid_session.py`（validator 包装） |
| `team.yml:1721` | `run_adopt_step` |
| `team.yml:1779` | `revalidate:`（job 头） |
| `team.yml:2141` | `replan:`（job 头） |
| `team.yml:2210` | `GITHUB_TOKEN`（replan 会话步置空） |
| `team.yml:2259` | `Round-53 fix`（推断注释起；文案赋值落 :2278-2279） |
| `team.yml:2405` | `run_droid_session.py`（replan 包装） |
| `team.yml:2423` | `GH_TOKEN`（落单步） |
| `team.yml:2697` | `worker2:`（job 头） |
| `team.yml:2784` | `900s`（worker2 裸跑） |
| `team.yml:3107` | `prep2:`（job 头） |
| `team.yml:3618` | `validate2:`（job 头） |
| `team.yml:3948` | `run_adopt_step`（validate2 flips 面） |
| `team.yml:4389` | `assemble:`（job 头） |
| `team.yml:4431` | `PROJECTS_STATE_PAT` |
| `team.yml:4441` | `project_state_write` |
| `team.yml:4636` | `assemble_chain_facts` |
| `env-check.yml:82` | `S_FACTORY_API_KEY`（五 secrets 注入区段起） |
| `scripts/team/foreman_run_lib.py:37` | `"lead": {`（预算区段起，lead droid_wall_sec=600 落 :38） |
| `scripts/team/foreman_run_lib.py:53` | `"worker": {`（worker 区段起，droid_wall_sec=900 落 :54） |
| `scripts/team/lint_workflow_budgets.py:16` | BARE_DROID 正则 |
| `scripts/team/lint_workflow_budgets.py:43` | worker/900s 豁免分支 |
| `scripts/team/write_worker_delta.py:42` | SELF_EXIT_CODES |
| `scripts/team/write_worker_delta.py:45` | classify_session_outcome |
| `scripts/team/worker_salvage.py:13` | 守卫四条件 docstring |
| `scripts/team/salvage_verdict.py:18` | PARTIAL_NAME |
| `scripts/team/salvage_verdict.py:121` | sealed 粘性 |
| `scripts/team/attribution_reason.py`（模块锚） | blocked_reason / neutral_attribution |
| `schemas/foreman-run.v1.schema.json:33` | human_stop |
| `schemas/foreman-run.v1.schema.json:65` | session_outcome 枚举 |
| `schemas/foreman-run.v1.schema.json:146` | session_outcome_by_pid |
| `schemas/foreman-run.v1.schema.json:153` | droid_exit_code_by_pid |
| `schemas/foreman-run.v1.schema.json:157` | stream_tail_marker_by_pid |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:190` | 钉子测试定义 |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:201` | F-1 文案逐字行起（跨 :201-:202） |
| `docs/板面关单翻板-最小操作指引.md` | Item closed 翻板专档 |
| `docs/W-14-写板活验通过判据-修订.md` | PAT 时间线定性 |
| 引擎：`module-capabilities.toml:574/579/588/596/598/601/604/618/623/630` | M-CAP 逐键（§3.1 表） |
| 引擎：`scripts/check_module_wall.py:12/13/90/131` | 形制要点 1/3/4（转引 form-basis） |
| 引擎：`src/infra_core/engine/droid_review/run_lead.sh:6/67/282/286` | 预算公式/工具白名单/终止序列（转引 form-basis） |
| 引擎：`scripts/hardening_baseline.py:1` | 封印形制（转引 form-basis） |

> 锚随树演化可能漂移；重核实以实读为准（本件快照 2026-11-27，测试仓 R58-D 收尾态）。

## 附B default-deny 速览

| 席 | 全集口径（清单之外不存在） |
|---|---|
| lead | 写=lead-plan-segments 唯一工作区面；读=墙＋卡面输入；令牌=token_scope 三件套；I8-B 夹具与全树读写不在清单 |
| worker | 写=卡面 allowed＋handoffs/status/delta；工具=包装器白名单；令牌=会话零 GH token；裸跑/全仓 verify/verdict 孤儿路径不在清单 |
| prep | 零 droid 零 BYOM；写=候选分支＋packs 缺失件 |
| validator | 零 GitHub 写权；写=verdict 系列＋证据对象；读=证据包＋墙 |
| replan | 写=plan-v2（拆门后落单写独立授权）；因果结论必有证据或「未明」 |
| assemble | 零 droid；写=板面 PAT 单点＋PR＋issue 面；human_stop 必须消费 |
| recorder | 写=partial/status 骨架/补卷记录；零跨席读零 GitHub 写；缺席=告警事件 |
