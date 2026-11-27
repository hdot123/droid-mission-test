# 结构化交接物 schema 设计（handoff-schemas 底稿）

> 底稿 2/2（mission F2/seat-gates 产出；主设计稿 §2 素材，被 §交接物全结构化 硬规则引用）。本件定义席位间四类交接物（worker-delta / verdict / plan-v2 / handoff）的目标态 JSON Schema：因果结论枚举化＋证据引用强制＋「未明」缺省＋证据对象构造权单源。门清单（席位能力授权面）见姊妹底稿 `seat-gates.md`（其 §1.3 `narrative-without-evidence` / `evidence-construct-violation` 两判词由本件 §6/§8 执法面承载）。
>
> **真源声明**：现状行号以 `docs/wall-v3/as-is-capability-inventory.md`（锚件 2）为准；形制要点以 `docs/wall-v3/form-basis.md`（锚件 1）为准。现状四件的非 schema 载体（脚本分类器/prompt 形状）已在 §0 逐件实读登记。本件全部 file:line 锚经实读核实（2026-11-27 快照）。
>
> **定位**：本件是设计底稿（schema 样例＋执法设计），零施工；施工落点＝schema 演进 v1→v2（§8 演进规则）＋契约测试同批（§7 形制锁）。

---

## §0 现状对位（交接物现状四件，非 schema 载体登记）

| 交接物 | 现状承载 | 现状形状 | 缺口 |
|---|---|---|---|
| worker-delta | `scripts/team/write_worker_delta.py`（上墙 `team.yml:836`） | JSON：`pid/result/cancel_reason/session_outcome/droid_exit_code/stream_tail_marker`（main() payload 结构） | 结局面齐（死因三字段机器分类），无因果叙事面；`session_outcome` 枚举 ok/wall_killed/job_wall_cancelled（classify_session_outcome `:45` 起枚举分支 `:63-75`；schema 枚举 `schemas/foreman-run.v1.schema.json:146-150`） |
| verdict | `scripts/team/salvage_verdict.py`（validator 逐件落盘；D-2 封章 `:121` sealed 粘性） | `verdict-partial.json`：`salvage_schema_version=validator-partial.v1/round/final/analyzed_count/processes[{id,verdict(pass|fail),reason}]/conflicts[{process,summary,evidence}]`（salvage_verdict() 返回结构 `:30-68`；CLI `--verdict pass|fail` choices） | verdict 仅二值枚举；`reason` 自由文本承载判定（违反「自由文本只给人看」）；evidence 字段无引用格式强制 |
| plan-v2 | replan 落单步（`team.yml:2420-2423`，机器校验：覆盖集/claim 不相交/受保护路径） | `team-plan-v2.json` changes 数组（脚本校验面，无 JSON Schema 载体） | 无 schema 文件；死因叙事含脚本内置推断（`team.yml:2259-2282`，F-1 文案 `:2278-2279`）且被 `tests/test_replan_context_and_skipped_outcome_r53c.py:190-206` 逐字钉住 |
| handoff | worker prompt 单源（`scripts/team/worker_prompt_template.py`，产物指令行） | `team/handoffs/<pid>.md` 自由 Markdown＋`team/status/<pid>.json`（键：id/title/state/files/checks） | handoff.md 无结构约束（自由文本给人看，合规）；status.json 无 schema 校验载体 |

**现状一句话**：结局面（发生什么）已有机器载体与枚举；**因果面（为什么）没有 schema**——死因叙事可由脚本推断或会话自述生成，无证据引用强制，无「未明」缺省。本件对象即此缺口（59 轮四问题①的 schema 层收口）。

---

## §1 总则（四原则，一次定死）

1. **因果结论枚举化**：因果结论类字段（死因/归因/冲突判定）只能是枚举值，自由文本禁止承载判定。
2. **证据引用强制**：凡因果结论字段非 `unknown` 者，必须挂 `evidence_refs`（非空数组，逐条指向证据对象 id）；`unknown` 时 `evidence_refs` 必须为空数组。
3. **「未明」缺省**：无证据时唯一合法取值 `unknown`（enum 显式成员）——不写=违约（required 强制），写枚举外值=schema 校验拒。
4. **自由文本不承载判定**：`reason`/`summary`/`note` 类字段只给人看；机器判定只读枚举与证据引用——两个判定通道物理隔离（字段级分离，非约定）。

**补卷覆盖面 ≠ 中性归因覆盖面**（现状口径沿用，锚件 2 §11）：交接物 schema 不因补卷器存在而放宽归因分支——补了卷不等于归因已中性化，`cause` 的中性枚举值只由机器死因事实（session_outcome/droid_exit_code/stream_tail_marker）驱动。

**证据对象与证据引用分离**：

- **证据对象（evidence object）**：`{ id, kind, origin, path, line?, sha256?, excerpt?, created_by }`——由核查环节构造（§6），落在证据登记文件（目标态 `work/evidence-index.json`）。
- **证据引用（evidence_ref）**：交接物内的 `"$eid:<id>"` 字符串——任何席位可引用已登记证据，但引用必须解析到已登记对象（悬挂引用=schema 校验拒，§3 通用约束）。

---

## §2 worker-delta v2 schema（死因因果面补齐）

现状 delta（§0 行 1）上墙机器死因三字段保留为结局面；v2 增加因果面（cause 枚举＋证据引用）与叙事面（自由文本给人看）：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "foreman/worker-delta.v2",
  "title": "worker-delta v2（工人席交接物：结局面+因果面+叙事面）",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "pid", "result", "session_outcome", "droid_exit_code", "stream_tail_marker", "cause", "evidence_refs", "narrative"],
  "properties": {
    "schema_version": { "const": "worker-delta.v2" },
    "pid": { "type": "string", "minLength": 1 },
    "result": { "enum": ["success", "failure", "cancelled"] },
    "cancel_reason": { "type": "string" },
    "session_outcome": { "enum": ["ok", "wall_killed", "job_wall_cancelled"] },
    "droid_exit_code": { "type": ["integer", "null"] },
    "stream_tail_marker": { "type": "boolean" },
    "cause": { "enum": ["self_completed", "wall_kill", "job_wall_cancel", "self_crash", "unknown"] },
    "evidence_refs": {
      "type": "array",
      "items": { "type": "string", "pattern": "^\\$eid:" },
      "description": "因果结论证据引用；cause=unknown 时必须为空数组"
    },
    "narrative": {
      "type": "string",
      "description": "自由文本，只给人看；机器判定不读本字段"
    }
  },
  "allOf": [
    { "if": { "properties": { "cause": { "const": "unknown" } } },
      "then": { "properties": { "evidence_refs": { "maxItems": 0 } } } },
    { "if": { "properties": { "cause": { "enum": ["self_completed", "wall_kill", "job_wall_cancel", "self_crash"] } } },
      "then": { "properties": { "evidence_refs": { "minItems": 1 } } } }
  ]
}
```

**枚举语义表**（cause 只增不改）：

| cause | 机器判据（谁构造） | 对位现状 |
|---|---|---|
| `self_completed` | delta 分类器：exit∈{0,1}＋stream 含 completion 事件（write_worker_delta.py:42 SELF_EXIT_CODES＋:86 区段 completion 扫描） | session_outcome=ok |
| `wall_kill` | delta 分类器：exit 124/137 或中断尾标（`:63-75` 分支；124/137=机器可证的 GNU timeout 杀印） | session_outcome=wall_killed |
| `job_wall_cancel` | delta 分类器：job cancelled（JOB_STATUS env 分支） | session_outcome=job_wall_cancelled |
| `self_crash` | delta 分类器：非零退出且无 completion（非 124/137 族，含 catch-all 码与未记录码） | 归责根治的死族分支（attribution_reason.py 非 124/137 分支措辞） |
| `unknown` | 无机器证据时唯一合法值——**不得推断** | 现状无此缺省（四问题①缺口） |

**构造权**：cause/evidence_refs 由机器分类步（write_worker_delta 演进体）构造；会话（droid exec 进程）无 cause 构造入口——会话只能产 narrative（自由文本），不产因果字段。

### 2.1 违约负例（验收线素材，每条常驻 pytest 负例设计）

| # | 违约注入 | 期望 |
|---|---|---|
| W-1 | cause=unknown 且 evidence_refs 非空 | schema 校验拒 |
| W-2 | cause=wall_kill 且 evidence_refs 空 | schema 校验拒 |
| W-3 | cause="F-1 检查拒绝"（枚举外自由值） | schema 校验拒 |
| W-4 | cause 缺席（required 违约） | schema 校验拒 |
| W-5 | evidence_ref="$eid:nonexistent"（悬挂引用） | 解析校验拒（§3） |
| W-6 | 会话进程写 cause 字段（构造权违约） | evidence-construct-violation 红（§6） |

---

## §3 verdict v2 schema（验收席判定：枚举+证据强制+未明缺省）

现状 verdict-partial（§0 行 2）的 pass|fail 保留；v2 每判定挂证据引用、冲突升级挂冲突枚举、整体结论带未明缺省：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "foreman/verdict.v2",
  "title": "verdict v2（验收席交接物：判定+证据引用+冲突升级）",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "round", "final", "judged", "conflicts", "overall"],
  "properties": {
    "schema_version": { "const": "verdict.v2" },
    "round": { "type": "integer" },
    "final": { "type": "boolean", "description": "D-2 封章（粘性，沿现状 salvage_verdict.py:121 sealed 语义）" },
    "judged": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["id", "verdict", "cause", "evidence_refs", "reason"],
        "properties": {
          "id": { "type": "string", "minLength": 1 },
          "verdict": { "enum": ["pass", "fail"] },
          "cause": { "enum": ["checks_red", "evidence_incomplete", "out_of_card_conflict", "aligned_pass", "unknown"] },
          "evidence_refs": { "type": "array", "minItems": 1, "items": { "type": "string", "pattern": "^\\$eid:" } },
          "reason": { "type": "string", "description": "自由文本，只给人看；引用证据用 $eid: 标记，机器判定不读本字段" }
        }
      }
    },
    "conflicts": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["process", "kind", "evidence_refs", "summary"],
        "properties": {
          "process": { "type": "string", "minLength": 1 },
          "kind": { "enum": ["out_of_card_write", "work_order_mismatch", "evidence_tampering", "other"] },
          "evidence_refs": { "type": "array", "minItems": 1, "items": { "type": "string", "pattern": "^\\$eid:" } },
          "summary": { "type": "string", "description": "自由文本" }
        }
      }
    },
    "overall": {
      "type": "object",
      "additionalProperties": false,
      "required": ["verdict", "cause", "evidence_refs"],
      "properties": {
        "verdict": { "enum": ["pass", "fail", "unknown"] },
        "cause": { "enum": ["all_processes_judged", "blocked_missing_evidence", "machine_records_disagreement", "unknown"] },
        "evidence_refs": { "type": "array", "items": { "type": "string", "pattern": "^\\$eid:" } }
      }
    }
  }
}
```

**枚举语义表**：

| 字段 | 枚举 | 语义 |
|---|---|---|
| judged[].cause | `checks_red` | 红章判死（对位 prompt 单源 :97 行 HARD RULE：红章永不 pass，机器构造） |
| | `evidence_incomplete` | 料不齐（legacy「缺件」语义枚举化） |
| | `out_of_card_conflict` | 卡外冲突（:98 行冲突升级纪律枚举化） |
| | `aligned_pass` | 证据对齐通过（:97 行「alignment proves honesty, not pass」的通过面） |
| | `unknown` | 证据不足不出判定（V-3 纪律枚举化） |
| conflicts[].kind | `out_of_card_write` | 卡外写 |
| | `work_order_mismatch` | 单卡不符 |
| | `evidence_tampering` | 证据篡改嫌疑（manifest sha 复验面） |
| | `other` | 其他（summary 必填说明） |
| overall.verdict | `pass`/`fail`/`unknown` | **unknown=验收席合法终局**：judgeable 集不可判时不得强行二值 |

**约束继承现状执法面**：D-2 封章粘性（salvage_verdict.py:121 sealed 粘性沿用）；红章判死（:97）；冲突升级必录（:98）；pytest 计数单源 check-summary.json（:100）——四条纪律全部进入 v2 契约测试（§7）。

### 3.1 违约负例

| # | 违约注入 | 期望 |
|---|---|---|
| V-1 | judged[].cause=unknown 且 evidence_refs 非空 | 拒 |
| V-2 | judged[].cause=checks_red 且 evidence_refs 空 | 拒 |
| V-3 | verdict="pass with concerns"（枚举外） | 拒 |
| V-4 | conflicts[].evidence_refs 空 | 拒 |
| V-5 | overall.verdict=unknown 且 evidence_refs 非空 | 拒 |
| V-6 | reason 内写 "verdict": "pass" 试图以叙事承载判定 | 机器判定不读 reason——不构成绕过（负面测试断言判定通道只读枚举字段） |

---

## §4 plan-v2 v1 schema（改计划席：死因注入面枚举化）

现状 team-plan-v2（§0 行 3）落单步已有机器校验（覆盖集/claim 不相交/受保护路径）；v1 schema 把**死因注入面**（replan prompt 的 outcome panel 输入）与 changes 数组一并 schema 化，废除脚本内置推断：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "foreman/plan-v2.v1",
  "title": "plan-v2（改计划席交接物：changes+死因注入面）",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "issue_number", "death_facts", "changes"],
  "properties": {
    "schema_version": { "const": "plan-v2.v1" },
    "issue_number": { "type": "integer" },
    "death_facts": {
      "type": "array",
      "description": "死因注入面：逐 pid 一条，来源=墙上机器记录（workers by-pid 三映射）或 delta；本数组由机器步构造，replan 会话只读",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["pid", "session_outcome", "cause", "evidence_refs", "note"],
        "properties": {
          "pid": { "type": "string", "minLength": 1 },
          "session_outcome": { "enum": ["ok", "wall_killed", "job_wall_cancelled", "not_recorded"] },
          "cause": { "enum": ["self_completed", "wall_kill", "job_wall_cancel", "self_crash", "f1_rejected_machine_confirmed", "unknown"] },
          "evidence_refs": { "type": "array", "items": { "type": "string", "pattern": "^\\$eid:" } },
          "note": { "type": "string", "description": "自由文本" }
        },
        "allOf": [
          { "if": { "properties": { "cause": { "enum": ["unknown"] } } },
            "then": { "properties": { "evidence_refs": { "maxItems": 0 } } } },
          { "if": { "properties": { "cause": { "enum": ["self_completed", "wall_kill", "job_wall_cancel", "self_crash", "f1_rejected_machine_confirmed"] } } },
            "then": { "properties": { "evidence_refs": { "minItems": 1 } } } }
        ]
      }
    },
    "changes": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["op", "target", "claim", "reason"],
        "properties": {
          "op": { "enum": ["add_process", "revise_process", "drop_process"] },
          "target": { "type": "string" },
          "claim": { "type": "string", "description": "受保护路径校验沿用现状落单步机器闸" },
          "reason": { "type": "string", "description": "自由文本；若引用死因事实必须挂对应 death_facts.pid" }
        }
      }
    }
  }
}
```

**f1_rejected_machine_confirmed 与现状推断的区别**：现状文案「F-1 检查拒绝」由分支缺席**推断**（无机器记录佐证，`team.yml:2276-2279`）；v2 的该枚举值**只能由机器守卫记录构造**——F-1 拒绝事件必须在发生时即登记证据对象（§6 机器证据构造方），分支缺席＋无 F-1 证据＝`unknown`（分支缺席本身不是死因，是缺料事实）。**钉子反转**见 §9.2。

### 4.1 违约负例

| # | 违约注入 | 期望 |
|---|---|---|
| P-1 | death_facts[].cause=f1_rejected_machine_confirmed 且证据对象 origin≠machine_guard | 构造权拒（§6） |
| P-2 | 死因叙事含字面「F-1 check rejected」而 cause=unknown | narrative-without-evidence 红（§9.2 钉子反转断言） |
| P-3 | changes[].reason 引用不存在 pid 的死因 | 拒 |
| P-4 | death_facts 缺席（required） | 拒 |

---

## §5 handoff v1 schema（工人席交接束：结构化骨架+自由文本分层）

现状 handoff.md（自由文本给人看，合规保留）＋status.json（无校验载体，收口）；v1 定义 status 面的 schema，handoff.md 保持 Markdown 但**引用结构化字段必须走 status.json**：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "foreman/handoff.v1",
  "title": "handoff（工人席交接束：status 结构面+handoff 文本面）",
  "type": "object",
  "additionalProperties": false,
  "required": ["schema_version", "id", "title", "state", "files", "checks"],
  "properties": {
    "schema_version": { "const": "handoff.v1" },
    "id": { "type": "string", "minLength": 1 },
    "title": { "type": "string" },
    "state": { "enum": ["in_progress", "done", "blocked"] },
    "files": { "type": "array", "items": { "type": "string", "description": "交付文件路径（F-1 allowed 集合子集，越界路径=F-1 拒后此处不得出现）" } },
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["command", "result"],
        "properties": {
          "command": { "type": "string" },
          "result": { "enum": ["pass", "fail", "skipped", "not_run"] }
        }
      }
    }
  }
}
```

**分层纪律**：判定性事实（做了/没做/检查结果）只在 status.json（schema 面）；handoff.md 是给人看的叙述面，机器判定不读 handoff.md。工人席自述的因果叙事（若写）只能进 delta 的 narrative 字段或 handoff.md，**永远不进 cause/evidence 字段**（构造权 §6）。

### 5.1 违约负例

| # | 违约注入 | 期望 |
|---|---|---|
| H-1 | state="完成"（枚举外中文自由值） | 拒 |
| H-2 | checks[].result="ran but failed"（枚举外） | 拒 |
| H-3 | files 含卡外路径（F-1 拒过的文件） | F-1 拒＋out-of-scope-write 双红 |

---

## §6 证据对象：构造权单源（核查环节构造）

**铁律**：证据对象只能由**核查环节**构造。领班域的核查环节白名单（一次定死，只增不改）：

| 构造方 | 可构造的证据 kind | 机器/会话 |
|---|---|---|
| 机器守卫步（F-1、caps-gate、budgets lint、delta 分类器） | `machine_guard_record` | 机器 |
| 验收席 validator 会话（经 recorder 工具落盘） | `validator_judgement` | 会话（核查席） |
| prep 补卷器 | `salvage_record` | 机器 |
| adopt/采认步 | `adopt_record` | 机器 |

lead / worker / replan / assemble 会话**无构造入口**：包装器不向这些会话暴露证据登记通道；交接物内这些席位产出的 `evidence_refs` 只能指向已登记对象（§1 引用/对象分离）。引用非构造——引用他人证据合法，自造证据对象违约。

**证据对象形状**（登记在目标态 `work/evidence-index.json`，append-only）：

```json
{
  "id": "eid-000123",
  "kind": "machine_guard_record",
  "origin": "f1|caps_gate|budgets_lint|delta_classifier|validator|salvage|adopt",
  "path": ".github/workflows/team.yml",
  "line": 731,
  "sha256": "…（证据文件指纹）",
  "excerpt": "git reset --soft …（≤200 字符）",
  "created_by": "machine_guard_step:commit_boundary",
  "created_at_wall_ref": "run_id/job/step（墙引用，非时戳）"
}
```

确定性纪律（对位引擎封印形制 form-basis 要点 8：无时戳、无绝对路径、同 tree 重跑可复演）：`created_at` 不用墙钟时戳，用墙引用（run_id/job/step）；path 相对仓根；sha256 逐文件指纹。

**构造权执法**：caps-gate `evidence-construct-violation` 判词（seat-gates §1.3）——交接物携带 `evidence-index.json` 变更而变更者不在核查环节白名单（机器步指纹/validator 会话标识对不上）即红；包装器对非核查席会话零登记通道（能力面执法，seat-gates §4.3）。

---

## §7 形制锁（schema 演进纪律，照抄引擎同批改锁）

1. **schema 一次定死＋同批改锁**（form-basis 要点 3，铁律对位 `docs/specs/key-registry.toml:14-16`）：四 schema 的枚举词表与 required 键集硬编码在契约测试（目标态 `tests/test_handoff_schema_contract.py`）；增删枚举/键必须同批改契约测试，禁止 schema 单边漂移。
2. **负对照共用生产校验路径**：负例（各节违约表）与生产校验用同一 jsonschema 校验器实现——测试红即生产红，牙齿一致（对位引擎 `tests/test_module_capabilities_contract.py` 负对照形制）。
3. **判词只增不改**：§2/§3/§4/§5 枚举词表只增不改；改名/删枚举值即破坏下游采认（对位判词纪律要点 4）。
4. **演进规则（v1→v2→…）**：schema_version 常量随之递增；旧版本读取兼容窗口一次裁定期（大哥裁），窗口外旧版本拒收——不做无限兼容。
5. **采认对位**：verdict/plan-v2 的采认链沿用现状 fail-closed pick 与 adopt 面（`team.yml:1721` run_adopt_step、`:4420` pick_verdict_from_wall）——schema 演进不放松采认 fail-closed 语义。

---

## §8 执法接线（谁校验、在哪校验、红了怎么办）

| 校验点 | 校验物 | 判词/后果 |
|---|---|---|
| 上墙合并步（workers-wall-merge `:885` merge_worker_deltas 演进体） | worker-delta v2 | schema 校验拒＝该 delta 不入墙并集（prep 门按缺 delta 走既有缺件路径） |
| adopt 采认步（`:1721` run_adopt_step 演进体） | verdict v2 | 校验拒＝不采认（fail-closed，链 result=failure） |
| replan 落单步（`:2420-2423` 机器校验演进体） | plan-v2 v1 | 校验拒＝不落单（无 v2 子单产生） |
| prep 门（`:860` prep_should_run 面） | status/handoff v1 | 校验拒＝该 pack 缺件（走补卷守卫四条件判定） |
| caps-gate（seat-gates §1.3） | 全部交接物＋证据登记文件 | narrative-without-evidence / evidence-construct-violation 红 |
| CI 恒跑 | 契约测试族（§7） | 负例全绿＝执法在岗；接线锁断言校验步恒跑（零 if 零 continue-on-error） |

**缺席即事件**（对位硬规则⑥）：必交交接物窗口内未出现＝告警事件（墙上计数面）——recorder 调用数（seat-gates §2.7 probes）、delta 缺席（现状 prep 缺件路径已有）、verdict-partial 缺席（52B 后逐件落盘＋D-2 封章；封章缺席＝round 重验，现状 :79 行纪律沿用）。

---

## §9 59 轮四问题①专项收口（死因叙事证据化）

### 9.1 机制根因（现状，锚件 2 §10-①）

replan 步 heredoc 由「分支缺席」**推断**「F-1 检查拒绝」死因（`team.yml:2259` 注释起、`:2276` branch_present 判定、`:2278-2279` F-1 文案赋值）；F-1 拒绝的真实机器记录（worker job 日志一行）从不进 replan 输入面——叙事无佐证。

### 9.2 设计收口（三件套）

1. **枚举+证据强制**：死因只能取 §4 cause 枚举；非 `unknown` 必挂证据引用；`f1_rejected_machine_confirmed` 只能由机器守卫记录构造（§6 origin=machine_guard_record/f1）。
2. **「未明」缺省**：分支缺席＋无 F-1 机器证据＝`unknown`——分支缺席是缺料事实不是死因；replan 拿到 unknown 时按缺料处理（补卷守卫四条件判定），不输出任何死因断言。
3. **钉子反转**：现状契约测试把推断文案钉成正确行为（`tests/test_replan_context_and_skipped_outcome_r53c.py:190` 测试定义、`:198-202` 逐字行、`:205` count==1 断言）。施工时同批反转（schema 演进与测试同批改锁，§7.1）：断言改为——①死因面 cause 枚举校验；②prompt 含「F-1 check rejected」字样当且仅当存在 origin=f1 的机器证据对象；③cause=unknown 时 prompt 死因面板呈现「未明（无机器证据）」。反转后该文案回归其真值条件：**机器证实才可说，否则未明**。

**归责分支对位**：attribution_reason.py 现状按 124/137 分支措辞（UT-M3-001 口径）——v2 delta 的 cause 枚举与其分支一一映射（wall_kill↔124/137 措辞、self_crash↔非机器判定措辞），归责模板演进为读枚举渲染，措辞字符串由模板单源（不散布）。

---

## 附：本件 file:line 锚清单

| 锚 | 解析判据（该行应含） |
|---|---|
| `team.yml:836` | `write_worker_delta` |
| `team.yml:885` | `merge_worker_deltas` |
| `team.yml:860` | `prep_should_run` |
| `team.yml:1223` | `worker_salvage`（接线区段起） |
| `team.yml:1515` | `build_validator_prompt` |
| `team.yml:1721` | `run_adopt_step` |
| `team.yml:2141` | `replan:`（job 头） |
| `team.yml:2259` | `Round-53 fix`（推断注释起） |
| `team.yml:2276` | `branch_present`（判定行） |
| `team.yml:2278` | `the round-1 branch for process`（F-1 文案赋值行） |
| `team.yml:2420` | 落单步（步名/机器校验区段起） |
| `team.yml:4420` | `pick_verdict_from_wall` |
| `scripts/team/write_worker_delta.py:29` | STREAM_INTERRUPT_MARKER |
| `scripts/team/write_worker_delta.py:42` | SELF_EXIT_CODES |
| `scripts/team/write_worker_delta.py:45` | classify_session_outcome |
| `scripts/team/salvage_verdict.py:18` | PARTIAL_NAME |
| `scripts/team/salvage_verdict.py:30` | salvage_verdict 定义 |
| `scripts/team/salvage_verdict.py:60` | salvage_schema_version（validator-partial.v1） |
| `scripts/team/salvage_verdict.py:121` | sealed 粘性 |
| `scripts/team/attribution_reason.py`（模块锚） | blocked_reason / neutral_attribution |
| `scripts/team/validator_prompt_template.py:97` | 红章判死 HARD RULE |
| `scripts/team/validator_prompt_template.py:98` | 冲突升级必录 |
| `scripts/team/worker_prompt_template.py:66` | handoffs/status 产物指令 |
| `scripts/team/worker_prompt_template.py:67` | status.json 键面 |
| `schemas/foreman-run.v1.schema.json:146` | session_outcome_by_pid |
| `schemas/foreman-run.v1.schema.json:153` | droid_exit_code_by_pid |
| `schemas/foreman-run.v1.schema.json:157` | stream_tail_marker_by_pid |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:190` | 钉子测试定义 |
| `tests/test_replan_context_and_skipped_outcome_r53c.py:205` | count==1 断言 |
| 引擎：`docs/specs/key-registry.toml:14` | schema 同批改锁铁律（转引 form-basis） |
| 引擎：`tests/test_module_capabilities_contract.py:159` | v4 词表只增不改注释区段（转引 form-basis） |

> 锚随树演化可能漂移；重核实以实读为准（本件快照 2026-11-27）。
