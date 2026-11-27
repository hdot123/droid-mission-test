# 形制基准（form-basis）——引擎墙形制十要点

> 锚件 1/2（mission F1/design-inputs 产出）。领班面墙 API 设计稿 v3.0 的唯一形制基准：设计稿定义任何墙/门/守卫时，形制照抄本件十要点；本件每要点带引擎仓（infraro-core，本地只读参照仓）原物 file:line 锚，全部经实读核实（2026-11-27 快照）。
>
> **本文只引用引擎仓相对路径**；行号锚格式 `路径:行号`。锚点可解析判据＝文件在树、行号不越界、锚定内容含要点关键词。
>
> **禁抄项声明见 §11**——引擎墙自身的未闭合缺口不是形制，设计稿不得照抄。

---

## 要点 1：双 TOML 登记真源＋守卫零硬编码（fail-loud）

**形制**：墙的规则全部住在登记文件里，执法脚本不硬编码任何路径/模块 id/接缝 id。归属墙与能力墙各一份 TOML（双登记真源）；规则畸形或输入歧义时守卫 fail-loud（exit 2），永不静默绿。

**原物锚**：
- 归属墙登记：`docs/specs/modules.toml:19`（`schema_version = 1`）、`docs/specs/modules.toml:24`（`path_match = "longest-prefix"`）、`docs/specs/modules.toml:206`（M-CAP 条目段起）
- 能力墙登记：`docs/specs/module-capabilities.toml:77`（`schema_version = 5`）、`docs/specs/module-capabilities.toml:574`（`[module.M-CAP]` 段起）
- 守卫本体 docstring（零硬编码承诺原文）：`scripts/check_module_wall.py:4`——"One wall, 16 doors: every changed file must resolve to an owner"；`scripts/check_module_wall.py:12-14`——"The registry files are the single rule source; this script hardcodes no paths, module ids or seam ids. Malformed rules or ambiguous input fail loud with exit 2 (usage/environment error), never silently green."

**设计稿对位**：`foreman-caps.v1.toml`（席位能力登记真源）＋守卫脚本分立；守卫零席位 id 硬编码。

---

## 要点 2：每模块一段门清单，字段固定（十键＋v5 三键）

**形制**：能力墙 TOML 里每个模块一段 `[module.<id>]`，键集固定：entry（公开门）/ api（双形态：str＝模块级整面，`{path: [符号]}`＝符号级）/ guard_test（契约测试载体）＋协作五键（events_consumed / events_produced / artifacts / state_reads / local_uses）＋v5 三键（callers / authorization / verification）。全部值带 file:line 锚。

**原物锚**：`docs/specs/module-capabilities.toml:574`（M-CAP 门清单段起）、`:604`（callers）、`:618`（authorization）、`:623`（verification）。

**设计稿对位**：逐席位门清单（F2）每席一段，字段照此键集＋token scope 对位 authorization 面。

---

## 要点 3：schema 一次定死＋同批改锁（负对照共用生产校验路径）

**形制**：键集/词表/计数硬编码在契约测试里；增删键或词表必须同一变更批内改契约测试，禁止守卫或登记单边漂移。负对照（内存变异坏 schema）与生产校验共用同一实现——牙齿一致，测试红即生产红。

**原物锚**：
- 钥匙台账头注铁律原文：`docs/specs/key-registry.toml:14-16`——「schema 一次定死：键集与词表硬编码在 tests/test_key_registry_contract.py；增删键/词表须同批改契约测试，禁止二改 schema 单边漂移」
- 契约测试族：`tests/test_modules_toml_contract.py`（模块 id 硬编码）、`tests/test_module_capabilities_contract.py`（schema 键集一次定死）、`tests/test_key_registry_contract.py`（词表＋对账）

**设计稿对位**：`foreman-caps.v1.toml` 的 schema 与枚举词表一次定死，契约测试同批锁；断言脚本与守卫共用校验实现。

---

## 要点 4：判词只增不改＋退出码三态

**形制**：守卫判词常量集只增不改（改名/删判词即破坏下游采认）；退出码三态 0（clean）/1（violations）/2（环境错误）。违规输出逐条点名 `RED <rule>: <file>: <detail>`，末行 `clean` 或 `RED`。

**原物锚**：判词常量 `scripts/check_module_wall.py:90`（RULE_UNREGISTERED 起）至 `:113`（RULE_QUOTED_PAYLOAD 止），共 11 个 RULE_* 常量；三态退出语义见 `scripts/check_module_wall.py:13-14`（"Malformed rules or ambiguous input fail loud with exit 2 (usage/environment error), never silently green"，原文跨 :13-:14 两行）。

**设计稿对位**：面墙守卫判词枚举一次定死、只增不改；任何检查器退出码三态，缺环境＝2 非绿。

---

## 要点 5：CI 恒跑接线锁（零 if、零 continue-on-error、两腿同面）

**形制**：守卫在 CI 恒跑（push 与 PR 两腿同面），接线步零条件门、零 continue-on-error；「守卫确实接在 CI 上」这个事实本身由契约测试锁住（接线锁测试）。

**原物锚**：
- 接线步：`.github/workflows/ci.yml:428-429`（`- name: Module wall guard` → `run: python scripts/check_module_wall.py --full-repo`）；同段注释 `:425-427` 明记 `--changes` 专属判词未接 CI（禁抄项，见 §11）
- 接线锁：`tests/test_module_wall_ci_wiring.py`（恒跑恰一步/零 if/两腿门/success-only 聚合/接线目标在树）

**设计稿对位**：面墙守卫（caps-gate）接线进 foreman-wall-ci 恒跑；接线语义有契约测试；施工期任何判词不落 CI 即显式未闭合，不冒充已执法。

---

## 要点 6：放行门单源 ruleset，不在代码养第二套标准

**形制**：合并放行门的唯一单源是 GitHub ruleset（branch protection main）required_status_checks；代码只持「门名→workflow」承载注册单作为升门人工同步点，不持门表快照。扩门只走「加进 ruleset」，配套契约测试断言投影齐全——ruleset 加门而注册单未同步补行即红。

**原物锚**：
- 单源声明注释原文：`scripts/board_sync_parse.py:97-104`——「放行门单源=ruleset（branch protection main，id 23079535）required_status_checks——本模块不再持门表快照……扩门只走『加进 ruleset』，不在代码养第二套标准」
- 承载注册单：`scripts/board_sync_parse.py:114-117`（GATE_TO_WORKFLOW：quality-gate→Quality Gate、substrate-gate-suite→CI）

**设计稿对位**：面墙守卫进 CI 门走同一单源口径；设计稿不设第二套门表常量。**两门口径（R-29 已裁，见 §11.2）：quality-gate / substrate-gate-suite，droid-review 不在执法门名单。**

---

## 要点 7：登记面升级闸＋governance 受保护路径

**形制**：改墙登记面（两 TOML＋守卫本体＋CI 守卫段）的变更集必须带显式声明标记（`wall-registry-change: true` 注释行），否则守卫判 `mixed-registry-change` 红——登记面升级显式化。登记面同时纳入 governance 受保护路径（owner 之外的改动被拒）。

**原物锚**：
- 升级闸常量：`scripts/check_module_wall.py:131`（`REGISTRY_CHANGE_DECLARATION = "wall-registry-change: true"`）
- 受保护路径：`src/infra_core/governance.py:26-34`（DEFAULT_PROTECTED_PATTERNS 七模式，含 `docs/specs/**`、`scripts/check_module_wall.py`、`.github/workflows/**`）

**设计稿对位**：`foreman-caps.v1.toml`＋守卫本体改动须带升级声明标记；登记面路径列入受保护面。**注意：引擎仓受保护路径面本身的执法状态是显式未闭合项（§11.1 NEW-1/U-4），设计稿只抄「升级闸＋保护面」形制，不抄其未闭合态。**

---

## 要点 8：封印＝sha256 指纹快照＋--verify 对平（确定性）

**形制**：模块封印判据 = 对每个模块产出「管辖文件清单＋每文件 sha256＋测试资产清点」快照；`--verify` 用同一套规则重算并逐项比对落盘快照，管辖面未变即退出码 0。快照确定性：无时戳、无绝对路径、同 tree 重跑逐字节相同。换模块判据＝门清单不变＋封印快照对平＋契约测试整套全过。

**原物锚**：
- 工具头注：`scripts/hardening_baseline.py:1-5`——「16 模块指纹基线工具（第一阶段硬化 · M1 封印底本）……终态对平（`--verify`）用同一套规则重算并逐项比对落盘快照，模块管辖面未变即退出码 0」
- sha256 计算与确定性：`scripts/hardening_baseline.py:113`（file_sha256）、`:180-182`（payload_sha256，排序固定后哈希 payload）；`--verify` 对平实现 `:303` 起；exit 0 判定 `:388`

**设计稿对位**：席位能力面封印（foreman-caps 指纹快照＋verify 对平）作为「换领班」判据之一；快照工具确定性同款。

---

## 要点 9：钥匙零值登记＋三态词表（use/cap_change；active/dormant/zombie/revoked）

**形制**：钥匙总管理台账只记名与元数据，任何字段禁止出现密钥值本体（契约测试以常见密钥值前缀族全文件扫描）。每条钥匙记录固定字段：name/kind/holder/access/nature/status/opens/consumes（逐条 file:line 消费锚）/notes/track_ref。定性二词（use＝使用钥匙 vs cap_change＝改能力钥匙）×状态四词（active/dormant/zombie/revoked）；机内对账（孤儿=0、幽灵=0、行号锚漂移即红）；「无回读不得记完成」；牺牲品样本常驻登记防幽灵复活。

**原物锚**：
- 台账头注与铁律：`docs/specs/key-registry.toml:2`（台账头注）＋`:5-8`（唯一真源与三轨归一、append-only 流水）、`:11-13`（零密钥值铁律）、`:14-16`（schema 同批改锁）、`:25-33`（定性/状态/读写词表定义）
- 台账本体：`docs/specs/key-registry.toml:38`（`schema_version = 1`）起
- 作废动作与回读证据：头注 `:7-8`（evidence/hardening-phase1-2026-11-20/key-ledger.md，append-only）

**设计稿对位**：领班制钥匙台账照此形制（零值、字段固定、use/cap_change 定性、逐条消费锚）；五 secrets 与 BYOM 三件盘点登记从本形制出（值不入稿）。

---

## 要点 10：失败规范＝点位普查表

**形制**：失败规范承载件是「全仓失败点位普查表」，每点位字段：触发面 / 现有 handler / 定级（无｜部分｜已接） / 缺口·备注；另设机器判据（指纹去重、升级滑窗、恢复自动闭环）。结构盲区显式列出（结构性不可见的失败面单列盲区行）；三态纪律：passed／显式未闭合／失败，不得虚称闭合。

**原物锚**：
- 普查表本体：`docs/guides/exception-point-inventory.md:23`（「全部活跃 workflow 失败点位清单（18 点）」）、`:27`（表头：`| # | 失败点位 | workflow | 触发面 | 现有 handler | 定级 | 缺口 / 备注 |`）
- 结构盲区显式列出：`docs/guides/exception-point-inventory.md:94`（「结构性盲区（显式列出）」）； retired 点位留痕范式 `:41`（~~13~~ 退役行）

**设计稿对位**：逐席位失败规范（F4）照普查表五字段＋机器判据＋盲区显式列出＋三态纪律成文。

---

## §10 补遗：执法点形制（超时墙/处决序列/工具白名单/环境剥离）

> 此四件不是独立要点，是要点 1-10 在「执法动力学」维度的形制素材，F3/F4 设计执法时照抄。

**a. 有界退出预算面（软超时＋轮数封顶＋心跳）**——原物锚：`src/infra_core/engine/droid_review/run_lead.sh:5-10`（纪律机制头注：轮数封顶 LEAD_MAX_TURNS 默认 100；软超时 LEAD_SOFT_TIMEOUT_SEC 按 workflow timeout−400s 公式推导注入；心跳采样双落纯观测不杀进程）；`:52-55`（默认值定义：LEAD_SOFT_TIMEOUT_SEC/LEAD_MAX_TURNS/LEAD_KILL_GRACE_SEC）。

**b. 终止序列（哨兵先行 → SIGTERM 进程组 → 宽限 → SIGKILL 进程组）**——原物锚：`run_lead.sh:9-10`（头注：「哨兵：lead-terminated.reason 先行（写哨兵 → SIGTERM 组 → 宽限 → SIGKILL）；哨兵在案 = findings 不采信（强制失败优先，防越界假绿混入验收数据）」）；实码 `run_lead.sh:282`（`kill -TERM "-$exec_pid"` 负 PID 组信号）与 `:286`（`kill -KILL` 同形态）。执法通道不依赖被管进程配合（组信号整组收）。

**c. 重试共享预算（绝对墙钟上限）**——原物锚：`run_lead.sh:318`（注释：「LEAD_TOTAL_DEADLINE_EPOCH 是整个 lead pass 的绝对墙钟上限（首轮起点起算」）、`:331`（预算起点）、`:349`（重试预算＝截止−当前）。重试不重置预算，最坏墙钟恒 ≤ soft＋宽限，不击穿 job timeout。

**d. 工具白名单＋pass-2 环境剥离**——原物锚：`run_lead.sh:67`（`LEAD_ENABLED_TOOLS="${LEAD_ENABLED_TOOLS:-Read,Grep,Glob,LS,Task}"` 默认值单行）＋`:19`（行注：Write/Edit 也移除——「提示词内嵌不可信 PR diff」）＋`:65`（行注：「任何评论/发帖/PR 写/执行类工具不得进入」）；pass-2 面由 run_validator.sh 承载（GITHUB_TOKEN/GH_TOKEN 显式置空）。

---

## §11 禁抄项声明（缺口不是形制）

> 以下两项是引擎墙**显式登记的未闭合缺口**（三态纪律下的「显式未闭合」），不是形制的一部分。领班面墙设计稿**禁止照抄其未闭合态**；对应面必须给出真实执法设计（「须执法，不允许纸面有门」）。设计稿引用引擎形制时，凡触及本节两点，一律以本节口径改写为执法设计。

### 11.1 VAL-M4-004／VAL-M4-007 未闭合态

**原物锚**（历史档，只读不改写）：`evidence/step5-api-unification/closeout/01-closeout-pack.md:94`（VAL-M4-004 行原文「**显式未闭合**（CI 执法面）／CLI 拦截面已验证……**CI 面缺口＝NEW-1/2/3**」）、`:97`（VAL-M4-007 行原文「**显式未闭合**……(a) 契约三门 vs 实执法两门＝用户裁定面……(b) droid-review 面显式停用（用户 2026-11-24 裁定）……判词维持显式未闭合不冒充」）。

**三个具体缺口（NEW-1/2/3）**：
- NEW-1＝governance owner 门停用态（evolution-governance workflow 变量门未设＋disabled_manually）；
- NEW-2＝`--changes` 专属判词（rename 改界、mixed-registry-change）未接 CI——引擎仓内自证：`.github/workflows/ci.yml:425-427` 注释原文「--changes 专属判词……为守卫 CLI 能力，本流水线未接线」；
- NEW-3＝登记面不在 governance 保护面（修复中非已闭合：U-4 已扩 DEFAULT_PROTECTED_PATTERNS 至七模式，`src/infra_core/governance.py:26-33`；U-2/U-3 未落地）。

**设计稿义务**：领班面墙的登记面升级闸必须接 CI 恒跑判词；登记面保护必须是运行时执法（非页面开关）；不允许任何「守卫判词存在但不接 CI」的形制。

### 11.2 R-29 两门口径演化（引用口径以两门为准）

**原物锚**：`evidence/step5-api-unification/closeout/05-risk-register.md:70`（R-29 行原文：「契约 required 三门（quality-gate/droid-review/substrate-gate-suite）实执法两门——droid-review 入口用户 2026-11-24 `disabled_manually` 停用……契约文本不动，缺口属用户裁定面」）。

**演化结论（已收口）**：R-29 经裁定采 (b)——契约口径**正式修订为两门**（quality-gate / substrate-gate-suite），PR #870（2026-11-27 MERGED）落地三载体同步。

**设计稿义务**：引用引擎「放行门」口径时一律写**两门**（quality-gate / substrate-gate-suite），不得复述「契约三门」旧口径；引用时注明演化（三门→两门，droid-review 已退）。领班面墙自身需要的门数按其守卫面独立裁定，不受两门/三门演化牵连，但**任何挂名未执法的门都按 §11.1 禁抄项处理**。

---

## 附：锚清单（本件 file:line 锚一览，供锚解析器与后续 feature 复用）

| 锚 | 解析判据（该行应含） |
|---|---|
| `docs/specs/modules.toml:19` | `schema_version = 1` |
| `docs/specs/modules.toml:24` | `path_match = "longest-prefix"` |
| `docs/specs/modules.toml:206` | `id = "M-CAP"` |
| `docs/specs/module-capabilities.toml:77` | `schema_version = 5` |
| `docs/specs/module-capabilities.toml:574` | `[module.M-CAP]` |
| `docs/specs/module-capabilities.toml:604` | `[module.M-CAP.callers]` |
| `docs/specs/module-capabilities.toml:618` | `[module.M-CAP.authorization]` |
| `docs/specs/module-capabilities.toml:623` | `[module.M-CAP.verification]` |
| `scripts/check_module_wall.py:4` | `One wall, 16 doors` |
| `scripts/check_module_wall.py:12` | `single rule source`（零硬编码承诺） |
| `scripts/check_module_wall.py:13` | `fail loud with exit 2`（跨 :13-:14） |
| `scripts/check_module_wall.py:90` | `RULE_UNREGISTERED = "unregistered-new-file"` |
| `scripts/check_module_wall.py:113` | `RULE_QUOTED_PAYLOAD = "unregistered-quoted-payload-import"` |
| `scripts/check_module_wall.py:131` | `REGISTRY_CHANGE_DECLARATION = "wall-registry-change: true"` |
| `.github/workflows/ci.yml:428` | `Module wall guard` |
| `.github/workflows/ci.yml:429` | `check_module_wall.py --full-repo` |
| `.github/workflows/ci.yml:425` | `--changes 专属判词`（禁抄项 11.1 NEW-2 佐证） |
| `scripts/board_sync_parse.py:97` | `放行门单源=ruleset` |
| `scripts/board_sync_parse.py:114` | `GATE_TO_WORKFLOW` |
| `src/infra_core/governance.py:26` | `DEFAULT_PROTECTED_PATTERNS = (` |
| `src/infra_core/governance.py:33` | 保护面第七模式 `gen-crosswalk-table.py` |
| `src/infra_core/engine/droid_review/run_lead.sh:5` | 纪律机制头注起（轮数封顶） |
| `src/infra_core/engine/droid_review/run_lead.sh:6` | 软超时（timeout−400s 公式） |
| `src/infra_core/engine/droid_review/run_lead.sh:9` | 哨兵先行（写哨兵 → SIGTERM 组 → 宽限 → SIGKILL） |
| `src/infra_core/engine/droid_review/run_lead.sh:10` | 哨兵在案 = findings 不采信 |
| `src/infra_core/engine/droid_review/run_lead.sh:52` | LEAD_SOFT_TIMEOUT_SEC 默认值 |
| `src/infra_core/engine/droid_review/run_lead.sh:53` | LEAD_MAX_TURNS 默认值 |
| `src/infra_core/engine/droid_review/run_lead.sh:55` | LEAD_KILL_GRACE_SEC 默认值 |
| `src/infra_core/engine/droid_review/run_lead.sh:65` | 评论/发帖/PR 写/执行类工具不得进入 |
| `src/infra_core/engine/droid_review/run_lead.sh:67` | LEAD_ENABLED_TOOLS 白名单默认值 |
| `src/infra_core/engine/droid_review/run_lead.sh:282` | `kill -TERM "-$exec_pid"` |
| `src/infra_core/engine/droid_review/run_lead.sh:286` | `kill -KILL` |
| `src/infra_core/engine/droid_review/run_lead.sh:318` | LEAD_TOTAL_DEADLINE_EPOCH 绝对墙钟上限注释 |
| `src/infra_core/engine/droid_review/run_lead.sh:331` | 预算起点赋值 |
| `src/infra_core/engine/droid_review/run_lead.sh:349` | 重试预算计算 |
| `scripts/hardening_baseline.py:1` | 16 模块指纹基线工具头注 |
| `scripts/hardening_baseline.py:113` | file_sha256 定义 |
| `scripts/hardening_baseline.py:180` | payload_sha256 定义 |
| `scripts/hardening_baseline.py:303` | 对平实现 docstring |
| `scripts/hardening_baseline.py:388` | verify: OK 输出 |
| `docs/specs/key-registry.toml:2` | 钥匙总管理台账头注 |
| `docs/specs/key-registry.toml:7` | key-ledger.md append-only |
| `docs/specs/key-registry.toml:11` | 零密钥值铁律 |
| `docs/specs/key-registry.toml:14` | schema 一次定死铁律 |
| `docs/specs/key-registry.toml:25` | 定性词表（nature） |
| `docs/specs/key-registry.toml:29` | 状态词表 active 定义 |
| `docs/specs/key-registry.toml:38` | `schema_version = 1` |
| `docs/guides/exception-point-inventory.md:23` | 18 点清单标题 |
| `docs/guides/exception-point-inventory.md:27` | 普查表表头七字段 |
| `docs/guides/exception-point-inventory.md:94` | 结构性盲区（显式列出） |
| `evidence/step5-api-unification/closeout/01-closeout-pack.md:94` | VAL-M4-004 行（禁抄项 11.1） |
| `evidence/step5-api-unification/closeout/01-closeout-pack.md:97` | VAL-M4-007 行（禁抄项 11.1） |
| `evidence/step5-api-unification/closeout/05-risk-register.md:70` | R-29 行（禁抄项 11.2） |
| `tests/test_lead_engine.py:1041` | TestRunLeadBoundedExitE2E 类定义 |
| `tests/test_lead_engine.py:1044` | hang→soft_timeout 遗书断言（必死形态样本） |
| `tests/test_lead_engine.py:794` | fake droid 桩 mode="hang" 分支 |
| `tests/test_lead_engine.py:792` | 哨兵文件写入（sentinel_reason） |

> 锚随引擎仓 main 演化可能漂移；后续 feature 引用引擎形制时以本件快照口径为准，重核实以实读为准（本件快照时点 2026-11-27）。
