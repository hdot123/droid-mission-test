# 面墙 API 设计稿 v3.0 · 三席对抗审查报告

| 字段 | 值 |
|---|---|
| 审查形式 | **三席独立对抗审＋独立终审收敛**（三席互不读对方产出；终审席位与三席载体不同源） |
| 审查对象版本 | `main` @ `4f4c53a`（#975 合入时点：主稿＋7 锚件＋398 例设计契约测试） |
| 审查对象 | `docs/领班制-面墙API设计稿-v3.md`（429 行）逐章＋`docs/wall-v3/` 7 锚件逐件 |
| 引擎锚基准 | `infraro-core` 钉树 `460922c`（全部经 `git show 460922c:<path>` 实读，未读引擎 main） |
| 三席阵容 | 席位一 `glm53-worker`（GLM-5.3，论证链与结构）；席位二 `sonnet-auditor`（Sonnet 5.5，锚与事实对质，file:line 级证据）；席位三 `ds4-auditor`（预算数字对质、执法设计可实现性、SL 桩可证伪性——席位三实际由 `glm53-worker` 兼任，用户 2026-11-28 裁定，产出文件名保留 seat-ds4） |
| 终审席位 | `glm54-auditor`（GLM-5.4，与三席载体不同源；对 15 项编号发现逐项回读原物裁决） |
| 独立性声明 | 三席派发时互不知晓他席存在与产出路径，三份席位报告经文本检查零交叉引用（`seat-glm53`/`seat-sonnet`/`seat-ds4` 互不含他席文件名）；席位三与席位一同载 GLM-5.3，两席间独立性由「互不读对方产出」的派发纪律保证，其对同一缺陷（DS4-01／GLM53-04）的独立命中计为「一模型两实例」佐证强度；终审为唯一可见三席全貌者，且对每项发现的核心锚独立回读原物取证，不以席位文本为证据 |
| 分档口径 | 阻断＝照稿施工会产生错误墙／假绿／执法缺位或契约矛盾；非阻断＝表述失真／指针陈旧／残留不一致，不影响施工正确性但施工前应清理；建议＝可选改进 |
| 本交付 | **仅增本文档＋一行 README 对抗审交付段**；零 workflow/scripts/schemas/测试/设计稿改动；零密钥值（secret 只记名）；发现只分级记录，本报告不修设计稿——处置属批后施工 mission |

---

## 1. 三席发现（15 项编号发现，每项五字段：编号／描述／证据／复现路径／自评级）

### 1.A 席位一（GLM-5.3，论证链与结构）—— 7 项

#### GLM53-01（复核维持登记项：NB-3 锚区间截短）

- **编号**：GLM53-01（复核维持登记，非新发现）
- **描述**：NB-3 复核确认仍成立——as-is-capability-inventory.md:91 的锚区间截短（四条件 docstring 实际延伸远超所记区间）与 :118（docstring 收尾实位与所记区间不符）两处未修。
- **证据**：`docs/wall-v3/as-is-capability-inventory.md:91`「锚：`scripts/team/worker_salvage.py:13`（「The guard is machine-judged and fail-closed; ALL of:」）、`:14-15 区间`（四条件逐条 docstring）」；`:118` 记 `worker_salvage.py:1-45`（docstring 产品纪律）。终审实读 `worker_salvage.py`：条件 1 在 :14、条件 2 在 :15、条件 3 跨 :16-:23、条件 4 跨 :24-:30，docstring 收尾 `"""` 在 :64——`:14-15` 只覆盖前两条，`:1-45` 落在 Products 段中间。
- **复现路径**：Read `docs/wall-v3/as-is-capability-inventory.md` 行 91 与 118；Read `scripts/team/worker_salvage.py` 行 13-64 对照。
- **自评级**：非阻断（沿用上使命登记档级；指针可解析、方向正确）。

#### GLM53-02（复核维持登记项：NB-4 之 Annexe A 行级不一致）

- **编号**：GLM53-02（复核维持登记，非新发现）
- **描述**：NB-4 之 Annexe A env-check 行号不一致复核确认仍成立——out-of-graph 附A 记 `env-check.yml:194`（S_PROJECTS_STATE_PAT 板面探测消费），实读 :194 为条件行、展开消费行在 :195；同件 :278（TOML 样例）写 :195、:452（附A 表）写 :194，两行级口径并存。
- **证据**：`docs/wall-v3/out-of-graph-artifacts.md:452`（附A 表写 :194）对 `:278`（TOML 样例写 :195）；实读 `env-check.yml:194`＝`if [ -n "${S_PROJECTS_STATE_PAT:-}" ]; then`、`:195`＝`PROJECT_TOKEN="$S_PROJECTS_STATE_PAT"`。主稿 §3.3/§3.4 已按 `:194-200` 区段口径表述，行级口径不一确认成立。
- **复现路径**：`sed -n '194,195p' .github/workflows/env-check.yml`；Read `docs/wall-v3/out-of-graph-artifacts.md` 行 278 与 452 对比。
- **自评级**：非阻断（区段级锚语义正确，行级口径残留不一致）。

#### GLM53-03

- **编号**：GLM53-03
- **描述**：主稿 §0b 表 NEW-1 行执法设计列复述全树口径写「全生产 workflow 树」，与 §8 待裁决清单项 3 及 §3.2/§3.4 的「12 文件/6 名/82 行」计数口径粗细不一（应两处同为带计数的全树口径；属表述粗细漂移，非事实矛盾——两者指同一扫描面，复算吻合）。
- **证据**：席位锚定主稿 :23（§0b NEW-1 行执法设计列）；主稿 §8 项 3（:413 区段）「全树实测 12 文件/6 名/82 行」；实测复算 `grep -n 'secrets\.' .github/workflows/*.yml | wc -l`＝82、文件数 12、六名分计吻合。
- **复现路径**：Read 主稿 :23 与 :407-:422；在 repo 根跑 `grep -n 'secrets\.' .github/workflows/*.yml | wc -l` 与 `grep -l 'secrets\.' .github/workflows/*.yml | wc -l`。
- **自评级**：非阻断（不影响施工正确性；施工前统一措辞即可）。

#### GLM53-04

- **编号**：GLM53-04
- **描述**：主稿 §2.2 validator 行与 seat-gates §2.4 的 budgets 预设样例将 job 墙定为 15m（「job_wall_min=15 job 墙（软超时公式基座）」「软超时 500」），但在树预算契约真源 `default_budgets()` 的 validator `job_wall_min`＝12，且 `budget_resolve.py:57-59` 注释明文「ForemanRun budgets.roles.validator.job_wall_min (12) is the contractual slice…GitHub Actions timeout-minutes: 15 is a wider platform job envelope; do not conflate them」——样例把「契约切片 12」与「平台 envelope 15」混同，与在树注释纪律相抵。
- **证据**：主稿 :148（§2.2 validator 行，`job_wall_min`=15 ＋ `soft_timeout_sec`=500）；seat-gates.md:280 `job_wall_min = 15`、:282「基座对平现状 workflow job envelope（team.yml:1387 timeout-minutes: 15）」；实读 `scripts/team/foreman_run_lib.py:42-46`（validator 块 `"job_wall_min": 12`）与 `scripts/team/budget_resolve.py:57-59`。
- **复现路径**：`sed -n '42,46p' scripts/team/foreman_run_lib.py`；`sed -n '57,59p' scripts/team/budget_resolve.py`；`sed -n '148p' docs/领班制-面墙API设计稿-v3.md`；Read seat-gates §2.4 budgets 注释块。
- **自评级**：非阻断（样例自称「对平现状 workflow job envelope」在字面层成立，但对平对象选了宽口径；施工前应清理的对平口径失真）。

#### GLM53-05

- **编号**：GLM53-05
- **描述**：主稿 §3.2 表内两处自指指针（「见本节表③行」「见主设计稿 §图外件」）在表格语境下不可解析——读者按「③行」找行时无稳定定位面。属表述结构问题，不改事实（指向目标存在）。
- **证据**：席位锚定主稿 :232/:238（§3.2 表件②/件③行单元格）。
- **复现路径**：Read 主稿 :225-:245（§3.2 表），尝试按「表③行」定位目标行。
- **自评级**：建议（可读性/可维护性改进；不产生错误施工）。

#### GLM53-06

- **编号**：GLM53-06
- **描述**：主稿 §1.2 十要点表的「引擎原物锚」列以「引擎仓相对路径」给锚，表内与列头未自带「按钉树 460922c 读」限定——钉树口径住头部锚纪律条款与 §0b，单看表格的读者需跳两跳才能拿到读法；并以「引擎 main 与钉树间已有一行之差」为实证建议表注补读法限定。
- **证据**：主稿 :62-:73（§1.2 表列头「引擎原物锚（引擎仓相对路径）」）；席位宣称 `exception-point-inventory.md` #3 行在钉树为 :31、在引擎工作树读为 :30（同内容随树差一行）。
- **复现路径**：`git -C <引擎仓检出目录> show 460922c:docs/guides/exception-point-inventory.md | sed -n '30,31p'`，再与引擎工作树同文件 :30-:31 对比。
- **自评级**：建议（防误读加固；钉树口径本身已在头部与 §0b 正确声明）。

#### GLM53-07

- **编号**：GLM53-07
- **描述**：§1.1 推论 3「无兜底」的判据面声明为「体外执法失败……是墙建成失败（§6.1 四条活验数字判据）」，但 §6.1 四条数字判据中并无一条直接度量「体外执法失败」（如监督者自身崩溃、哨兵写失败）——推论 3 的支撑指针比其宣称的覆盖面窄，属轻断链。
- **证据**：主稿 :56（推论 3）；:315-:318（§6.1 四条：全红率／延迟上界／不采信率／缺席报警触发率——被测对象都是违约会话/缺席注入，无「执法体自身失败」直接条目）。
- **复现路径**：Read 主稿 :48-:60 与 :311-:323 对照。
- **自评级**：建议（论证补强；席位原建议由 SL-1/SL-3 断言承载，终审核验该建议不成立——见 §2 裁决）。

### 1.B 席位二（Sonnet 5.5，锚与事实对质）—— 3 项

#### SONNET-1

- **编号**：SONNET-1
- **描述**：handoff-schemas.md:197 一行里「红章判死（:97）；冲突升级必录（:98）；pytest 计数单源 check-summary.json（:100）」三个裸锚紧跟 `salvage_verdict.py:121` 之后，按就近原则读作同一文件，但该文件 :97/:98/:100 是函数调用实参，无红章/冲突升级/计数单源内容；作者本意应指 `validator_prompt_template.py`。另该句自称「现状执法面」，而其中两条仅是 prompt 文字纪律（as-is:61 自述「无运行时效力」），红章的代码执法面实际在 `adopt_verdict.py`。
- **证据**：实读 `scripts/team/salvage_verdict.py:96-102`（:97 `work_dir,`／:98 `analyzed={...},`／:100 `round_num=round_num,`，均为实参）；实读 `scripts/team/validator_prompt_template.py:97`「HARD RULE — a red mandated check is never a pass…」、:98 conflicts 必录、:100 Authoritative counts——三行语义逐一吻合；代码执法面 `scripts/team/adopt_verdict.py:85-:93`（注释引 HARD RULE）、:98 `_gate_red_reason`、:138 `machine_gate_reds`。
- **复现路径**：`sed -n '197p' docs/wall-v3/handoff-schemas.md`；`sed -n '96,102p' scripts/team/salvage_verdict.py` 与 `sed -n '97,100p' scripts/team/validator_prompt_template.py` 对照。
- **自评级**：非阻断（被引三条纪律在 failure-specs.md:76/:125 等处有正确全路径锚；任何按「锚可解析＝文件在树、行号不越界、含预期关键词」做的锚检查会在该行报红，修一处文字即可）。

#### SONNET-2

- **编号**：SONNET-2
- **描述**：handoff-schemas.md:84（`self_completed` 行）写 completion 扫描在 `write_worker_delta.py:86 区段`，实读 :86 是 `try:`，属中断尾标解析函数（语义相反）；completion 扫描函数 `_stream_has_completion_event` 定义在 :98、调用点 :72。:42 与 :63-75 两锚吻合。
- **证据**：`scripts/team/write_worker_delta.py:42`（`SELF_EXIT_CODES = (0, 1)`）、:70-:72（调用）、:78-:95（中断解析 `_is_interrupt_event`，:86 在其体内）、:98-:101（completion 函数）。
- **复现路径**：`sed -n '80,101p' scripts/team/write_worker_delta.py`。
- **自评级**：建议（「区段」一词留有余地，但 :86 所在函数语义相反，锚应改指 :98 或 :72）。

#### SONNET-3

- **编号**：SONNET-3
- **描述**：as-is-capability-inventory.md:143（§9 第 5 条）「PAT 只在两处：assemble 写板（team.yml:4431）与 env-check 探板（env-check.yml:86）」与实情不吻合，且与本件自身相矛盾——全树实读 `secrets.PROJECTS_STATE_PAT` 共 8 处展开；本件 :133 自己已列 S_PROJECTS_STATE_PAT 注入、姊妹件 out-of-graph :181/:186 已登记 env-check 墙步 `:238-240` 再展开、:332 台账⑤已按全树 8 行登记。
- **证据**：`grep -n 'secrets\.PROJECTS_STATE_PAT' .github/workflows/*.yml` 实测 8 行：env-check.yml :86、:240；i8-zero-escape-live-orchestrator.yml :102/:184/:258/:310/:347；team.yml :4431。as-is 自身矛盾位：:133（五 secrets 全部进入本 job 环境，含 S_PROJECTS_STATE_PAT，锚 env-check.yml:82-86）。
- **复现路径**：同上 grep；`sed -n '236,241p' .github/workflows/env-check.yml`；对照 as-is :143 与 :133。
- **自评级**：非阻断（下游凭证台账与对账判据已采用全树 8 行口径；但若施工者按 as-is:143 当「PAT 消费点全集」去做收口，会漏 env-check :240 与编排器五处）。

### 1.C 席位三（预算对质／执法可实现性／SL 桩可证伪性）—— 5 项

#### DS4-01

- **编号**：DS4-01
- **描述**：validator `job_wall_min` 预算键值契约侧与单源真源不吻合——应是 12（单源 `default_budgets()` 与 budgets lint 双锁），实是主稿与 seat-gates 把 GitHub job envelope 的 15 写成该键值（15 为平台 envelope，budget_resolve.py 注释明文「do not conflate」）。软超时公式基座两说（按 15→500s，按 12→320s，分歧 180s）。
- **证据**：单源侧 `scripts/team/foreman_run_lib.py:45` `"job_wall_min": 12`（validator 段）；执法侧 `scripts/team/lint_workflow_budgets.py:95-97` `vmin = default_budgets()...get("job_wall_min")`＋`"wall validator job_wall_min must stay 12 (contractual slice)"`；口径仲裁 `scripts/team/budget_resolve.py:57-60`。契约侧失真处：主稿 :148；seat-gates.md:280＋:281 注释；seat-gates §3.3 budgets 表「job 墙（15/15/15m，team.yml:59/:1387/:2154）」。
- **复现路径**：`sed -n '42,47p' scripts/team/foreman_run_lib.py`；`sed -n '95,103p' scripts/team/lint_workflow_budgets.py`；`sed -n '57,60p' scripts/team/budget_resolve.py`；`grep -n 'job_wall_min' docs/领班制-面墙API设计稿-v3.md docs/wall-v3/seat-gates.md`。
- **自评级**：非阻断——现状下 lint 只锁 12、envelope 15 不进预算消费，照稿施工若以契约侧 15 覆写将立即触发 budgets lint 红，错误在 CI 首跑即暴露，不会产出错误墙或假绿；但施工者可能改 lint 而非改契约，把「契约切片」语义改坏——施工前必须统一该键值叙事，列非阻断首位。

#### DS4-02

- **编号**：DS4-02
- **描述**：主稿 §2.2 prep 段「步级超时 600s/300s 入 budgets 键」登记不全——现状 prep/prep2 帧装超时按版本注记 (E) 共含「other calls 120s／pip install 300s／per-process checks 300s／full pytest 600s」多层，契约侧（seat-gates :232-234 仅三键）漏登 120s 层；按 default-deny「登记即全集」口径，未登记者照稿不可判。
- **证据**：主稿 §2.2 prep 段「步级超时 600s/300s 入 budgets 键」；`docs/wall-v3/seat-gates.md:232-234` 仅 `pytest_timeout_sec = 600 / checks_timeout_sec = 300 / job_wall_min = 20`；`.github/workflows/team.yml:10` 版本注记 (E)；树内实读 :1004 `PIP_TIMEOUT = 300`、:1005 `PYTEST_FULL_TIMEOUT = 600`、:1006 `CHECK_TIMEOUT = 300`、:1106/:1114 `timeout=60`。
- **复现路径**：`grep -n '步级超时 600s/300s' docs/领班制-面墙API设计稿-v3.md`；`sed -n '232,234p' docs/wall-v3/seat-gates.md`；`sed -n '10p' .github/workflows/team.yml`。
- **自评级**：建议——不影响执法正确性（300/600 两主层已登记且与现状吻合），属预算登记面完整性欠缺。

#### DS4-03

- **编号**：DS4-03
- **描述**：INV-1/SL-8a 的「首步窗口」判定窗口未量化——「首步窗口=会话开始后首个分析单元内」中「分析单元」无机器定义，窗口截止时点不可计算，该子断言当前不可判红绿（全程窗口=budgets.droid_wall_sec 可判，不受影响）。
- **证据**：主稿 :303（§5.2 INV-1「首步窗口＋全程窗口」）与 `docs/wall-v3/acceptance-line-map.md:378`、`docs/wall-v3/seat-gates.md:426`、`docs/wall-v3/failure-specs.md:132`——四处同文均未给量化参数；`grep -rn '首步窗口' scripts/team/` 零命中（无实现可反推定义）。
- **复现路径**：`grep -n '首个分析单元' docs/领班制-面墙API设计稿-v3.md docs/wall-v3/acceptance-line-map.md docs/wall-v3/seat-gates.md`；`grep -rn '首步窗口' scripts/team/`。
- **自评级**：非阻断——SL-8a 机器骨架在全程窗口内可判可证伪；但「首步落盘纪律」是核心子断言，不量化则判红窗口漂移——施工前需把窗口定义为机器值（如「首个 tool_call 后 N 秒」）。

#### DS4-04

- **编号**：DS4-04
- **描述**：SL-13a 变体③（`entry` 键空数组→拒启）的拒启判据未具体化——变体①（删段）②（budgets 键缺失）对应 fail-loud 校验有明确键级判据，变体③「空数组」与「键缺失」是两种输入形态，判据文本未覆盖空值形态。
- **证据**：`docs/wall-v3/acceptance-line-map.md:314`（注入「③`entry` 键空数组」）与 :315（执法体「键缺失即拒启——exit 2」）。
- **复现路径**：`sed -n '313,317p' docs/wall-v3/acceptance-line-map.md`。
- **自评级**：建议——样本构造不受影响（桩可同时构造两种形态），仅判据文本需补一句「entry 空数组视同键缺失」级口径。

#### DS4-05

- **编号**：DS4-05
- **描述**：主稿 §4 宣称的体外执法形态（包装器＋监督者双进程、哨兵先行、进程组信号）与现状包装器实态（GNU timeout 同体执法，无哨兵无组信号）之间存在形态跨越，但施工落位未点名「改 run_droid_session.py 本体」——防施工者把「现状已包装」误读为「现状已体外执法」而漏改 wrapper 本体。
- **证据**：目标态宣称主稿 §4；现状实态 `scripts/team/run_droid_session.py:165-:190`（`build_droid_timeout_cmd` 生成 `timeout --signal=TERM --kill-after=30s <wall>s`）——全文件 grep「哨兵/监督者/killpg/setsid」零命中；契约侧措辞 `docs/wall-v3/seat-gates.md:286-:289`。
- **复现路径**：`grep -n '哨兵' scripts/team/run_droid_session.py`（零命中）；`sed -n '165,190p' scripts/team/run_droid_session.py`。
- **自评级**：建议——设计稿 §0 已声明「零施工、目标态」性质，可实现性不受影响（组B结论为可实现）。

### 1.D 三席自评总账

| 席位 | 新发现 | 复核维持（非新发现） | 自评分级 |
|---|---|---|---|
| 席位一 | 5（GLM53-03～07）＋复核维持登记 2（GLM53-01/02） | NB-1/NB-2/NB-4/NB-R3-1..5/round-1/2 留档项 | 阻断 0／非阻断 2＋2／建议 3 |
| 席位二 | 3（SONNET-1/2/3） | NB-1/NB-2/NB-3/NB-4（部分子项标「未复核」） | 非阻断 2／建议 1 |
| 席位三 | 5（DS4-01～05） | NB-1/NB-2/NB-4 | 非阻断 2／建议 3 |

三席对机械层与事实面的共同底账：席位二全量机械层解析 1606 个锚 token（1557 在界、49 伪报全部裁决为扫描器挂靠伪影、真越界 0）＋语义对质约 288 处（吻合约 278）；席位三预算四组真源逐组对照（10 组中 9 组吻合）＋SL 桩 13 族可证伪性全过（2 处局部存疑即 DS4-03/04）；席位一八章逐章论证链零实质断链、三件套三方一致性与十条硬规则落位核查闭合（唯一瑕疵即 GLM53-04 对平口径漂移）。三席均未发现对上使命已闭合结论（RC-10/RC-11、BLK-2 修复、21/21 断言面）的反证。

---

## 2. 终审裁决（逐项裁决与核验证据）

**终审席位**：glm54-auditor（GLM-5.4），与三席载体不同源。**裁决方法**：对 15 项编号发现逐项执行「席位指控 → 回读原物 → 比对 → 裁决」，裁决三分：成立（原物证实指控）／不成立（原物证明指控失真或证据不可复现）／降级（指控实质成立但锚位、定性或级档需调整）。15 项核心锚全部原物回读（15/15，实读行内容非行号存在）；凡席位给出的行号与实读不符，裁决条内写明「席位引什么、实是什么」。

### 2.A 席位一裁决（7 项）

| 编号 | 裁决 | 核验证据（终审独立回读） |
|---|---|---|
| GLM53-01 | **成立**（复核维持确认） | as-is :91/:118 实读在场；`worker_salvage.py` 实读——条件 1 在 :14、条件 2 在 :15、条件 3 跨 :16-:23、条件 4 跨 :24-:30，docstring 收尾在 :64。`:14-15` 只覆盖前两条，`:1-45` 落在 Products 段中间。级档非阻断（沿用上使命登记档级） |
| GLM53-02 | **成立**（复核维持确认） | `env-check.yml:194` 实读为条件行、:195 为 `PROJECT_TOKEN="$S_PROJECTS_STATE_PAT"`；out-of-graph :278 写 :195 与 :452 写 :194 两种行级口径并存确认。主稿 §3.3（:243）`:194-200` 区段口径可容纳两种行号。级档非阻断 |
| GLM53-03 | **降级**（实质不成立，入建议档） | 席位引 :23，实读该行为「升级闸判词 `mixed-registry-change` 必须接 foreman-wall-ci 恒跑」——**不含「全生产 workflow 树」字样也无扫描口径**；全文 grep「全生产 workflow 树」命中 :223/:229/:250 三处，**三处均带计数**（12 文件/6 名/82 行）。席位所称「无计数版」在原物中不存在，指控不可复现。级档由非阻断降为建议（措辞统一类顺带项，不单列处置） |
| GLM53-04 | **成立**（与 DS4-01 同源，合并裁定见 DS4-01 条） | 契约侧主稿 :148、seat-gates :280-:282/:606 实读在场；单源侧 `foreman_run_lib.py:42-46` 实读 validator 块 `job_wall_min=12`；仲裁 `budget_resolve.py:57-59` 实读「do not conflate」。**终审补强**（两席未点出）：seat-gates :289-:291 注释自己引用了「两个口径不得互相冒充」的纪律，而紧邻键值 `job_wall_min = 15` 恰把 envelope 冒充为会话切片——注释引用的纪律否定键值本身，比单纯数值漂移更重。级档非阻断 |
| GLM53-05 | **不成立**（按席位所述形态）；残余入建议 | grep「见本节表③行」唯一命中 **:235**，实读为 §3.2 六件表**之后**的散文段（非表格单元格），指向同节带 ①-⑥ 序号列的表，序号列在场可解析；席位所引 :232 实读为件⑤行且无该指针；grep「见主设计稿 §图外件」**零命中**。席位的行号、位置定性、引文三项均与原物不符。残余：:229「③补」与 :230「③」同用序号 ③，「见本节表③行」严格说可指两行，轻微歧义归建议档顺带项 |
| GLM53-06 | **不成立** | (a) 读法限定已在位——主稿 :5/:6/:19 三处声明引擎锚按钉树 460922c 读＋契约测试引擎锚解析器按 `git show 460922c:<path>` 读，:60-:62 表头与表首行锚即钉树行号；(b) 席位核心实证不可复现——终审按钉树读 `exception-point-inventory.md` :30-:31，#3 行在钉树与引擎工作副本**完全一致**（同在 :31），「一行之差」实测不存在于该文件。引擎 main 漂移本身是真实披露面，但已由主稿 :6「施工前逐文件 diff 披露」条款覆盖，且不在本项例证文件上 |
| GLM53-07 | **成立** | 主稿 :56 与 §6.1 四条（:315-:318）实读在场——四条被测对象都是违约会话/缺席注入，无一条以「监督者自身崩溃、哨兵写失败」为注入面。**终审修正席位原建议**：「执法体自身死亡面由 SL-1/SL-3 的哨兵在案＋不采信断言承载」不成立（那两条的哨兵是在位的）；真正闭合需施工时新增「监督者被杀/哨兵写失败后会话产物仍不被采认」的必死样本。级档建议 |

### 2.B 席位二裁决（3 项）

| 编号 | 裁决 | 核验证据（终审独立回读） |
|---|---|---|
| SONNET-1 | **成立** | `salvage_verdict.py:96-102` 实读——:97/:98/:100 均为 `salvage_verdict(...)` 调用关键字实参；`validator_prompt_template.py` :97/:98/:100 实读语义逐一吻合（HARD RULE／conflicts 必录／Authoritative counts）；席位附论「红章的代码执法面在 adopt_verdict.py」经 grep 核实（:85 注释、:98 `_gate_red_reason`、:138 `machine_gate_reds`）。**连带定性**：该句自称「现状执法面」，三条中两条只有 prompt 文字纪律、无代码执法体，措辞与 as-is :61 口径不一致，属同一行连带措辞问题合并处置。级档非阻断 |
| SONNET-2 | **成立** | `write_worker_delta.py` 实读——:42 `SELF_EXIT_CODES`、:72 调用点、:78 `def _is_interrupt_event`、:86 `try:`（在 `_is_interrupt_event` 体内）、:98 `def _stream_has_completion_event`。锚应改指 :98（定义）或 :72（调用点）。级档建议 |
| SONNET-3 | **成立**（席位证据行号归属需修正） | 全树 grep 实测 8 行展开（env-check :86/:240；I8 编排器 :102/:184/:258/:310/:347；team.yml :4431）。席位所引「本件 :181/:186」实为**姊妹件 out-of-graph-artifacts.md** 的行号（as-is 不足 190 行）；矛盾实质不变——as-is 自身矛盾位是 **:133**（五 secrets 注入行含 S_PROJECTS_STATE_PAT），:143 的「两处」在其声明范围内已错（漏 env-check :240），全树口径下漏 6 处。级档非阻断 |

### 2.C 席位三裁决（5 项）

| 编号 | 裁决 | 核验证据（终审独立回读） |
|---|---|---|
| DS4-01 | **成立**（与 GLM53-04 同源合并，主编号 DS4-01） | 单源侧 `foreman_run_lib.py:45`、执法侧 `lint_workflow_budgets.py:95-104`（**同时锁两个数**：会话切片必须 12、平台 envelope 必须 15，报错文案写明「is separate」）、契约侧三处失真实读在场。**终审独立补强危害边界**（修正两席风险描述）：`job_wall_min` 在全树无任何运行时消费点（grep 全部命中为取值函数/注释/定义/lint 锁/历史 fixture；team.yml 四处预算消费点只读 `validator_session_budget()` 返回值）——现状下 12/15 分裂零运行时后果；目标态把该键升格为软超时公式基座后**第一次获得执法语义**：按单源 12 施工则哨兵在 droid 墙 480s 到期前 160s 杀会话（320 < 480），按契约 15 施工则 lint「must stay 12」立即红——**两条施工路径都错，必须先裁口径**。终审裁定正确口径：该键作软超时基座时语义只能是 job timeout（平台 envelope，validator=15），因公式减项必须是 GitHub 真实硬杀墙（引擎 `droid-review-lead.yml:35-37` margin 400s 纪律实读在场）；错的是键名与单源「契约切片 12」同名异义、样例自我背书、公式未声明序约束（validator 现状 500 < 480＋120，本身需核）。级档**非阻断首位**（施工前置必要性高于普通非阻断项；未升阻断因设计稿零施工，缺陷在施工第一步即暴露，不会产出假绿墙） |
| DS4-02 | **成立**（终审补强：漏登面大于席位所指） | seat-gates :232-234 仅三键、team.yml:10 注记实读在场；树内 prep 区间 timeout 字面量实测 :1004-:1006（PIP 300/PYTEST 600/CHECK 300）、:1106/:1114（`timeout=60`，prep2 镜像同形）。**补强**：席位只点注记的 120s 层；树内实际未登记层是 pip install 300s 与两处 `timeout=60`，注记所写「other calls 120s」在 prep 区间未找到对应字面量（注记本身也滞后）。按 default-deny「登记即全集」，prep 席步级超时实际至少五层（600/300/300/60/60），契约登记两层。级档建议 |
| DS4-03 | **成立** | 三处同文均无量化实读在场（seat-gates :426／acceptance-line-map :378／failure-specs :132）；`grep -rn '首步窗口\|analysis_unit\|first_step' scripts/team/` 零命中；主稿 :303 INV-1 同样未量化。级档非阻断（与 GLM53-07 同属验收判据可判定性缺口，但本项有全程窗口兜底、影响面限于一个子断言） |
| DS4-04 | **降级为建议**（成立但影响极轻；定性收窄） | 实读 `acceptance-line-map.md:314-:316`——:316 断言行**已把变体③纳入「三变体全部拒启」**，期望结果明确（拒启、exit 2）；未具体化的只是 :315 执法体校验语义描述（「键缺失」是否涵盖「键在值为空」）。这不是判据缺失，是校验器规格措辞完备性——断言面已闭合，样本可构造性与红绿可判性不受影响。级档建议（维持档位，定性由「判据未具体化」收窄为「执法体描述未覆盖空值形态，断言面已覆盖」） |
| DS4-05 | **不成立**（指控的失真点在原物中不存在），不入呈裁清单 | (a) 现状实态与席位描述一致（run_droid_session.py 全文件 grep 哨兵/监督者/killpg/setsid 零命中，:165-:190 为 GNU timeout 同体执法）；(b) 但「施工落位未点名」与原物不符——主稿 :273 实读在同句内并置「lead/validator/replan **现状已包装**」与「**包装器＋监督者双进程**（目标态）」，改造关系被明示；:200 把「体外执法启动（§4 终止序列）」列为包装器目标态步骤；seat-gates :87 总注明示整段 TOML 为「**目标态样例（设计稿底稿，非施工）**」。施工者读 :273 不会误读。席位自评亦为建议且自述「可实现性不受影响」，但指控文本失真点未被原物支持 |

### 2.D 裁决计数

**成立 10**（GLM53-01、GLM53-02、GLM53-04、GLM53-07、SONNET-1、SONNET-2、SONNET-3、DS4-01、DS4-02、DS4-03；其中 DS4-02 成立且补强，GLM53-04 与 DS4-01 同源合并）；**降级 2**（GLM53-03 非阻断→建议；DS4-04 定性收窄）；**不成立 3**（GLM53-05、GLM53-06、DS4-05）。10＋2＋3＝15，无未裁决项。

**与上使命 21/21 验证结论的冲突核对**：21/21 全过为真、无翻案；本轮 15 项中有 5 项（DS4-01/GLM53-04、SONNET-1、SONNET-3、DS4-03、GLM53-07）落在 21 条断言**射程之外**的面——键值对质、裸锚文件归属、全称量词事实性、验收子断言可判定性、硬规则失败分支覆盖。这五个面是上使命验证提问框架的系统性盲区（「锚可解析≠话为真」「键集完整≠键值正确」「链路存在≠末端可判」），性质是「断言未覆盖该面」，不是「某条已过断言实为不过」。三席发现与 NB-1..4 登记全部相容（NB-3/NB-4 子项以复核维持编号进入本轮清单，非新发现）。

---

## 3. 呈裁清单（三档，呈大哥裁）

> 与终审裁决（mission 工件 adjudication.md）一致：阻断 0／非阻断 6 项（对应编号 7 个）／建议 6 项（对应编号 6 个）；不入清单 2 项（GLM53-06、DS4-05，不成立）。

### 3.1 阻断档

**本档无。**

15 项发现经逐项原物核验，无一满足阻断条件（「照稿施工会产生错误墙/假绿/执法缺位或契约矛盾」且无更早暴露点）。最接近阻断线的 DS4-01＋GLM53-04 在施工第一步（caps 文件落树＋budgets lint 接线）即必然暴露（lint :95-97 硬锁 12 与契约侧 15 直接冲突，CI 首跑红），不会静默产出错误墙。设计稿性质为零施工目标态（主稿 :4 自述），不存在「照稿施工即错墙」的当量。

### 3.2 非阻断档（6 项，施工前清理）

| # | 发现编号 | 席位来源 | 终审裁决 | 证据指针 | 处置建议（批后施工 mission） |
|---|---|---|---|---|---|
| 1 | **DS4-01 ＋ GLM53-04**（同源合并，对应编号 2 个） | 席位三＋席位一 | 成立；合并为一条 | 主稿 :148；seat-gates.md:280-:291/:606；`foreman_run_lib.py:45`；`lint_workflow_budgets.py:95-:104`；`budget_resolve.py:57-:60`；`team.yml:1387` | **施工前（必须，前置清理项首位）**：先裁「`job_wall_min` 作软超时基座时的语义」——终审建议口径＝平台 job envelope（15，公式减项必须是 GitHub 真实硬杀墙）。据此：① seat-gates :280-:291 与主稿 :148 显式声明「本键＝平台 envelope（15），与单源契约切片 `job_wall_min=12` 同名异义」，或为基座另立键名（如 `job_timeout_min`）消除同名；② 删除/改写 :289-:291 的自我背书注释；③ 补序约束：soft_timeout_sec 必须 ≥ droid_wall_sec＋adopt_reserve_sec（validator 现状 500 < 480＋120，施工前核清 adopt 储备是否在哨兵线之后）。**施工中**：caps 落树时 `default_budgets()` 与 lint :95-:97 的两口径迁移必须同一变更集完成（否则 lint 首跑必红），并新增契约测试断言「契约侧 job 墙键值 ↔ lint 锁值 ↔ team.yml timeout-minutes 三者一致」 |
| 2 | **SONNET-3** | 席位二 | 成立（席位证据行号归属修正：矛盾位为本件 :133 与姊妹件 out-of-graph :181/:186） | as-is:143（失实句）、:133；env-check.yml:86/:240；i8-zero-escape-live-orchestrator.yml:102/:184/:258/:310/:347；team.yml:4431；out-of-graph:332（已正确登记全树 8 行） | **施工前**——as-is :143 改为「PAT 展开位点全树 8 处」并回指主稿 §3.4 台账⑤（as-is 自述现状唯一真源，此句若被当「PAT 消费点全集」做收口会漏 env-check :240 与编排器 5 处）。**施工中**——件⑤收口（wall 步归零）落地时同步复核 |
| 3 | **SONNET-1** | 席位二 | 成立 | handoff-schemas.md:197；误指对象 `salvage_verdict.py:97/:98/:100`（函数实参）；本意对象 `validator_prompt_template.py:97/:98/:100`；代码执法面 `adopt_verdict.py:98/:138` | **施工前**——:197 三裸锚补全路径；同句「现状执法面」措辞按实情改写（红章有代码执法面，冲突升级与计数单源两条仅为 prompt 文字纪律，与 as-is :61 口径对齐）。避免施工期锚检查在该行误红 |
| 4 | **DS4-03** | 席位三 | 成立 | seat-gates.md:426；acceptance-line-map.md:378；failure-specs.md:132；主稿 :303；`scripts/team/` 全目录 grep 零命中 | **施工前**——把「首个分析单元」定义为机器值并三处同改（可选口径：「会话开始后 N 秒」或「首个 tool_call 事件后 N 秒」，N 入 budgets 键如 `first_persist_sec`）。**施工中**——SL-8a 按量化窗口构造首步子断言；量化落地前 SL-8a 只按全程窗口单判，首步子断言显式标「待量化」而非默许通过 |
| 5 | **GLM53-01**（上使命 NB-3 维持） | 席位一 | 成立（复核确认） | as-is:91（`:14-15 区间`）、:118（`:1-45`）；`worker_salvage.py:13-:30`（四条件实际区间）、`:64`（docstring 收尾） | 并入施工前清理清单——:91 改 `:14-:30`，:118 改 `:1-:64` |
| 6 | **GLM53-02**（上使命 NB-4 子项维持） | 席位一 | 成立（复核确认） | out-of-graph:452（附A 写 :194）对 :278（样例写 :195）；`env-check.yml:194`（条件行）、`:195`（展开消费） | 并入施工前清理清单——附A :452 统一为 :195（与 :278、主稿 §3.4 台账⑤、out-of-graph:332 对齐） |

### 3.3 建议档（6 项，顺带处理）

| # | 发现编号 | 席位来源 | 终审裁决 | 证据指针 | 处置建议 |
|---|---|---|---|---|---|
| 1 | **GLM53-07** | 席位一 | 成立（处置建议按终审修正） | 主稿 :56（推论 3）、:315-:318（§6.1 四条）、:85/:328（SL-1/SL-3，哨兵在位） | **施工前**——:56 支撑指针补「执法体自身失效面由 SL-1 变体『监督者先死/哨兵写失败』承载」。**施工中**——SL 族新增必死样本：注入监督者崩溃或哨兵文件不可写，断言会话产物仍不被采认、无回退路径。席位原建议「由 SL-1/SL-3 哨兵在案断言承载」不成立，不能照抄 |
| 2 | **SONNET-2** | 席位二 | 成立 | handoff-schemas.md:84；`write_worker_delta.py:86`（`try:`，中断函数体内）、`:98`（completion 函数定义）、`:72`（调用点） | 施工前清理清单顺带项——:84 的「:86 区段」改「:98」或「:72」 |
| 3 | **DS4-02** | 席位三 | 成立（补强：漏登面为 pip 300s 与两处 60s，非仅注记的 120s） | seat-gates.md:231-:234；主稿 :146；`team.yml:1004-:1006`、`:1106`、`:1114`、`:10` | 施工前清理清单顺带项——prep budgets 段按树内实况补全（pip 300s 入键；git 探测 60s 是否入键由施工者定；注记「other calls 120s」一并校正为实况） |
| 4 | **DS4-04** | 席位三 | 降级为建议（断言面 :316 已覆盖三变体全拒） | acceptance-line-map.md:314/:315/:316 | 施工前清理清单顺带项——:315 补一句「键存在但值为空（空数组/空串）视同键缺失」 |
| 5 | **GLM53-03**（降级入建议） | 席位一 | 降级（实质不成立：带「全生产 workflow 树」措辞的三处 :223/:229/:250 均带计数；:23 无该措辞） | 主稿 :23、:223、:229、:250 | 无需专项处置；若施工前顺带统一措辞，§0b 表 NEW-1 行可补「（全树口径 12 文件/82 行，§3.4）」回指。优先级最低 |
| 6 | **GLM53-05 残余**（不成立项的残余） | 席位一 | 不成立（残余入建议） | 主稿 :235（指针所在，表外散文可解析）、:229（「③补」行）、:230（「③」行） | 可选——:229 行标签「③补」改用独立序号（如「③′」），或 :235 指针改「见本节表件③主行」。优先级最低 |

**不入清单（不成立，不必处置）**：GLM53-06（读法限定已在位三次；「一行之差」实测不存在）、DS4-05（主稿 :273 明文并置现状/目标态，seat-gates :87 总注覆盖目标态样例）。

---

## 4. 结论与下一步

### 4.1 总判

**三席对抗审完成，无阻断发现。** 15 项编号发现：成立 10／降级 2／不成立 3；呈裁清单三档＝阻断 0／非阻断 6／建议 6。上使命 21/21 验证结论无翻案；5 项覆盖缺口（键值对质、裸锚文件归属、全称量词事实性、验收子断言可判定性、硬规则失败分支覆盖）显式登记为上使命验证框架的系统性盲区。基线恒绿保持：本报告零代码改动，全量 pytest（997 passed, 2 skipped）＋五 lint 全绿。

### 4.2 呈大哥裁要点

1. **先裁 DS4-01 口径再开工**（非阻断首位，施工前唯一必裁项）：validator `job_wall_min` 作软超时基座应取 job envelope（15）还是契约切片（12）。终审建议取 15 并消除与 `default_budgets()` 的同名异义；同时核清 soft（500）< droid（480）＋adopt（120）的序关系。两条施工路径现状下都会错：按 12 施工则哨兵先于会话墙 160s 杀会话，按 15 施工则 lint 首跑红。
2. **非阻断 6 项并入施工前清理清单**（同批处理 NB-1/NB-2 两个已登记残留）：as-is :143 PAT 全集句、handoff-schemas :197 裸锚与「执法面」措辞、首步窗口量化、as-is :91/:118 区间、附A :195 统一。
3. **建议 6 项顺带**：GLM53-07 需施工时新增「监督者先死」必死样本（席位原建议的承载方案不成立，不能照抄）；DS4-02 漏登面比席位所报更大（pip 300s 与两处 60s；注记的 120s 在树内已无对应字面量）。
4. **三项不成立不必处置**：GLM53-05、GLM53-06、DS4-05 的指控文本失真点经原物回读不存在；GLM53-05 的「③补」序号歧义可顺带处理。
5. **验证框架补强**（供批后施工 mission 契约测试设计参考）：本轮覆盖缺口的共同形态是上使命断言只验「形」不验「值」；施工 mission 的契约测试建议补三类断言——TOML 栅栏 budgets 键值对单源、裸锚显式文件归属、全称量词句（「只在」「唯一」「全部」）逐句对树。

### 4.3 下一步

本报告呈大哥裁。**批准后另立施工 mission** 承接：呈裁清单处置（含施工前清理清单与 DS4-01 口径裁决落地）＋验证框架三类补强断言。本 mission 零施工、零设计稿修改，到此收口。

---

*审查对象版本 main@4f4c53a；引擎锚基准 460922c；三席 glm53-worker/sonnet-auditor/ds4-auditor（席位三 glm53-worker 兼任）＋终审 glm54-auditor；裁决日期 2026-11-29。本报告零密钥值（secret 只记名），唯一 repo 改动＝本文档＋README 对抗审交付段。*
