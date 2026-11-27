# 图外件清零清单＋钥匙总管理台账设计（out-of-graph 底稿）

> 底稿（mission F3/out-of-graph 产出；主设计稿 §图外件清零清单 与 §钥匙总管理 两章的素材源）。本件逐件列明领班制流水线的图外自动化、图外会话与散落凭证，每件四要素（现位置 file:line 锚／图外性判定／收编或禁绝方式／责任席位），并给出钥匙总管理台账设计（照引擎 M2 口径：零值登记、use/cap_change 定性、消费锚、对账判据）。
>
> **真源声明**：引擎形制以 `docs/wall-v3/form-basis.md`（锚件 1）为准（钥匙台账铁律＝其要点 9）；测试仓现状行号以 `docs/wall-v3/as-is-capability-inventory.md`（锚件 2）为准——本件引用 team.yml 现状一律转引锚件 2，新增锚点（锚件 2 未覆盖者）全部实读核实后登记于本件附A。席位门清单授权面以 `docs/wall-v3/seat-gates.md`（F2 底稿）为准——本件清零后的每件归宿都落在对应席位门清单内（VAL-CROSS-002 一致性）。
>
> **零施工声明**：本稿只设计，不动现状。清零动作分两类归属：**施工 mission**（workflow 文本、scripts、schema、契约测试改动）与**大哥人工操作**（板侧内建规则、凭证裁定、工作区清理）。本稿不写「待定」——每件给可施工步序；裁定权项显式标注「呈大哥裁」，裁项内容本身已成文。
>
> **零密钥值铁律**：本件只记 secret 名与元数据。唯一涉及值位形态的是 I8-B 夹具假 PAT（前缀族 `ghp_` 的哑值，非真凭证），本稿记名与位点不转录值本体。
>
> **禁抄项**（form-basis §11）：引擎墙未闭合缺口中**仍在册的缺口态**（`--changes` 判词不接 CI 的登记时点态已于 main@460922c 上游闭合，引用引擎接线口径一律按闭合后形态；NEW-1 governance 门现状＝enabled 在役执法——见本件 §3.7 与 form-basis §11.1 更新口径）不抄入本件——本件所有守卫与对账都是**须执法的门**（接 CI 恒跑，见 §3.7）。引用引擎放行门口径一律按 R-29 已裁**两门**（quality-gate / substrate-gate-suite）。
>
> **版本口径**：本件属设计稿 v3.0 体系，作废 v2.7~v2.10 账面墙口径；现状 team.yml:7 标 v2.7.0、README 交付段另标 v2.9/v2.10 的漂移（锚件 2 §0）由 v3.0 统一收口。
>
> 全部 file:line 锚经实读核实（2026-11-27 快照，测试仓 R58-D 收尾态基线 564ce30；引擎仓 main 当前树）。

---

## §0 图外判定口径（什么样的东西算「图外」）

**图内**（in-graph）＝某席位的门清单登记面覆盖的东西：入口在 `entry`、行为在 `api`/`local_uses`、产出在 `artifacts`/`events_produced`、令牌在 `authorization.token_scope`、验证在 `verification`。**门清单之外不存在**（default-deny）。

**图外**（out-of-graph）＝不属于任何席位门清单登记面的自动化、会话或凭证面。按三型归口：

| 型 | 定义 | 本件对象 |
|---|---|---|
| 图外自动化 | 触发面或执行体在流水线编排之外，且其写目标落在链上权威面（板面/issue/凭证） | 图外件①板面 Item closed 自动化 |
| 图外载荷 | 活验/探针载荷内嵌生产文本，生产消费面为零，或值本体违反零值登记 | 图外件②I8-B 标题键控假 PAT 夹具 |
| 图外凭证面 | 凭证展开位点、消费关系、暴露面未登记未对账，或多席位重复展开无 scope 差异 | 图外件③BYOM 全树位点展开（声明体 11 位点＋内联变体面，全树口径 12 文件/6 secret 名/82 展开行实测）、图外件⑤env-check 五 secrets 全量入环境、第 6 secret I8_TEAM_TRIGGER_PAT（I8 编排器 5 行展开） |
| 图外产物 | 链上语义命名（verdict 系）出现在链外位置，生成演员未登记 | 图外件④verdict.json/md 顶层孤儿件 |
| 图外会话面 | 运行态会话记录/记忆面在墙外运行、不进墙、不承载判定却可能被误用为证据源 | 图外件⑥memory/ 运行态会话面 |

**清零两词**（每件四要素之「收编或禁绝」只能取其一或组合，禁止空置）：

- **禁绝**（eliminate）：图外件被关死或移出，不留功能等价旁路（如板侧 Disable、夹具拆除＋探针改道）。
- **收编**（incorporate）：图外件的功能获得图内归宿——收进某席位门清单登记面、某声明体单点、或台账登记面，进入对账。

**判据承载分工**：本件给每件的**清零判据**（§4 汇总）与负例载体指针；必死样本的桩设计与执法延迟口径归 F4（`docs/wall-v3/failure-specs.md`＋主设计稿验收线章），本件不重复定义桩形态。

---

## §1 图外件总览（六件一张表）

| # | 图外件 | 型 | 现位置锚 | 收编/禁绝 | 责任席位 | 判据节 |
|---|---|---|---|---|---|---|
| ① | 板面 Item closed 自动化（关单翻板） | 图外自动化 | 板侧 Projects #33 内建工作流；证据 `docs/板面关单翻板-最小操作指引.md:12-14` | 禁绝（板侧 Disable/终态选项改造）＋收编（图内漂移对账与再同步） | 大哥（板侧）＋装配席（再同步）＋env-check（探测项） | §2.1/§4 |
| ② | I8-B 标题键控假 PAT 夹具 | 图外载荷 | `team.yml:419`、`:412-432` 区段（命中分支 `:429-432`） | 禁绝（夹具仓化＋生产文本净化＋探针改道） | lead 席默认删行＋大哥退役批（workflow 文本编辑权属施工批，见 §2.2 责任席位行）＋验收席面（活验编排改道） | §2.2/§4 |
| ③ | BYOM 三件＋FACTORY_API_KEY 全树位点重复展开 | 声明体位点 11 个，跨 4 个 workflow 文件：team.yml 8 个 Write BYOM settings 步（`team.yml:117/:529/:1460/:1880/:2176/:2723/:3702/:4113`，名称行）＋`droid.yml:25`（replica pattern）＋`droid-probe.yml:13`＋`probe6.yml:10`；内联变体面 `droid-probe2.yml`（`:15-17` env 注入＋`:37` 内联 settings.json 写位）＋`probe3.yml`（`:15`＋`:38-40` env 注入＋`:51/:60` 内联写位）；其余探针面 probe/probe4/probe5 与 I8 编排器＋c-fixture 注入面同树入账。**全树口径（对账判据 1 与守卫面 §3.6 与位点集三者同边界）**：`grep -n 'secrets\.' .github/workflows/*.yml` 实测＝12 个 workflow 文件、6 个 secret 名、82 条展开行 | 收编（单点声明体＋全树消费锚＋按席差异化 scope 矩阵呈裁＋台账 1 登记多锚；probe/I8/内联变体族纳入裁定面与对账锚集） | 写板席（声明体）＋大哥（scope 裁定）＋caps-gate（对账） | §2.3/§3.4/§4 |
| ④ | verdict.json/md 顶层孤儿件 | 图外产物 | mission 工作区顶层两件（2026-11-27T08:07 生成，非 repo 树、非 git tracked） | 禁绝（清理）＋收编（命名空间合法落点＋防复活负例） | 写板席（命名空间）＋大哥/人工（清理） | §2.4/§4 |
| ⑤ | env-check 五 secrets 全量入环境 | 图外凭证面 | `env-check.yml:82-86`（gate 步 5 件）、`:238-240`（wall 步 3 件重复） | 收编（按消费分离注入：wall 步归零＋台账登记暴露面） | env-check 零号门＋写板席（施工）＋caps-gate（对账） | §2.5/§3.5/§4 |
| ⑥ | memory/ 运行态图外会话面 | 图外会话面 | `memory/log/2026-11-27-sessions.md`（会话记录面）；untracked 运行态树 | 收编（接口收口：证据入库单点＋门清单禁写＋台账登记） | 改计划席（输入面）＋写板席（入库规范）＋领班席（编排声明） | §2.6/§4 |

六件覆盖任务书必含清单全部六项（板面 Item closed／I8-B 夹具／BYOM＋FACTORY_API_KEY 收口／verdict 孤儿件／env-check 五 secrets／memory 会话面）。

---

## §2 逐件四要素底稿

### 2.1 图外件①：板面 Item closed 自动化（关单翻板）

**四要素速览**

| 要素 | 内容 |
|---|---|
| 现位置 | 板侧 Projects #33 → Workflows → Built-in「Item closed」（板面设置，非 repo 树）；现象证据 `docs/板面关单翻板-最小操作指引.md:12-14`（三单实测行）、机制结论 `:22`；仓内唯一板面写点对照 `team.yml:4431`（PAT 注入）/`:4441`（project_state_write 调用） |
| 图外性判定 | 触发面图外（工单关闭事件无 workflow 触发器可挂）＋执行体图外（`github-project-automation` 平台系统演员，全仓 grep 零命中，`:20`）＋写目标未授权（Status=施工中不是任何席位门清单的门，与装配席 projects-write 单点面冲突） |
| 收编/禁绝 | 板侧禁绝（大哥按 `:26-33` 指引二选一改造）＋图内收编（装配席漂移对账/再同步＋env-check 探测项＋墙记 board_drift） |
| 责任席位 | 板侧规则状态＝大哥（板面所有者，人工一次）；漂移检测与再同步＝装配席（写板单点）；探测项＝env-check 零号门 |

**现状与锚**：assemble 窗内 PAT 写板「已验收」（`team.yml:4431`/`:4441`，演员=PAT 持有人）→人工关单→1–2 秒内 Status 被翻回「施工中」，演员 `github-project-automation`（#761/#763/#764 三单同构，时间线见 `docs/板面关单翻板-最小操作指引.md:12-14`）。专档结论原文：翻板不是流水线代码造成的，repo 内无可拦截、可修正的写入点（`:3` 状态行、`:18-22` 排查节）。该自动化的规则体住在 GitHub Projects 板面设置（Built-in workflow「当项目中的项被关闭时→Set Status=施工中」），repo 树内无其文本。

**图外性判定（三条成立）**：

1. **触发面图外**：工单关闭事件不在 team.yml 触发面内（team.yml 只触发 issue 评论/开启，锚件 2 §1）；流水线没有任何 job 能在该事件上被唤起。
2. **执行体图外**：`github-project-automation` 是平台内建自动化的系统演员（`:22`），不在任何席位门清单的 `api`/`local_uses` 登记面内。
3. **写目标未授权**：它写的是链上权威面（Projects #33 Status，板面权威口径，`team.yml:4599` 审计镜像声明行），但「关单时置施工中」不装配席、也不属任何其他席的门清单——这是把板面写面从 PAT 单点（seat-gates §2.6 `projects-write` 单点）扩成了「板侧规则也有写权」，直接违反写入口收口（硬规则⑤）与图外清零（硬规则⑩）。

**收编/禁绝方式（板侧禁绝＋图内再同步，两者缺一不可）**：

- **板侧禁绝（大哥人工，一次）**：按专档 `:26-33` 最小操作执行，本稿把三选项写成裁定项：**A**＝Disable 整条规则或删除 Set Status 步（关单不改 Status）；**B**＝Set Status 目标选项从「施工中」改为「已验收」（关单即终态）。A/B 都消除翻板；**「保留原样」不在可行集**——它与写板终态直接冲突（翻板实证）。施工验收判据照抄专档 `:37`：下一单关单后 1–2 分钟查 timeline，不再出现 `actor=github-project-automation` 的 `ProjectV2ItemStatusChangedEvent`、Status 保持 assemble 写入终态即闭环。
- **图内再同步（装配席，施工面）**：即便板侧 Disable，仍需图内发现能力防「板侧规则被重开」静默复发：
  1. **漂移对账步**（assemble 收口段新增，施工落 `scripts/team/board_state_check.py` 目标态）：以 PAT 单点读板，当「工单关闭且 Status≠assemble 写入终态」时记 `board_drift` 事件——墙 `closeout` 切片扩字段（schema 变更走同批改锁，`schemas/foreman-run.v1.schema.json:210-215` closeout_slice 面）＋重写板一次（PAT 单点，写终态）＋仍漂移则 `chain_facts.summary_code` 取板面漂移枚举值＋硬评论报警（`post_comment_hard --hard-required`）。
  2. **env-check 探测项**（零号门检查清单扩展，施工落 env-check.yml 检查 8）：板面内建规则状态列为新检查项；受平台 API 边界限制（内建工作流配置无公开读 API 的部分）以 WARN 人工巡检项登记，边界明示不入 PASS（照 env-check「边界声明非通过」既有口径）。
  3. **诚实边界**：关单发生在 run 结束之后时，图内侧只有「下一单 run 的 env-check/assemble 对账」能发现漂移——图内机制是**发现与纠正**，不是阻断；**板侧 Disable/终态改造是唯一完全解**。因此本件的禁绝主责在板侧，图内机制是防复发，不是兜底（无兜底铁律）。

**清零判据**（详见 §4 表）：①板侧规则不再产生翻板事件（timeline 判据）；②`board_drift` 对账与 env-check 探测项在树且接 CI/活验；③负例载体：F4 必死样本「板面翻板回归样本」（59 轮四问题③回归，桩＝模拟关单后 Status 漂移输入，断言对账步必红必再写）。

### 2.2 图外件②：I8-B 标题键控假 PAT 夹具

**四要素速览**

| 要素 | 内容 |
|---|---|
| 现位置 | `team.yml:419`（`I8_LIVE_B_INVALID_GH_TOKEN` 变量行，含 `ghp_` 前缀族哑值——值本体不转录）；命中分支内嵌于生产步「Post plan dispatch comment (B4/I4)」（`team.yml:412-432` 区段：`:418` 注释、`:429` 标题比较、`:430` export 换 token、`:431` echo 说明、`:432` 收尾 fi） |
| 图外性判定 | 执行条件图外（issue 标题字符串是活验编排面信号，非流水线门面输入）＋生产消费面为零（只有 I8-B 活验单命中）＋夹具值内嵌违反零值登记（PAT 前缀族值住生产 workflow 文本，污染钥匙审计 grep 面） |
| 收编/禁绝 | 禁绝（三步：夹具仓化→生产文本净化→活验断言改道探针）＋守卫负例常驻 |
| 责任席位 | 默认删行＝lead 席（门清单 §2.4 表 2 的多出的门默认删——workflow 文本编辑权不在任何会话席门清单内，default-deny 下由施工批按主设计稿 §2.4/§3.2 落地）＋大哥退役批（探针退役＋假 PAT 回读验证）；活验编排改道＝验收席面（validator 职能的 I8 编排，大哥批准另立施工单）；假 PAT 变量退役＝钥匙台账（zombie→revoked，§3.3 条目⑦）。**口径注**：recorder（写板席）门清单（seat-gates §2.7）不含 workflow 编辑权（artifacts 面仅 partial/status/补卷三路径），本件拆除不派写板席 |

**现状与锚**：lead 派单评论步（生产步，每单执行）内嵌一段标题键控分支：`ISSUE_TITLE == "[I8] API墙活验 B 评论硬失败"` 时把 `GH_TOKEN` 换成假 PAT 变量（`team.yml:429` 比较、`:430` export、`:431` echo、`:432` 收尾 fi），变量默认值是 `ghp_` 前缀族哑值（`:419`）。该夹具属 I8 四类活验的 B 型（评论硬失败传播）证据链。

**图外性判定（四条成立）**：

1. **执行条件图外**：命中键是 issue 标题字符串——活验编排面信号，不是任何门清单的 `entry`/`events_consumed` 登记；生产 run 的输入面里没有这个键。
2. **生产消费面为零**：非 I8-B 单从不进入该分支；生产文本为此常驻一段死载荷。
3. **值本体违规**：PAT 前缀族值（哑值）住生产 workflow 文本——钥匙总管理口径下应记名位（台账），不应有值位（key-registry 零值铁律，form-basis 要点 9）；且任何 `ghp_` 前缀 grep 审计都会命中生产文本（§3.6 对账判据 2 的值泄漏扫描被夹具值污染，需显式登记例外位，拆除批消除例外）。
4. **归属错位**：活验夹具是验收证据链的载荷，却住生产编排文本——证据载荷与生产面无隔离。

**禁绝方式（三步施工序＋守卫）**：

1. **夹具仓化**：新建 `.github/workflows/i8-zero-escape-live-b-fixture.yml`，形态对位既有 C 型夹具（`i8-zero-escape-live-c-fixture.yml` 在树——I8 家族中 C 型已是独立 workflow 文件，B 型对齐同构）：`workflow_dispatch` 触发（inputs: issue_number），夹具假 PAT 经 repo variables `I8_LIVE_B_INVALID_GH_TOKEN` 注入**夹具文件内**（不在 team.yml）。工作流文件清单（含全部探针/夹具族：`probe.yml`、`probe3-6.yml`、`droid-probe*.yml`、`i8-zero-escape-live-*.yml`）登记进台账 `[[external_face]]` 参考面（§3.3）。
2. **生产文本净化**：team.yml 删 `:418` 注释行、`:419` 变量行、`:429-432` 命中分支（`:429` 标题比较起、`:430` export、`:431` echo、`:432` 收尾 fi——fi 必须随分支整段删除，否则残留悬空 if 收尾使 workflow 语法失效）——「Post plan dispatch comment」步恢复为无条件 `GH_TOKEN: ${{ github.token }}`（`:415`）＋单一 `post_comment_hard` 调用；步内 `:414` env 块、`:425-428` foreman-run freshen 行不在删除集（均为生产步必需行）。
3. **活验断言改道**：I8-B 的断言语义（无效令牌→评论 401/403→`post_comment_hard --hard-required` 退出 1→墙 patch 记录硬失败）改由**探针单**承载：探针 workflow（家族形态在树）内以无效令牌对探针 issue 调用同一 `post_comment_hard` 共享件断言硬失败传播。成立性说明：`post_comment_hard.py` 是全链单源共享件（`scripts/team/`），硬失败语义单源——探针红即生产该路径红，I8-B 证据效力不变且生产文本零夹具。
4. **守卫负例（常驻）**：文本断言进 caps-gate 载体（`tests/test_foreman_caps_contract.py`，目标态新增）——生产 workflow 树（`.github/workflows/*.yml` 12 文件全树边界，对账判据 1 与位点集同一扫描面；件②判据行同此边界）正文出现 `I8_LIVE_B` 或 PAT 前缀族字面（`ghp_` 等）即红。此负例同时是 §3.6 对账判据 2（值泄漏扫描）的一个实例；扫描边界口径与件②判据的禁绝判据（生产 workflow 零 I8_LIVE_B＋零 PAT 前缀族）同面——「四文件集」旧表述自本批废止（实测：82 展开行中 37 行在四文件集之外，扫描面收窄会漏检）。

**清零判据**：生产 workflow 零夹具分支与零 PAT 前缀族命中；B 夹具文件在树且探针改道后 I8-B 活验单全链红照旧；守卫负例常驻 CI。假 PAT 变量（repo variables）随拆除转 `[[dangling_name]]`（zombie），探针退役批回读验证后转 revoked（§3.6 判据 4 牺牲品链）。

### 2.3 图外件③：BYOM 三件＋FACTORY_API_KEY 的全树位点重复展开（12 文件/6 名/82 行实测口径）

**四要素速览**

| 要素 | 内容 |
|---|---|
| 现位置 | **全树实测口径（对账判据 1 与守卫面同边界）**：`grep -n 'secrets\.' .github/workflows/*.yml` ＝ 12 个 workflow 文件、6 个 secret 名、82 条展开行。其中「Write BYOM settings」声明体位点 11 个，跨 4 个 workflow 文件：team.yml 8 个会话步（`:117/:529/:1460/:1880/:2176/:2723/:3702/:4113`，名称行）＋`droid.yml:25`（replica pattern，caller-side gateway auth）＋`droid-probe.yml:13`（same as droid.yml v5）＋`probe6.yml:10`（replica pattern）；每步 env 注入两到三件＋写文件 heredoc（如 team.yml lead `:131-149` 区段：headers 键位 `:133-135`、`x-opencode-session` 头 `:134`、apiKey 位 `:141`；droid.yml 同构块 `:25-60` 区段）；FACTORY_API_KEY 独立步注 team.yml 8 处（`:157/:568/:1501/:1916/:2209/:2757/:3738/:4147`）＋`droid.yml:62`＋`droid-probe.yml:46`＋`probe6.yml:44`。**内联变体面（同构写位、无命名步）**：`droid-probe2.yml`（`:15-17` env 三件注入＋`:37` 内联 settings.json 写位）与 `probe3.yml`（`:15` 单件注入＋`:38-40` 三件注入＋`:51/:60` 内联写位）。**同树其余凭证位点**：probe.yml `:16/:22`（WORKER_CI_KEY）、probe4.yml `:10-11`（WORKER_CI_KEY＋GO_GITHUB_RUN_TOKEN）、probe5.yml `:10-11`（WORKER_CI_KEY＋GW_TOKEN_KNOWN）、env-check.yml（`:82-86` gate 步五件＋`:238-240` wall 步三件——件⑤分账）、I8 编排器 `i8-zero-escape-live-orchestrator.yml` 五组三件注入（`:100-102`/`:182-184`/`:256-258`/`:308-310`/`:345-347`，含**第 6 secret `I8_TEAM_TRIGGER_PAT` 5 行**——全树唯一使用面）、c-fixture `:41-42`（两件探针面）。六名清单：FACTORY_API_KEY 16 行／WORKER_CI_KEY 21 行／GW_TOKEN_KNOWN 12 行／GO_GITHUB_RUN_TOKEN 20 行／PROJECTS_STATE_PAT 8 行／I8_TEAM_TRIGGER_PAT 5 行 |
| 图外性判定 | 重复展开≠登记（同一能力面多份平行配置、零登记零对账）＋无席位差异声明（四角色同拿三件＋同模型条目，多发票证=图外能力）＋写文件位图外（`~/.factory/settings.json` 是 runner 会话外配置面，生命周期无登记，session 结束即弃）＋**收口面完整性（round-2 全树口径）**：硬规则⑨「全部凭证」口径下，凭证收口不因 workflow 文件归属（非领班席生产/探针/I8 面）而遗漏——`droid.yml`（@droid 触发的生产 workflow）、probe 族（workflow_dispatch 探针）与 I8 编排器/c-fixture/内联变体面的凭证位点与领班席同树同构，不收编则位点对账判据（§3.6 判据 1）在全生产 workflow 树上必然失配 |
| 收编/禁绝 | 收编（单点声明体＋全树调用位变消费锚＋按席差异化 scope 矩阵呈裁＋台账 1 登记多锚；probe/I8/内联变体族纳入裁定面与对账锚集） |
| 责任席位 | 声明体与收口＝写板席；scope 裁定＝大哥（本稿给呈裁清单，probe 族一并呈裁）；对账执行＝caps-gate；台账登记＝钥匙面（§3.3 条目①-④） |

**现状与锚**：team.yml 8 个 droid 会话步（lead/worker/validate/revalidate/replan/worker2/validate2/revalidate2）各自把 `WORKER_CI_KEY`/`GO_GITHUB_RUN_TOKEN`/`GW_TOKEN_KNOWN` 写进 `~/.factory/settings.json` 的 BYOM 模型条目（headers 键位 `x-ci-key`/`x-opencode-session`/`cf-aig-authorization`＋`apiKey` 位），机制块逐位点重复（lead 形态 `team.yml:131-149` 区段）。会话头已按席位 pin：`SESSION_NAME`（`:123` lead=team-lead、`:534` worker=team-worker-<pid>、`:1466` validator=team-validator、`:1886` revalidate 同名、`:2181` replan=team-lead-replan、`:2728` worker2=…-r2）——**席位可区分性已存在，只是 scope 未差异化**。FACTORY_API_KEY 另在每席位独立 env 注入（team.yml 8 锚）。**非领班面同构 3 步**（锚经实读核实）：`droid.yml:25`（@droid 触发的生产 workflow，BYOM 条目 model=dynamic/droid-review、headers 三键位齐全，`:62` FACTORY_API_KEY 注入）、`droid-probe.yml:13`（workflow_dispatch 探针，`WORKER_CI_KEY`/`GO_GITHUB_RUN_TOKEN` 双件、`:46` FACTORY_API_KEY）、`probe6.yml:10`（workflow_dispatch 探针，三件齐全、`:44` FACTORY_API_KEY）——三步与 team.yml 机制块同构（同一 `~/.factory/settings.json` 写位、同一模型条目族）。**内联变体两件（round-2 全树口径入账）**：`droid-probe2.yml`（`:15-17` env 三件注入、`:37` 内联 `~/.factory/settings.json` 写位——BYOM 机制同构但无「Write BYOM settings」命名步）与 `probe3.yml`（`:15` 步 1 单件注入、`:38-40` 步 2 三件注入、`:51-60` 两处内联 settings.json 写位（:60 为 json.dump 写文件行））——**两件并入本件收口面**（不再只登记 `[[external_face]]` 参考面）：收口施工时与 11 声明体位点同批核对/改写，或显式禁改登记。**第 6 secret**：`I8_TEAM_TRIGGER_PAT` 仅在 I8 编排器展开（5 行：`:100/:182/:256/:308/:345`），生产 team.yml 零消费——按全树口径入台账（§3.3 条目⑧）。全树总账（实测）：12 个 workflow 文件、6 个 secret 名、82 条展开行；位点对账判据（§3.6 判据 1）、守卫负例扫描面（§2.3 收编方式 4）、本位点集三者边界一致＝全生产 workflow 树。

**图外性判定（三条成立）**：

1. **重复展开≠登记**：台账口径下应为「1 条登记＋N 条消费锚」；现状是多份平行声明体（跨 4 文件）＋内联变体面＋散点探针/I8 注入位、零登记、零对账——任何一件的用途/暴露面变化都无从发现。
2. **无席位差异声明**：lead/worker/validator/replan 四角色拿完全相同的三件＋同模型条目；probe/droid/I8 面（非领班席）同拿同构件无任何登记。各面三件是否都必要无声明无对账——席位用不到的钥匙=无授权能力（59 轮问题类的凭证面变体）。
3. **写文件位图外**：`~/.factory/settings.json` 不进墙、不进台账、不进 artifact；其内容由 heredoc 在各声明体位点与内联变体位各自生成，无单源。

**收编方式（单点声明＋按席差异化 scope）**：

1. **单点声明体**：BYOM 写入逻辑收敛为一个单源脚本 `scripts/team/write_byom_settings.py`（目标态新增；参数化 role/session_name），**11 个声明体位点全部改为单行调用**（team.yml 8 步＋droid.yml/probe6.yml 两步——两文件均在生产 workflow 树，收口后声明体对其同形可用；droid-probe.yml 双件形态以参数化子集承载），**内联变体面（droid-probe2.yml/probe3.yml 的 3 处内联写位）同批收口**为声明体调用或显式禁改登记——对位本仓脚本单源化先例（`write_worker_delta.py`／`validator_prompt_template.py` 单源，锚件 2 §2/§3）。声明体是**登记面**，调用行是**消费锚**（台账 consumes 字段，锚集边界=全生产 workflow 树）。
2. **按席差异化 scope 矩阵**（与 seat-gates §2 各席 `authorization.token_scope` 对齐，本件不重复定义席位面，只给凭证面的裁定程序）：
   - 判定程序：逐席列出三件各自的消费键位（`x-ci-key`/`cf-aig-authorization`/`apiKey`），从「该席会话是否产生需要该键位的请求」推导最小集；推导不出的保守登记现状全量。
   - **呈大哥裁两条建议**：①validator/revalidate 席（会话零 GitHub 写权已成立）的 BYOM 三件最小集裁定——尤其 `cf-aig-authorization` 头位与 `apiKey` 位对该席会话的必要性；②`FACTORY_API_KEY` 与 BYOM `apiKey` 位（`GO_GITHUB_RUN_TOKEN`）是否双轨冗余（同一会话面两把模型钥匙）——冗余则按席收窄到单轨。裁定结果回填 seat-gates 对应席 `token_scope` 与本件 §3.4 矩阵。**probe/droid/I8 面（`droid.yml`/`droid-probe*.yml`/`probe*.yml`/`i8-zero-escape-live-*`）的凭证面去留随裁定一并处理**——各面非领班席 job，但同写 `~/.factory/settings.json`（droid/probe 族）或注入 secrets（I8 编排器，含第 6 件 I8_TEAM_TRIGGER_PAT），属同一凭证最小化裁定的对象面。
3. **台账收口形态**：三件＋FACTORY_API_KEY＋I8_TEAM_TRIGGER_PAT 各 1 条 `[[key]]`（§3.3 条目①-④＋⑧），consumes=收口后「1 声明体行锚＋全树调用位锚＋env-check presence 位锚」（锚集边界=全生产 workflow 树——12 文件 82 行实测，含内联变体面与 I8 编排器面）；暴露面登记（写文件位 `~/.factory/settings.json` 入 `[[external_face]]`）。
4. **守卫负例（常驻）**：文本断言——**全生产 workflow 树**（`.github/workflows/*.yml`，12 文件实测边界）内「Write BYOM settings」**内联 heredoc 形态**出现次数>0 即红（收口后只允许声明体调用形态）；`secrets.WORKER_CI_KEY`/`GO_GITHUB_RUN_TOKEN`/`GW_TOKEN_KNOWN`/`FACTORY_API_KEY`/`PROJECTS_STATE_PAT`/`I8_TEAM_TRIGGER_PAT` 六名的 `${{ secrets.* }}` 展开位点集合≠台账 consumes 预期集即红（对账判据 1 的文本层，位点扫描边界=全生产 workflow 树——与判据、位点集三者同边界，round-2 口径）。

**清零判据**：11 声明体位点全部变为单行调用＋内联变体面（droid-probe2/probe3）收口或禁改登记；六名 secrets 展开只存在于声明体 env 区块（或 env 直传单区块）；scope 矩阵获大哥裁定并回填两件（seat-gates token_scope＋本件 §3.4）；守卫负例常驻 CI（扫描边界=全生产 workflow 树）。

### 2.4 图外件④：verdict.json/md 顶层孤儿件

**四要素速览**

| 要素 | 内容 |
|---|---|
| 现位置 | mission 工作区顶层 `verdict.json`/`verdict.md` 两件（生成时点 2026-11-27T08:07；非 repo 树内、非 git tracked——`git ls-files` verdict 命中仅 docs/evidence/ 档案件与 scripts/team/ 脚本名，零 repo 树孤儿） |
| 图外性判定 | 位置孤儿（文件名在链上有唯一语义＝final verdict，位置在链外顶层，无采认链背书）＋生成演员未登记（repo 链上无「工作区顶层 verdict 产出」步骤）＋消费面不明且具冒充风险（墙权威 pick 口径下顶层件可能被人工误读为权威终局） |
| 收编/禁绝 | 禁绝（清理两件）＋收编（verdict 系命名空间合法落点声明＋防复活负例＋台账 `[[orphan]]` 登记） |
| 责任席位 | 写板席（recorder——verdict 系命名空间主人）；清理动作＝大哥/人工（本 mission 边界条款禁动）；防复活＝写板席门清单 artifacts 合法落点＋adopt/merge 步路径校验（施工面） |

**现状与锚**：生产链上 verdict 系文件的合法链位是 run 工作区与墙 artifact（`salvage_verdict.py` 逐件落盘 verdict-partial.json→verdict-droid.json/md→adopt 采认→pick_verdict_from_wall 墙权威 pick，锚件 2 §3/§6）。repo 树内 tracked 的 verdict 件全部在证据档案面（`docs/evidence/v3-gate-rerun/**`）与脚本名——**树内零孤儿**。孤儿在 mission 工作区顶层：两件内容为一次 pass 的 verdict 产物形态（overall/pytest_exit/processes 结构），生成演员不在 repo 链内（本地会话/dry-run 落盘），AGENTS.md mission 条款「不动 verdict.json/verdict.md」确认其运行态产物身份。

**图外性判定（三条成立）**：

1. **位置孤儿**：`verdict.json/md` 在链上有唯一语义（final verdict），链上合法落点是 run 工作区与墙 artifact；工作区顶层不是任何席位门清单 `artifacts` 登记的落点。
2. **生成演员未登记**：repo 链上不存在产出「顶层 verdict」的步骤；生成者（本地会话）无门清单、无采认链。
3. **冒充风险**：本仓终局采认口径是墙权威（`pick_verdict_from_wall.py` fail-closed，`team.yml:4420`），顶层件无采认链背书，存在被误读为权威终局的风险。

**禁绝＋收编方式**：

1. **即时清理（禁绝，大哥/人工）**：顶层两件移入证据档案面或删除。本 mission 边界条款禁动该两件，本稿只登记其指纹位（文件名/生成时点/内容形态）与处置令，执行归施工单或大哥。
2. **命名空间收口（收编，施工面）**：写板席门清单 `artifacts` 面声明 verdict 系**合法落点白名单**（run 工作区链位＋墙 artifact＋证据档案面），其余位置＝非法落点；adopt/merge 步路径校验（施工落）拒绝白名单外落点输入。
3. **防复活负例（常驻）**：caps-gate 载体文本断言——repo 树内出现 `verdict*.json/md` 且不在证据档案面白名单即红。工作区顶层（repo 外）面无 CI 执法点——诚实登记：顶层守卫载体是 mission 目录巡查/手工巡检（判据入 §4 表），**本设计稿执法面只覆盖 repo 树**。
4. **台账登记**：本件入 `[[orphan]]` 表（kind=orphan-artifact、生成时点、处置=待清理、防复活判据）；对账判据「工作区顶层 verdict 孤儿=0」。

**清零判据**：顶层两件已清理（人工确认）；合法落点白名单入写板席门清单；防复活负例常驻 CI；`[[orphan]]` 表该项转 cleared。

### 2.5 图外件⑤：env-check 五 secrets 全量入环境

**四要素速览**

| 要素 | 内容 |
|---|---|
| 现位置 | `env-check.yml:82-86`（gate 步 env 五件全量注入：S_FACTORY_API_KEY/S_WORKER_CI_KEY/S_GW_TOKEN_KNOWN/S_GO_GITHUB_RUN_TOKEN/S_PROJECTS_STATE_PAT）；`:238-240`（wall 步 env 三件再展开）；`:24-34`（workflow_call secrets 声明五件）；消费面：presence 检查（`:155-163` 区段，5 名单布尔）、板面探测 PAT（`:194-200`）、`scripts/team/env_check_wall.py:65-67`（只读 3 件布尔入墙切片） |
| 图外性判定 | wall 步 3 件重复展开（env_check_wall 与 gate 步布尔重复消费）＋值在场暴露面未登记（gate 步为 presence 布尔而使五件真值全部进入 job 环境——值只被布尔消费，暴露面大于消费面）＋注入位点无对账 |
| 收编/禁绝 | 收编（按消费分离注入：wall 步归零改读对账面；gate 步暴露面登记进台账＋注入位点对账） |
| 责任席位 | env-check 零号门（非席位，门清单随总装单列）；施工＝写板席；对账＝caps-gate；台账＝钥匙面（§3.3 条目①-⑤consumes） |

**现状与锚**：env-check 是零号门（锚件 2 §8）。gate 步把五 secrets 全量注入 job 环境（`:82-86`），消费只有两处：检查 4 的 presence 布尔（`:155-163` 区段，`bool(os.environ.get("S_"+name))`）与板面探测的 PAT 真消费（`:194-200`）。墙切片步再注入三件（`:238-240`），但 `env_check_wall.py:65-67` 只读 `FACTORY_API_KEY`/`WORKER_CI_KEY`/`PROJECTS_STATE_PAT` 三件布尔——与 gate 步 results.tsv 已产出的 PASS/FAIL 行重复。

**图外性判定（三条成立）**：

1. **重复展开**：wall 步 3 件注入与 gate 步布尔消费重复——同一信息两个取值路径，其中一路（env 读值）是多余暴露。
2. **暴露面＞消费面**：gate 步为 presence 布尔而使五件真值全部在场（环境变量持真值）；布尔消费本不需要值在场，这是平台机制（GitHub 不提供 runner 内 secret 存在性免值查询）下的**机制性最小暴露**——但现状未登记该暴露面，也无「位点=最小」的对账。
3. **注入位点无对账**：env-check.yml 的 secrets 展开位点集无登记，新增展开（如未来加一步再注入某件）无守卫可红。

**收编方式（按消费分离注入）**：

1. **wall 步归零**：`env_check_wall.py` 删 `:65-67` 的 `os.environ` secret 读值段，三件布尔改从 gate 步 `env-check-results.tsv` 的 PASS/FAIL 行解析继承（tsv 已含 Secret 名单行）；`env-check.yml` wall 步 env 删 `:238-240`。施工后「全量入环境」变「按消费入环境」：gate 步 5 件（presence 检查语义需要＋板面探测 PAT 真消费）＋wall 步 0 件。
2. **暴露面登记**：gate 步 5 件注入位点（`:82-86`）登记进台账对应 `[[key]].consumes` 并注记「presence 布尔消费，值在场（机制性最小面）」——暴露面从无登记变登记面。
3. **位点对账（守卫负例，常驻）**：文本断言——env-check.yml 的 `${{ secrets.* }}` 展开位点集合=台账预期集（gate 步 5＋workflow_call 声明 5），多出即红（orphan-secret-expansion 判词，§3.6 判据 1）。
4. **一致性对账**：墙切片 secrets 布尔与 gate 步 tsv 判定一致性测试（目标态新增，防两路取值漂移）。

**清零判据**：`env_check_wall.py` 零 `os.environ` secret 读值；env-check.yml secrets 展开位点=登记集；一致性对账测试在树；台账 consumes 锚更新（wall 步三锚删除）。

### 2.6 图外件⑥：memory/ 运行态图外会话面

**四要素速览**

| 要素 | 内容 |
|---|---|
| 现位置 | repo `memory/` 运行态树（untracked：kb/log/docs/inbox/archive 等）；会话记录面实例 `memory/log/2026-11-27-sessions.md`（本 mission 各 worker 会话的 token/工具调用/摘要逐段记录；59 轮四问题①的原始记录位在该面 L586-589 区段——点火任务书段）；工作区顶层 NOW.md/INDEX.md 同面；hook 全局态根 `~/.memory-core/`；注入面 `~/.factory/bin/memory-hook`（session-start 注入 AGENTS.md 指引块） |
| 图外性判定 | 执行面图外（hook 进程在席位门清单之外运行与写入）＋会话面图外（完整会话记录不进墙、不经采认，却已是流水线真相的实际存储位——四问题①证据只存在于此面）＋untracked 结构性图外（AGENTS.md 明令不 commit，永在 git 墙外） |
| 收编/禁绝 | 收编（接口收口：图外记录作证据须先入库转图内证据对象；席位门清单显式禁写 memory/；台账 `[[external_face]]` 登记）——不收编其运行 |
| 责任席位 | 接口收口＝改计划席（replan 输入面）＋写板席（证据入库规范）；边界声明＝领班席（mission 编排面）；台账登记＝钥匙面 |

**现状与锚**：memory/ 是 memory-core hook 体系的运行态树（跨会话记忆/日志/知识库），untracked（仓库 AGENTS.md 明令不 commit 不手改）。`memory/log/2026-11-27-sessions.md` 逐段记录会话流水（模型/token/工具调用/摘要）——本 mission 的调研与设计会话全部在其记录面内；59 轮四问题①（replan 虚构死因）的原始记录恰在此面（repo docs 证据链止于第 58 轮，调研真源明载）。

**图外性判定（四条成立）**：

1. **执行面图外**：hook 进程与会话写入不经任何席位门清单——其写入面、触发面、存储位都在墙外。
2. **会话面图外**：会话记录面不进墙、不经 validator 采认，是一个完整的「图外会话」证据库。
3. **真相职能外溢（收编需求的实证）**：四问题①的原始记录只存在于此面——图外面已在实际承担「流水线真相存储」职能，而 replan 输入面若直接引用它即是以图外未采认记录为死因佐证（虚构死因的同类缺口）。
4. **untracked 结构性图外**：永不入 git，任何 repo 侧守卫对其树内内容无执法点。

**收编方式（接口收口，不收编运行）**：

1. **定性声明**：memory/ 是**图外设施**，定位＝开发支撑面（跨会话记忆），不是流水线图内件；v3.0 不收编其运行（无权亦无必要），收编其对流水线的**输出接口**。
2. **证据入库单点（图内收口）**：图外记录要作为死因佐证/采认输入，必须先经「证据入库」转写为图内结构化证据对象（handoff-schemas 的证据对象，由核查环节构造），禁直接以 memory 路径作叙事佐证——落位：replan 输入面死因注入只认墙 worker-delta 三字段＋图内证据对象；memory/log 只给人看（对位交接物铁律「自由文本只给人看，不承载判定」）。施工落：replan prompt 生成面的佐证字段 schema 类型=图内证据引用（契约断言）。
3. **门清单禁写**：全部席位门清单 `artifacts`/`governance_face` 显式不含 memory/（写授权=无）；caps-gate 文本层不变量——workflow 文本/单源模板零 memory/ 写路径（现状恒真，登记为恒真不变量防未来引入）。
4. **台账登记**：memory/ 面入 `[[external_face]]`（kind=external-state-face，非钥匙），消费锚=四问题①证据指针，处置=接口收口（上述 2/3）。
5. **诚实边界**：hook 注入面（AGENTS.md 注入块）是平台级设施，本设计稿无权收编；登记其存在与「不承载判定」定性即闭环。59 轮四问题①的回归样本（F4）须从图内可构造（worker-delta 注入路径），不依赖图外面还原现场。

**清零判据**：席位门清单零 memory/ 写授权；replan 佐证字段 schema 断言在树；`[[external_face]]` 条目在台账；四问题①回归样本图内可构造。

---

## §3 钥匙总管理台账设计（M2 口径）

### 3.1 承载文件与铁律（照抄形制要点 9）

**承载文件（目标态）**：`docs/specs/foreman-keys.toml`（施工落 repo；本稿定 schema 与预填面）。形制照抄引擎 `docs/specs/key-registry.toml`（form-basis 要点 9 原物锚：头注与铁律 `key-registry.toml:2`/`:11-16`、词表 `:25-33`、schema_version `:38`、meta 面与首条目 `:47-75`）：

1. **零密钥值**：只记名与元数据；契约测试 value_leak_scan 以常见前缀族（`ghp_`/`gho_`/`fk-` 等）全文件扫描（铁律原文 `key-registry.toml:11-13`）。本稿清零前唯一例外位＝I8-B 夹具哑值（`team.yml:419`，显式登记例外，拆除批消除——§2.2）。
2. **schema 一次定死＋同批改锁**：键集与词表硬编码在契约测试（`tests/test_foreman_keys_contract.py`，目标态新增）；增删键/词表须同批改契约测试（铁律原文 `key-registry.toml:14-16`）。
3. **只登记不轮换**：在役钥匙「只盘不动」；作废/退役走施工单＋回读验证后改 status＋append-only 流水（铁律原文 `key-registry.toml:21-24` 口径）。
4. **三轨归一参考**：领班侧轨道＝①repo secrets（在役五件＋备用一件 CI_KEY，gh secret list 六名口径，2026-11-28 实测）②runner 会话配置面（`~/.factory/settings.json`，`[[external_face]]`）③repo variables（I8-B 夹具假 PAT，zombie 轨）。

### 3.2 台账 schema（一次定死）

```toml
# docs/specs/foreman-keys.toml —— schema 样例（目标态；施工时按本段落树＋契约测试同批）
schema_version = 1

[meta]
owner = "M-WALL"                      # 面墙 specs 面（对位引擎 M-SPEC 口径；施工时按模块 id 裁定命名）
registry_kind = "foreman-key-registry"
value_policy = "zero-values-names-and-metadata-only"
change_ledger = "docs/wall-v3/key-ledger.md"   # append-only 动作流水（目标态）
baseline = "564ce30"                  # 登记基线（R58-D 收尾态）
inventory_date = "2026-11-27"
repo_secret_source = "在役五件＋备用一件 CI_KEY（gh secret list 六名口径，2026-11-28 实测；CI_KEY 零消费=zombie 轨备案，§3.3 备考行；CI 内 github.token 无列名单权限——对账载体见 §3.6 判据 5）"

# 词表（硬编码进契约测试；增删须同批改 tests/test_foreman_keys_contract.py）
# nature：use=使用钥匙（只消费既有能力）／cap_change=改能力钥匙（能改仓库/链上能力面：写板终态、建单关单、push、铸 PR）
# status：active=在役／dormant=休眠（登记在册消费链停机）／zombie=零消费者（作废候选）／revoked=已作废（回读验证在案）
# access：read／write／read_write／verify

[[key]]                                # 8 字段固定（name/kind/holder/access/nature/status/opens/consumes）＋notes/track_ref 可选
name = "PROJECTS_STATE_PAT"
kind = "github_pat"
holder = "repo secret（值源 1P sever GitHub 族；条目名施工盘点回填）"
access = "read_write"
nature = "cap_change"                  # 板面 Status=链终态权威面（team.yml:4599 审计镜像声明），写板=改终态能力
status = "active"
opens = "板面写（装配席单点）＋板面探测（env-check）＋漂移对账读（§2.1 再同步）"
consumes = [
    ".github/workflows/team.yml:4431",   # PAT 注入（写板单点）
    ".github/workflows/team.yml:4441",   # project_state_write 调用
    ".github/workflows/env-check.yml:86",# gate 步注入
    ".github/workflows/env-check.yml:195",# 板面探测真消费
    ".github/workflows/i8-zero-escape-live-orchestrator.yml:102",  # I8 编排器探针注入（五组面之一）
]
notes = "全链唯一板面写令牌； PAT 时间线演员定性=第 50 轮口径（docs/W-14-写板活验通过判据-修订.md）"
track_ref = "docs/wall-v3/out-of-graph-artifacts.md §2.1/§2.5"

[[key]]
name = "I8_TEAM_TRIGGER_PAT"
kind = "github_pat"
holder = "repo secret（值源 1P；条目名施工盘点回填）"
access = "read_write"
nature = "use"                          # 触发凭证（发 issue 评论点火链路），非改能力钥匙；消费侧选择权对位引擎 key-registry.toml:27-28 词表
status = "active"
opens = "I8 编排器触发面（五组 job 注入：i8-zero-escape-live-orchestrator.yml:100/:182/:256/:308/:345）；team.yml 生产链零消费"
consumes = [
    ".github/workflows/i8-zero-escape-live-orchestrator.yml:100",
    ".github/workflows/i8-zero-escape-live-orchestrator.yml:182",
    ".github/workflows/i8-zero-escape-live-orchestrator.yml:256",
    ".github/workflows/i8-zero-escape-live-orchestrator.yml:308",
    ".github/workflows/i8-zero-escape-live-orchestrator.yml:345",
]
notes = "全树唯一使用面=I8 编排器（round-2 全树口径补条）；零值登记"
track_ref = "docs/wall-v3/out-of-graph-artifacts.md §2.3/§3.4"

[[orphan]]                             # 孤儿件表（④收编面）
kind = "orphan-artifact"
name = "verdict.json / verdict.md（mission 工作区顶层）"
generated_at = "2026-11-27T08:07"
disposition = "待清理（大哥/人工）；防复活判据=写板席 artifacts 合法落点白名单＋caps-gate 负例"
track_ref = "docs/wall-v3/out-of-graph-artifacts.md §2.4"

[[external_face]]                      # 图外状态面登记（非钥匙轨）
kind = "external-state-face"
name = "memory/ 运行态树（untracked）＋~/.memory-core/ hook 态根＋~/.factory/settings.json runner 会话配置＋内联 BYOM 变体面（droid-probe2.yml:37、probe3.yml:51/:60 写位——收口批改声明体调用或显式禁改）"
disposition = "接口收口（证据入库单点＋席位禁写）；内联变体面随件③收口批处置；不收编运行"
track_ref = "docs/wall-v3/out-of-graph-artifacts.md §2.3/§2.6"

[[dangling_name]]                      # 防幽灵复活表
name = "I8_LIVE_B_INVALID_GH_TOKEN（repo variables，ghp_ 前缀族哑值）"
status = "zombie"                      # ②拆除批后：消费面=0；探针退役批回读验证后转 revoked
track_ref = "docs/wall-v3/out-of-graph-artifacts.md §2.2"
```

**设计说明**：四表结构对位引擎五表（repo_secret/dangling_name/repo_variable/mac_face/onepassword_item）的归口逻辑：[[key]]＝在役与待处置钥匙正表；[[orphan]]＝本仓特有的链外产物面（引擎以封印指纹覆盖，本仓 verdict 孤儿是产物面孤儿）；[[external_face]]＝非钥匙的状态/配置面（memory 树、runner 会话配置、探针 workflow 族）；[[dangling_name]]＝防复活（牺牲品链载体，§3.6 判据 4）。

### 3.3 现状登记面（repo-secret 名册六条一处陈述：①-⑤在役＋⑥备用 CI_KEY；⑦repo-variable 哑值与⑧I8_TEAM_TRIGGER_PAT 跨轨登记随表备考——round-3 实测 `gh secret list` 六名：①②③④⑤＋CI_KEY）

| # | name | kind | access | nature | status | opens（消费面） | consumes 锚 |
|---|---|---|---|---|---|---|---|
| ① | FACTORY_API_KEY | factory_cli_key | read | use | active | droid CLI 会话模型面（team.yml 8 席位会话步 env 直传＋droid/droid-probe/probe3/probe6/droid-probe2 探针面＋env-check gate/wall＋c-fixture 探针） | team.yml `:157/:568/:1501/:1916/:2209/:2757/:3738/:4147`＋`droid.yml:62`＋`droid-probe.yml:46`＋`droid-probe2.yml:17`＋`probe3.yml:40`＋`probe6.yml:44`＋env-check.yml `:82/:238`＋c-fixture `:41`——全树 16 行 |
| ② | WORKER_CI_KEY | worker_gateway_key | read | use | active | BYOM headers `x-ci-key` 位＋probe 族网关鉴权 | 声明体位点：team.yml `:120/:531/:1463/:1883/:2178/:2725/:3705/:4115` 区段＋`droid.yml:25`＋`droid-probe.yml:13`＋`droid-probe2.yml:15`＋`probe3.yml:15/:38`＋`probe6.yml:10` 区段＋env-check.yml `:83/:239`＋c-fixture `:42`＋probe.yml `:16/:22`＋probe4.yml `:10`＋probe5.yml `:10`——全树 21 行；③收口后=1 声明体锚＋全树调用锚 |
| ③ | GW_TOKEN_KNOWN | cf_ai_gateway_run_token | read | use | active | BYOM headers `cf-aig-authorization` 位 | 声明体位点：team.yml 8 位点区段＋`droid.yml:25`＋`probe6.yml:10` 区段（droid-probe.yml/droid-probe2.yml 无此件）＋env-check.yml `:84`＋probe5.yml `:11`——全树 12 行 |
| ④ | GO_GITHUB_RUN_TOKEN | github_pat（kind 初判，装配盘点回填） | read | use | active | BYOM `apiKey` 位（模型网关鉴权）＋probe 族 | 声明体位点（同②11 位点区段＋`droid-probe2.yml:16`＋`probe3.yml:39`）＋env-check.yml `:85/:239`＋I8 编排器 `:101/:183/:257/:309/:346`＋probe4.yml `:11`＋probe6.yml `:13` 区段——全树 20 行 |
| ⑤ | PROJECTS_STATE_PAT | github_pat | read_write | cap_change | active | 板面写（装配席单点）＋板面探测＋漂移对账读＋I8 编排器探针注入 | `team.yml:4431/:4441`＋env-check.yml `:86/:195/:240`＋I8 编排器 `:102/:184/:258/:310/:347`（样例见 §3.2）——全树 8 行 |
| ⑥ | GITHUB_TOKEN（github.token） | platform_builtin | read_write | use | active | per-run 临时令牌，按席 token_scope 面（seat-gates §2 逐席已登记：lead `:79/:241`、worker commit `:710`、prep `:1321`、replan 落单 `:2423`、assemble `:4448/:4659` 等） | 参考条目不占编号（照引擎 GITHUB_TOKEN 先例 `key-registry.toml:36-37`） |
| ⑥ | CI_KEY（备用件，2026-11-28 实测在列） | gateway_key（族初判，装配盘点回填） | read | use | zombie | 零消费（grep 全树零展开零调用；probe4/probe5 的 `CI_KEY` env 名实为 WORKER_CI_KEY 展开，非此件——`probe4.yml:10`/`probe5.yml:10`） | 零锚；gh secret list 备考名，施工盘点批裁定退役或回役 |
| ⑦ | I8_LIVE_B_INVALID_GH_TOKEN | github_pat（哑值） | read | use | zombie | I8-B 活验探针（改造后）；生产消费面=0 | 现生产位 `team.yml:419/:430`（②拆除批消除）→改道探针 workflow→退役批 revoked→[[dangling_name]] |
| ⑧ | I8_TEAM_TRIGGER_PAT（跨轨备考：repo secret 名单 gh secret list 实测不含此名——仅 I8 编排器 env 展开登记，是否独立在役 secret 装配盘点回填） | github_pat（kind 初判，装配盘点回填） | read | use | active | I8 编排器触发面（五组 job 注入：点火/编排/探针面）——team.yml 生产链零消费 | `i8-zero-escape-live-orchestrator.yml:100/:182/:256/:308/:345`——全树 5 行；零值登记（值不入稿）；scope 裁定随 §3.4 呈裁面 |

另登记非钥匙轨：`[[orphan]]` 一条（④）、`[[external_face]]` 四条（memory 树、runner 会话配置、探针/夹具 workflow 族、内联 BYOM 变体面 droid-probe2.yml/probe3.yml）、`[[dangling_name]]` 一条（⑦退役后落位）。BYOM 三件（②③④）的按席 scope 差异见 §3.4；⑧I8_TEAM_TRIGGER_PAT 的 scope 裁定随 §3.4 呈裁面一并处理。全树口径：12 workflow 文件/6 secret 名/82 展开行实测（`grep -n 'secrets\.' .github/workflows/*.yml`）。

### 3.4 use/cap_change 定性＋按席差异化 scope（对账基座）

**定性判据**（照引擎词表 `key-registry.toml:25-28`）：只消费既有能力＝use；能改仓库/链上能力面（写终态权威面、建单/关单、push、铸 PR）＝cap_change。台账 nature 字段八条中唯⑤ PROJECTS_STATE_PAT 为 cap_change（板面 Status=链终态权威，`team.yml:4599`——⑧的触发面消费与⑤同一令牌轨，三处定性一致）；⑥ CI_KEY 与⑧ I8_TEAM_TRIGGER_PAT 为 use——⑧是触发凭证（I8 编排器以 PAT 发 issue 评论点火，消费的是既有 issue-comment 能力）而非改能力钥匙，编排器消费侧的选择权住 `i8_select_gh_trigger_token.sh`（优先 PROJECTS_STATE_PAT，⑧为回退），领班侧不因持有触发凭证获得新能力；⑦ repo-variable 哑值沿旧表登记为 use（无真值即无改能力面）；github.token 虽按席可写（issues/pull-requests/contents），其定性随席位 token_scope 已在 seat-gates 逐席登记（platform_builtin 轨不重复定性，参考条目注记）。

**按席差异化 scope 矩阵**（凭证面；席位面以 seat-gates §2 为准，本表是凭证维度的对账视图）：

| 席位 | 会话步 GitHub 令牌 | BYOM 三件 | FACTORY_API_KEY | 呈裁项 |
|---|---|---|---|---|
| lead | 会话步无（建单/评论步 github.token `:79/:241`） | 全套（三件） | 有 | — |
| worker/worker2 | 会话步零令牌；commit 步 github.token `:710` | 全套 | 有 | 呈裁②（双轨冗余） |
| validate/revalidate/validate2/revalidate2 | 零（双置空 `:1390-1391/:1502-1503` 面） | 全套 | 有 | 呈裁①（validator 最小集）＋呈裁② |
| replan | 会话步零；落单步 github.token `:2423` | 全套 | 有 | 呈裁② |
| prep/prep2 | 报告步 github.token `:1321` | 无（无 droid） | 无 | — |
| assemble | github.token `:4448/:4659` | 无（无 droid） | 无 | — |
| recorder（目标态独立席） | 无 | 无（承载面同 validator，目标态裁定） | 无 | — |

呈裁两条（§2.3 已述，裁定结果回填本表与 seat-gates token_scope）：**①** validator 族 BYOM 三件最小集（尤其 `cf-aig-authorization`/`apiKey` 位必要性）；**②** FACTORY_API_KEY 与 BYOM `apiKey` 位（GO_GITHUB_RUN_TOKEN）双轨冗余裁定。裁前保守登记现状全量；裁后收窄＋caps-gate 对账判据同步收紧。

### 3.5 消费锚体系（8→1 收口后的锚形态）

- **锚定义**：consumes 字段逐条 `file:line`；锚判据＝该行含 secrets 展开（`${{ secrets.X }}`）、env 注入键、或声明体调用行。台账行锚随批登记进设计契约 fixture（`tests/fixtures/wall-v3/design-contract.json` anchors 数组——round-3 起：台账 consumes 锚、§3.3 表 consumes 锚列、design-contract.json 三处同批增删，防台账锚单边漂移；round-3 实证：⑤行内 `env-check.yml:240` 锚实为 wall 步 `S_WORKER_CI_KEY` 展开行，内容不对应，已删——台账锚的内容核查与解析核查同纪律）。
- **收口前后形态**：现状②③④三件各 11 展开锚（team.yml 8＋droid.yml 1＋droid-probe.yml 1＋probe6.yml 1；GW_TOKEN_KNOWN 实为 10——droid-probe.yml 双件形态）＋内联变体面锚（droid-probe2/probe3）＋probe 族散点锚＋2 presence 锚＋I8 编排器锚（⑤/⑧ 面）；③收口后变「1 声明体行锚＋全树调用位锚＋presence 锚」——调用位是消费锚（真实消费），声明体是登记锚（唯一展开点）；内联变体位收口为声明体调用并入调用位锚集。⑤收口后 env-check 消费锚从「5+3」变「5」（wall 步三锚删除）。
- **锚执法**：锚集对账进 caps-gate（§3.6 判据 1/2）；锚漂移（行号漂移、锚定内容失配）即红（判词 anchor-drift）——施工单改凭证接线必须同批改台账（对位引擎「文件增删不改语义（点名 workflow 即消费面）」口径，`key-registry.toml:19-20`）。

### 3.6 对账判据（五判＋牺牲品样本）

1. **展开位点对账**：生产 workflow 树的 `${{ secrets.* }}` 展开行集合=台账 consumes 锚集。**扫描边界＝全生产 workflow 树**（`.github/workflows/*.yml` 全集——round-2 裁定：判据 1、守卫负例（§2.3 收编方式 4）、本表位点集三者同边界，硬规则⑨「全部凭证」全树口径；现状实测 12 文件/6 名/82 行）。多出=orphan-secret-expansion 红（图外凭证注入检出）；少了=anchor-drift 红。载体：caps-gate/契约测试（文本 grep 对账）。
2. **值泄漏扫描**：常见前缀族全文件扫描（铁律对位 `key-registry.toml:11-13`）。清零前唯一登记例外位=`team.yml:419` 夹具哑值（②拆除批消除例外）；例外位采用「显式登记＋限期消除」纪律，禁止常驻例外。
3. **旁路检出**（三面巡检）：环境面（`~/.factory/settings.json` 写入位点=声明体单点——③收口判据）；本地面（工作区顶层 verdict 孤儿=0——④判据）；板面（PAT 时间线演员=PAT 持有人单点，翻板演员=0——①判据）。
4. **牺牲品样本（防幽灵复活）**：对位引擎 REVOCATION_TEST_KEY 牺牲品链——领班侧牺牲品＝I8-B 假 PAT（⑦，已是哑值样本）：走「登记（zombie）→探针改道→退役批回读验证（打不开）→revoked→[[dangling_name]]」全链演练；此后常驻 dangling 表，任何同名/同前缀复活即红。
5. **名单对账**：在役 repo secrets 实测名单=5（①-⑤），另实测在列备而无消费链的 CI_KEY 一件（zombie 轨备考，⑧I8_TEAM_TRIGGER_PAT 的在役定性随装配盘点回填）——repo-secret 名册六条一处陈述以本判据为口径。载体裁定（呈大哥裁二选一）：**a** 季度人工 `gh secret list` 对账留痕（CI 内 github.token 无列名单权限——平台边界，`env-check.yml` 已按「边界声明非通过」口径处理同类面）；**b** 若 PROJECTS_STATE_PAT 具 admin 读面则机器对账（施工时实测其权限后定）。对账输出落 append-only 流水（`docs/wall-v3/key-ledger.md`，对位引擎 key-ledger append-only 口径 `key-registry.toml:7-8`；动作行五元组对位引擎 gate-ledger 口径——时戳｜动作｜who｜which｜what｜evidence，且「无回读不得记完成」，`docs/governance/gate-ledger.md:4/:12` 原物）。

**判词枚举（caps-gate 钥匙面初版，只增不改）**：`orphan-secret-expansion`／`anchor-drift`／`value-leak`／`unregistered-bypass-surface`（旁路面未登记）／`mixed-key-registry-change`（升级闸违例）。

### 3.7 升级闸与治理（禁抄项对位声明）

- **升级闸**：改台账文件＋守卫本体＋CI 守卫段的变更集须带显式声明行 `key-registry-change: true`（对位引擎 `REGISTRY_CHANGE_DECLARATION`，form-basis 要点 7 原物锚 `scripts/check_module_wall.py:131`），否则判 mixed-key-registry-change 红。
- **治理执法声明（禁抄项对位，round-2 事实重写）**：引擎墙 governance owner 门**现状＝enabled 在役执法**——repo 变量 `EVOLUTION_GOVERNANCE_ENABLED=enabled`（2026-11-26T19:50Z 设定，实测读取在场）＋workflow 开关 active；非属主治理 run 已判 failure 双红帧（PR #880/#881，governance job conclusion=failure，引擎证据 `evidence/step6-u-closeout/04-governance-enforcement-verification.md:11`（总判读行）、`:17`（变量 enabled 实读行）、`:103-104`（双红帧行））。「governance owner 门停用态」是过期 R-18 行（`05-risk-register.md:47`）登记的历史态，不得转抄为本件禁抄项口径。**剩余真实缺口如实登记**：governance 门非 required status check，不阻断合并——本件对应义务因此更重：钥匙面守卫与对账判据全部接 foreman-wall-ci 恒跑（接线语义有契约测试锁，对位要点 5）；登记面（docs/specs/**＋守卫本体）列入受保护路径面（运行时执法设计归主设计稿执法章，非页面开关），不允许领班侧复刻「门在役但不阻断」的形制而不补运行时执法。
- **CI 接线口径**：R-29 已裁两门（quality-gate / substrate-gate-suite，form-basis §11.2）——钥匙面守卫进 CI 的门归属按 foreman-wall-ci 既有恒跑面接线，不新设挂名门。

---

## §4 清零判据汇总（图外=0 的机器定义）

「图外=0」不是口号，是六条可断言判据＋三态纪律：

| # | 判据（可断言形态） | 负例/对账载体 | 施工/人工归属 |
|---|---|---|---|
| ① | 板面 timeline 零 `github-project-automation` 翻板事件；`board_drift` 对账步＋env-check 探测项在树 | F4 必死样本：翻板回归样本（59 轮四问题③） | 板侧=大哥人工；对账步=施工单（装配席步列） |
| ② | 生产 workflow 树（`.github/workflows/*.yml` 12 文件全树边界，round-3 起「四文件集」旧口径废止）零 `I8_LIVE_B` 与 PAT 前缀族命中；B 夹具文件在树；探针单全链红照旧 | caps-gate 负例：生产文本夹具/值前缀必红（扫描面=全树） | 施工单（lead 席默认删行落地＋探针改道）＋大哥（退役批） |
| ③ | BYOM 写入=声明体单点（内联 heredoc 形态计数=0）；六名 secrets 展开位点=台账锚集（扫描边界=全生产 workflow 树：12 文件/6 名/82 行实测口径——判据、守卫、位点集三者同边界） | caps-gate 负例：多声明体/锚集失配必红 | 施工单（声明体）＋大哥（scope 裁定） |
| ④ | 工作区顶层 verdict 孤儿=0（人工巡检）；repo 树内 verdict 件全在档案白名单 | caps-gate 负例：白名单外 verdict 落点必红 | 清理=大哥/人工；白名单+负例=施工单（写板席） |
| ⑤ | env_check_wall 零 os.environ secret 读值；env-check.yml secrets 位点=登记集；墙切片布尔与 gate tsv 一致性测试绿 | caps-gate 负例：位点集失配必红＋一致性测试 | 施工单（env-check 文本＋env_check_wall） |
| ⑥ | 席位门清单零 memory/ 写授权；replan 佐证字段=图内证据引用（schema 断言）；[[external_face]] 条目在台账 | 契约断言：佐证字段类型必红负例（F4 四问题①回归） | 施工单（门清单/replan 输入面）＋领班席（编排声明） |

**三态纪律**（照引擎普查表口径，form-basis 要点 10）：每件清零状态只能取 **cleared**（判据全绿）／**cleared-with-declaration**（判据绿但带显式边界声明——如⑤的机制性最小暴露、⑥的「不收编运行」）／**blocked**（判据不可达，显式登记阻塞面——如①板侧动作待大哥）。禁止虚称 cleared；blocked 件保留图外登记不除名。

**验收线归属声明**：本件只给判据与负例载体指针；必死样本桩设计（fake-droid 注入形态）与执法延迟口径归 F4 底稿 `docs/wall-v3/acceptance-line-map.md` 与主设计稿验收线章（`failure-specs.md` 承载逐席失败规范四字段格与判据侧，桩形态与延迟口径不在其重复面——详见其头注「必死样本设计见姊妹底稿 acceptance-line-map.md」分工声明）——两处的判据引用以本件 §4 表为准绳（VAL-CROSS-002 一致性：清零后的每件归宿都在对应席位门清单内——①归装配席/零号门、②归 lead 席默认删行＋大哥退役批（workflow 编辑是治理行为，非任何会话席门清单写面；recorder 门清单不含 workflow 文本）、④归写板席命名空间、③归各席 token_scope（收口面=全树口径：11 声明体位点改单行调用＋内联变体面同批收口）、⑤归零号门、⑥归改计划席/写板席）。

---

## 附A 本件 file:line 锚清单（供锚解析器与后续 feature 复用）

> 锚判据＝文件在树、行号不越界、锚定内容含预期关键词。**本件新增锚（锚件 2 未覆盖者）标 ★；其余转引锚件 2/锚件 1，解析以其附表为准。**

| 锚 | 解析判据（该行应含） | 来源 |
|---|---|---|
| `.github/workflows/team.yml:7` | `v2.7.0 change note` | 锚件 2 §0 |
| `.github/workflows/team.yml:31` | `permissions:` | 锚件 2 §1 |
| `.github/workflows/team.yml:37` | `env-check:` | 锚件 2 §8 |
| `.github/workflows/team.yml:46` | `uses: ./.github/workflows/env-check.yml` | ★ |
| `.github/workflows/team.yml:117` | `Write BYOM settings (lead session)` | ★ |
| `.github/workflows/team.yml:120` | `WORKER_CI_KEY: ${{ secrets.WORKER_CI_KEY }}` | 锚件 2 §1（`:120`） |
| `.github/workflows/team.yml:123` | `SESSION_NAME: team-lead` | ★ |
| `.github/workflows/team.yml:134` | `x-opencode-session` | ★ |
| `.github/workflows/team.yml:157` | `FACTORY_API_KEY` | 锚件 2 §1 |
| `.github/workflows/team.yml:412` | `Post plan dispatch comment (B4/I4)` | ★ |
| `.github/workflows/team.yml:418` | `I8-B live only`（夹具注释行） | ★ |
| `.github/workflows/team.yml:419` | `I8_LIVE_B_INVALID_GH_TOKEN`（夹具变量行；`ghp_` 哑值在场，不转录） | ★ |
| `.github/workflows/team.yml:429` | `[I8] API墙活验 B 评论硬失败`（标题比较） | ★ |
| `.github/workflows/team.yml:430` | `export GH_TOKEN="$I8_LIVE_B_INVALID_GH_TOKEN"` | ★ |
| `.github/workflows/team.yml:432` | `fi`（命中分支收尾） | ★ |
| `.github/workflows/team.yml:4431` | `PROJECTS_STATE_PAT` | 锚件 2 §6 |
| `.github/workflows/team.yml:4441` | `project_state_write` | 锚件 2 §6 |
| `.github/workflows/team.yml:4599` | 板面权威审计镜像声明 | 锚件 2 §6 |
| `.github/workflows/team.yml:529` | `Write BYOM settings (worker session)` | ★ |
| `.github/workflows/team.yml:1460` | `Write BYOM settings (validator session)` | ★ |
| `.github/workflows/team.yml:1880` | `Write BYOM settings (validator revalidate session)` | ★ |
| `.github/workflows/team.yml:2176` | `Write BYOM settings (replan session)` | ★ |
| `.github/workflows/team.yml:2723` | `Write BYOM settings (worker round 2 session)` | ★ |
| `.github/workflows/team.yml:3702` | `Write BYOM settings (validator round 2 session)` | ★ |
| `.github/workflows/team.yml:4113` | `Write BYOM settings (validator revalidate round 2 session)` | ★ |
| `.github/workflows/droid.yml:25` | `Write BYOM settings (replica pattern, caller-side gateway auth)`（件③非领班面锚 1/3） | ★ |
| `.github/workflows/droid.yml:62` | `FACTORY_API_KEY`（件③锚） | ★ |
| `.github/workflows/droid-probe.yml:13` | `Write BYOM settings (same as droid.yml v5)`（件③非领班面锚 2/3） | ★ |
| `.github/workflows/droid-probe.yml:46` | `FACTORY_API_KEY`（件③锚） | ★ |
| `.github/workflows/probe6.yml:10` | `Write BYOM settings (replica pattern, caller-side gateway auth)`（件③非领班面锚 3/3） | ★ |
| `.github/workflows/probe6.yml:44` | `FACTORY_API_KEY`（件③锚） | ★ |
| `.github/workflows/droid-probe2.yml:15` | `WORKER_CI_KEY: ${{ secrets.WORKER_CI_KEY }}`（件③内联变体面锚；round-2 全树口径补） | ★ |
| `.github/workflows/droid-probe2.yml:17` | `FACTORY_API_KEY`（件③内联变体面锚） | ★ |
| `.github/workflows/droid-probe2.yml:37` | `~/.factory/settings.json`（内联写位） | ★ |
| `.github/workflows/probe3.yml:15` | `WORKER_CI_KEY`（件③内联变体面锚） | ★ |
| `.github/workflows/probe3.yml:38` | `WORKER_CI_KEY`（步 2 三件注入起，跨 :38-:40） | ★ |
| `.github/workflows/probe3.yml:51` | `customModels` 条目起（内联 settings.json 写位块 :51-:60——:60 为 json.dump 写文件行） | ★ |
| `.github/workflows/i8-zero-escape-live-orchestrator.yml:100` | `S_I8_TEAM_TRIGGER_PAT`（第 6 secret 展开首行；五组面 :100/:182/:256/:308/:345） | ★ |
| `.github/workflows/env-check.yml:24` | `secrets:`（workflow_call 声明面） | ★ |
| `.github/workflows/env-check.yml:82` | `S_FACTORY_API_KEY` | 锚件 2 §8（`:82-86` 区段） |
| `.github/workflows/env-check.yml:83` | `S_WORKER_CI_KEY` | ★ |
| `.github/workflows/env-check.yml:84` | `S_GW_TOKEN_KNOWN` | ★ |
| `.github/workflows/env-check.yml:85` | `S_GO_GITHUB_RUN_TOKEN` | ★ |
| `.github/workflows/env-check.yml:86` | `S_PROJECTS_STATE_PAT` | 锚件 2 §8 |
| `.github/workflows/env-check.yml:155` | `Secrets presence` | ★ |
| `.github/workflows/env-check.yml:194` | `S_PROJECTS_STATE_PAT`（板面探测消费） | ★ |
| `.github/workflows/env-check.yml:238` | `S_FACTORY_API_KEY`（wall 步再展开） | ★ |
| `.github/workflows/env-check.yml:240` | `S_PROJECTS_STATE_PAT`（wall 步再展开） | ★ |
| `.github/workflows/probe4.yml:10` | `CI_KEY: ${{ secrets.WORKER_CI_KEY }}`（env 名 CI_KEY 的真实源=WORKER_CI_KEY 展开） | ★ |
| `.github/workflows/probe5.yml:10` | `CI_KEY: ${{ secrets.WORKER_CI_KEY }}`（同上） | ★ |
| `.github/workflows/probe4.yml:15` | `x-ci-key: $CI_KEY`（CI_KEY env 消费行；源为 WORKER_CI_KEY） | ★ |
| `.github/workflows/probe5.yml:15` | `x-ci-key: $CI_KEY`（同上） | ★ |
| `scripts/team/env_check_wall.py:65` | `FACTORY_API_KEY`（os.environ 布尔读值） | ★ |
| `scripts/team/env_check_wall.py:67` | `PROJECTS_STATE_PAT`（同上） | ★ |
| `schemas/foreman-run.v1.schema.json:210` | `closeout_slice` | ★ |
| `schemas/foreman-run.v1.schema.json:214` | `project_state_written` | ★ |
| `docs/板面关单翻板-最小操作指引.md:3` | `repo 侧不可修` | ★ |
| `docs/板面关单翻板-最小操作指引.md:12` | `#761`（三单实测表首行） | ★ |
| `docs/板面关单翻板-最小操作指引.md:14` | `#764`（三单实测表末行） | ★ |
| `docs/板面关单翻板-最小操作指引.md:20` | `github-project-automation`（仓内零写入点结论） | ★ |
| `docs/板面关单翻板-最小操作指引.md:22` | 内建工作流系统演员结论 | ★ |
| `docs/板面关单翻板-最小操作指引.md:26` | `需大哥侧动作`（板侧操作节） | ★ |
| `docs/板面关单翻板-最小操作指引.md:37` | timeline 验证判据 | ★ |
| `.github/workflows/i8-zero-escape-live-c-fixture.yml` | 在树（C 型夹具独立 workflow 文件——B 型仓化对位形态） | ★（文件存在性锚） |
| `docs/specs/key-registry.toml:2`（引擎仓） | 钥匙总管理台账头注 | 锚件 1 要点 9 |
| `docs/specs/key-registry.toml:25`（引擎仓） | 定性词表（nature） | 锚件 1 要点 9 |
| `docs/specs/key-registry.toml:38`（引擎仓） | `schema_version = 1` | 锚件 1 要点 9 |
| `docs/governance/gate-ledger.md:4`（引擎仓） | 五元组格式 | ★ |
| `docs/governance/gate-ledger.md:12`（引擎仓） | 无回读不得记完成 | ★ |
| `memory/log/2026-11-27-sessions.md:586` | mission 点火任务书段（59 轮四问题原始记录位） | ★（运行态锚，只读引用） |

## 附B 图外件 × 席位 × 硬规则落位映射（主设计稿总装索引）

| 图外件 | 主责席位（清零后归宿） | 硬规则落位（architecture §8 映射） | 姊妹件引用 |
|---|---|---|---|
| ① 板面翻板 | 装配席（projects-write 单点＋board_drift 对账）＋env-check（探测项） | 规则⑤写入口收口（§写入口）＋规则⑩无兜底不留图外（§图外件清零） | seat-gates §2.6 assemble 门清单；F4 回归样本③ |
| ② I8-B 夹具 | lead 席（默认删行）＋大哥退役批（探针编排改道=验收席面） | 规则⑩（图外件清零）＋规则④必死样本（探针负例） | 主设计稿 §2.4 表 2（lead 多出的门默认删）；F4 探针负例 |
| ③ BYOM 11 位点 | 写板席（声明体）＋各席 token_scope＋大哥（probe 族 scope 裁定） | 规则⑨钥匙总管理（§钥匙台账） | seat-gates §2 各席 authorization；本稿 §3.4 |
| ④ verdict 孤儿 | 写板席（命名空间合法落点） | 规则⑩＋规则①（recorder 门清单 artifacts 面） | seat-gates §2.7；本稿 §3.2 [[orphan]] |
| ⑤ env-check 五 secrets | env-check 零号门（门清单随总装单列） | 规则⑨（暴露面登记＋位点对账） | 本稿 §3.3/§3.6；seat-gates §0 辅助面口径 |
| ⑥ memory/ 会话面 | 改计划席（输入面收口）＋写板席（入库规范）＋领班席（编排声明） | 规则②交接物结构化（证据入库）＋规则⑩ | handoff-schemas 证据对象；F4 回归样本① |
| 钥匙台账（全件底座） | 钥匙面（caps-gate 执法） | 规则⑨整条（§钥匙台账） | form-basis 要点 9；本稿 §3 全节 |
