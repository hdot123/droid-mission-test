# 现状能力面登记件（as-is capability inventory）——7 席位五要素

> 锚件 2/2（mission F1/design-inputs 产出）。领班面墙 API 设计稿 v3.0 的唯一现状真源：**后续 feature（F2/F3/F4/F5）引用 team.yml 现状行号一律以本件为准，不再直查 team.yml 重数行号**（mission AGENTS「行号真源」条款）。本件按 R58-D 收尾态（基线 564ce30）实读核实，2026-11-27 快照。
>
> 现状对象：`.github/workflows/team.yml`（4672 行）及其消费的 `scripts/team/`、`schemas/`、`.github/workflows/env-check.yml`。本件只登记现状，不改现状；行号锚格式 `路径:行号`，全部经实读核实，锚可解析判据＝文件在树、行号不越界、锚定内容含预期关键词。

---

## 0. 口径声明（读本件前必读）

**席位口径（7 席）**：领班 lead、工人 worker、验收 validator、改计划 replan、备料 prep、装配 assemble、写板 recorder。前六席对应 team.yml 的六个 droid/脚本 job；**写板席（recorder）现状无独立 job**——其职能由两处承载：①validate 席的逐件落盘纪律（validator prompt 单源 `validator_prompt_template.py`，team.yml:1515）；②prep 补卷器的机器兜底写（`worker_salvage.py`，team.yml:1223-1226 接线）。设计稿把写板立为独立席位是**目标态设计**，现状面按本段口径登记。

**二轮镜像口径**：worker2（team.yml:2697）/ workers2-wall-merge（:3029）/ prep2（:3107）/ validate2（:3618）/ revalidate2（:4010）是一轮对应席（worker/merge/prep/validate/revalidate）的镜像：分支后缀 `-r2`、validate2 带 flips 翻案记账（:3948 run_adopt_step 面）、revalidate2 一次性哨兵同构。**二轮席的门清单按一轮对应席同构适用**，本件对二轮席只登差异点，不重复五要素全表；revalidate/revalidate2 同理为 validate 的镜像变体（复用同一证据包，sha 不变）。

**辅助 job 口径**：workers-wall-merge（:851）与 workers2-wall-merge（:3029）是无 droid 纯脚本合并 job，作为工人席的墙出口合并面登记在工人席条目内，不占席位名额。env-check（:37）是零号门（非席位），单列 §8。

**版本口径现状**：team.yml 头部 change note 标 `v2.7.0`（team.yml:7），README 交付段另标 v2.9/v2.10 措辞——版本口径三处不一致（漂移细节见 §9 风险清单第 3 条）。设计稿 v3.0 起版并声明作废 v2.7~v2.10 账面墙口径，即在收口此漂移。

---

## 1. 领班席（lead）

| 要素 | 现状 | 锚 |
|---|---|---|
| **入口** | issue 评论触发（含 `@team-droid`，非 PR 评论），经 env-check 门放行：`needs.env-check.outputs.foreman_ok == 'true'`；下载墙 artifact；重复点名去重（dup 步） | `team.yml:52`（job 头）、`:31-34`（顶层触发权限面） |
| **出口** | `team/lead-plan-segments/*.json` 分段卡→机器 stitch 出 `team-plan.json`；[计划] issue＋[工序] sub-issues；派单评论（post_comment_hard --wall-patch plan_dispatch）；墙 patch（budgets.session_outcome、plan slice） | `team.yml:439-443`（plan artifact upload） |
| **工具面** | droid 会话**经包装器** run_droid_session.py --role lead（墙预算 600s，FOREMAN_RUN_PATCH=1），带 heartbeat＋lead 段闸线程；gh issue create/comment/api | `team.yml:203-204`（--wall foreman-run.json --role lead）、`scripts/team/foreman_run_lib.py:37-40`（lead droid_wall_sec=600） |
| **写目标** | repo 工作区任意文件（**无机器 F-1 类守卫，仅 prompt 纪律**「只写 team/lead-plan-segments/ 下新 JSON」）；issues（建计划单/子单/评论）；墙 patch | `team.yml:203`（会话步）；F-1 守卫仅在工人 commit 步存在（对照 §2） |
| **凭证** | BYOM 三件（WORKER_CI_KEY/GO_GITHUB_RUN_TOKEN/GW_TOKEN_KNOWN 写入 ~/.factory/settings.json）＋FACTORY_API_KEY＋GH_TOKEN=github.token（建单/评论步） | `team.yml:120`（WORKER_CI_KEY）、`:157`（FACTORY_API_KEY）、`:79`/`:241`（GH_TOKEN=github.token） |

**专有现状（图外件，F3 清零对象）**：派单评论步带 I8-B 活验夹具——按 issue 标题命中即把 GH_TOKEN 换成假 PAT 变量（生产 workflow 文本内嵌活验分支）。锚：`team.yml:419`（假 PAT 默认值 dummy 变量，ghp_ 前缀族夹具值本体不转录、见该行原文）、`:429-431`（标题命中换 token 逻辑：`:429` 标题比较、`:430` export、`:431` echo 说明）。

---

## 2. 工人席（worker，矩阵 max-parallel 3；镜像 worker2 :2697）

| 要素 | 现状 | 锚 |
|---|---|---|
| **入口** | `needs.lead.outputs.processes` 矩阵，每卡一会话 | `team.yml:503`（job 头）、`:508`（timeout-minutes: 25） |
| **出口** | 交付文件＋`team/handoffs/<pid>.md`＋`team/status/<pid>.json`（＋checks-failed.marker）；分支 `team/issue-N/run-R/<pid>`；handoff 评论（母单＋子单）；`worker-delta.json` 结构化结局（write_worker_delta.py 上墙） | `team.yml:836`（write_worker_delta.py） |
| **工具面** | **裸跑**：`timeout --signal=TERM --kill-after=30s 900s ~/.local/bin/droid exec --auto high …`——**不经 run_droid_session.py 包装器**；verify 步跑卡面 checks（subprocess 无超时）；commit 步 git push | `team.yml:599`（裸跑行）、`scripts/team/lint_workflow_budgets.py:16-18`（BARE_DROID 正则）＋`:43-51`（worker/900s 豁免分支：`:46` 豁免判断、`:49-51` 报错文案） |
| **写目标** | **F-1 机器守卫在此席位**：commit 步 `git reset --soft BASE_SHA` squash 会话自提交，changed-files 对卡面 allowed 集合比对，越界即拒；分支 push；issues 评论 | `team.yml:731`（git reset --soft）、`:710`（commit 步 GH_TOKEN=github.token） |
| **凭证** | BYOM 三件＋FACTORY_API_KEY；**会话步无 GH_TOKEN**（仅 commit 步有） | `team.yml:531`（WORKER_CI_KEY）、`:568`（FACTORY_API_KEY）、`:710` |

**工人墙出口（辅助 job）**：workers-wall-merge（always() 接纳上游 cancelled）读 delta 并集 completed_pids→产出 prep 门 prep_should_run（I1）。锚：`team.yml:851`、`:885`（merge_worker_deltas.py --wall）、`:860`（prep_should_run output 声明）、`:899-902`（投影步条件与计算）。墙上 worker 预算账面值 900（`foreman_run_lib.py:53-54`）与裸跑硬编码 900s 数值偶合，但**墙值不被 workflow 执行路径读取**——工人预算是账面非执法（详见 §9 风险 4）。

**worker2 差异点**：分支后缀 `-r2`；裸跑同款（`team.yml:2784`）；delta 上墙 `:3017`；merge 面 `:3060`/`:3077`；BYOM `:2725`；FACTORY_API_KEY `:2757`。

---

## 3. 验收席（validator；镜像 validate2 :3618、变体 revalidate :1779 / revalidate2 :4010）

| 要素 | 现状 | 锚 |
|---|---|---|
| **入口** | `needs.prep.result == 'success'`（revalidate：validate.outputs.should_revalidate=='true'＋一次性哨兵 revalidate_run_started fail-closed 拒二次）；下载墙＋证据包（manifest sha 门） | `team.yml:1382-1391`（job 头/needs/if/timeout 15m/permissions: {}/空 token env） |
| **出口** | `verdict-partial.json`（recorder salvage_verdict.py 逐件落盘）→`verdict-droid.json/md`→`verdict.json/md`；墙 validation 切片（adopt：run_adopt_step.py） | `team.yml:1721`（run_adopt_step.py） |
| **工具面** | droid 会话**经包装器** --role validator（墙预算 480s＋adopt 储备 120s）；prompt 单源 validator_prompt_template.py | `team.yml:1534-1535`（--role validator）、`:1515`（build_validator_prompt）、`foreman_run_lib.py:42-45`（validator droid_wall_sec=480、adopt_reserve_sec=120） |
| **写目标** | **无 GitHub 写权**：job 级与步级 GITHUB_TOKEN:""/GH_TOKEN:"" 双显式置空；证据防篡改＝事后 manifest sha 逐文件复验；工作目录 work/ | `team.yml:1390-1391`（job env）、`:1502-1503`（步 env） |
| **凭证** | BYOM 三件＋FACTORY_API_KEY；无任何 GitHub 令牌 | `team.yml:1463`（WORKER_CI_KEY）、`:1501`（FACTORY_API_KEY） |

**关联：recorder 职能现状（写板席承载点之一）**：validator prompt 单源内的逐件落盘纪律（salvage_verdict.py 逐件写 verdict-partial.json）是 prompt 文字纪律，无运行时效力；per-run 无 recorder 调用数墙字段、无报警（§9 风险 10，四问题④）。

**镜像差异点**：revalidate `:1779`（一次性哨兵面 `:1806-1816` 区段——「Refuse a second revalidate, stamp this run started (at most one, fail-closed)」步实读裁决修正：原记 `:1784-1788` 为 job 头区段 timeout/permissions/token env，非哨兵步）、validate2 `:3618-3627`（BYOM `:3705`、FACTORY `:3738`、步 env 置空 `:3739-3740`、prompt `:3752`、会话 `:3771-3772`、adopt/flips `:3948`）、revalidate2 `:4010-4019`（BYOM `:4115`、FACTORY `:4147`、env 置空 `:4148-4149`、prompt `:4161`、会话 `:4180-4181`、adopt `:4338`）。

---

## 4. 改计划席（replan）

| 要素 | 现状 | 锚 |
|---|---|---|
| **入口** | 墙 `replan_gate.should_replan`（validate 或 revalidate 投影）；下载 plan/verdict/evidence | `team.yml:2141`（job 头）、`:2154`（timeout 15m） |
| **出口** | `team-plan-v2.json`（changes 数组）；[工序] v2 新 sub-issue＋旧子单关闭（not planned）；replan 通知评论（--wall-patch replan_notice_*） | `team.yml:2638`（关单步 GH_TOKEN） |
| **工具面** | droid 会话**经包装器** --role replan（墙预算 480s）；会话步 GITHUB_TOKEN:""/GH_TOKEN:""；prompt 由 validate 面脚本内置推断生成（死因叙事，见 §10-①） | `team.yml:2405-2406`（--role replan）、`:2210-2211`（会话步 env 置空）、`foreman_run_lib.py:48-50`（replan 480） |
| **写目标** | team-plan-v2.json（落单步机器校验：覆盖集、claim 不相交、受保护路径）；issues（建单/关单/评论）；墙 patch | `team.yml:2420-2423`（落单步：`:2420` 步名、`:2423` GH_TOKEN=github.token 同 job 混合） |
| **凭证** | BYOM 三件＋FACTORY_API_KEY＋落单步 github.token（会话步无 token） | `team.yml:2178`（WORKER_CI_KEY）、`:2209`（FACTORY_API_KEY）、`:2423`（GH_TOKEN） |

**专有现状**：死因叙事含脚本内置推断——「分支缺席→F-1 检查拒绝」文案写死在 replan 步 heredoc，且无机器记录佐证（§10-① 四问题①）。锚：`team.yml:2259-2282`。

---

## 5. 备料席（prep；镜像 prep2 :3107）

| 要素 | 现状 | 锚 |
|---|---|---|
| **入口** | `workers-wall-merge.outputs.prep_should_run == 'true'`（I1：读墙 completed_pids）；validator never merges | `team.yml:936`（job 头）、`:944`（timeout 20m） |
| **出口** | 候选分支 `team/issue-N/candidate-R`（merge worker 分支）；evidence.tar.gz（manifest sha256 权威）；备料报告评论；**补卷器**（worker_salvage.py M2） | `team.yml:1223-1226`（salvage_packs 接线） |
| **工具面** | 纯脚本 job（无 droid 会话）；git merge/ls-remote；全量 pytest（600s 超时）；卡 checks 复跑（300s 超时） | `team.yml:1223` 区段 |
| **写目标** | 候选分支 push；issues 评论（母单＋计划单）；墙 patch；补卷器机器写死亡工序缺失的 evidence 件 | `team.yml:1321`（报告步 GH_TOKEN=github.token） |
| **凭证** | GH_TOKEN=github.token（报告步）；**无 droid、无 BYOM** | `team.yml:1321` |

**补卷器守卫四条件（机器判定 fail-closed）**：merged true ＋ F-1 clean ＋ prep 复跑 checks 全绿且 marker 按内容判红 ＋ 会话异常终止（wall_killed／非零 droid 退出码／真 stream_tail_marker）。锚：`scripts/team/worker_salvage.py:13`（「The guard is machine-judged and fail-closed; ALL of:」）、`:14-15 区间`（四条件逐条 docstring）。注意规格明文：补卷覆盖面 ≠ 中性归因覆盖面——归责只按 wall_killed 分支（§10-①关联）。

**prep2 差异点**：`team.yml:3107`（job 头）、`:3114`（timeout 20m）；补卷接线 `:3453-3462`。

---

## 6. 装配席（assemble）

| 要素 | 现状 | 锚 |
|---|---|---|
| **入口** | always()（lead 非 skipped 且非 duplicate） | `team.yml:4389`（job 头）、`:4396`（timeout 10m） |
| **出口** | 最终状态卡评论（--wall-patch final_status_card）；PR 尝试（pass 时）；子单/计划单关闭；chain_facts 收口（assemble_chain_facts.py） | `team.yml:4636`（assemble_chain_facts.py）、`:4599`（板面权威审计镜像声明行） |
| **工具面** | **无 droid 会话**；纯脚本；pick_verdict_from_wall.py（墙权威 pick，fail-closed）；project_state_write.py（PAT 写板） | `team.yml:4420`（pick_verdict_from_wall）、`:4441`（project_state_write） |
| **写目标** | **全链最强 GitHub 写面**：Projects #33 Status 字段（PAT）；PR create（github.token）；issue close/comment | `team.yml:4431`（PROJECTS_STATE_PAT）、`:4448`/`:4659`（GH_TOKEN=github.token） |
| **凭证** | PROJECTS_STATE_PAT（**全链唯一使用点**）＋GH_TOKEN=github.token | `team.yml:4431` |

**专有现状（图外件，F3 清零对象）**：①板面终态无一致性机制——关单后 Projects 内建 Item closed 自动化可把 Status 翻回「施工中」，repo 侧无写点可拦（§10-③）；②human_stop 已上墙（schema `:33`）但不被 assemble 消费提前停（§9 风险 13）。

---

## 7. 写板席（recorder——现状无独立 job，职能承载点）

| 要素 | 现状 | 锚 |
|---|---|---|
| **入口** | 两个承载点：①validate 席 prompt 纪律（会话内逐件落盘 verdict-partial.json）；②prep 补卷器机器兜底（死亡工序的 evidence 件由机器补写，标记 salvaged_from_machine） | `team.yml:1515`（validator prompt 单源）、`:1223-1226`（补卷器接线） |
| **出口** | verdict-partial.json→verdict-droid.json/md→verdict.json/md（墙 validation 切片经 adopt 采认） | `team.yml:1721`（run_adopt_step） |
| **工具面** | 承载点①：validator 会话工具面（无 GitHub 写权）；承载点②：纯脚本 | `team.yml:1502-1503`（validator 置空 env） |
| **写目标** | verdict 系列文件与墙切片；补卷器只补缺失件、不碰 worker 已写件（evidence immutability） | `scripts/team/worker_salvage.py:1-45`（docstring 产品纪律） |
| **凭证** | 承载点②无 droid 无 BYOM；承载点①同 validator（无 GitHub 令牌） | `team.yml:1463`/`:1501` |

**recorder 纪律现状定性**：prompt 文字无运行时效力（P-2 口径）；per-run 无 recorder 调用数墙字段、无报警——「必落字段与约定首步静默缺席」无人知晓（§10-④ 四问题④）。设计稿把 recorder 立为独立席位，是对这一现状的结构化收编。

---

## 8. 零号门（env-check，非席位）

| 要素 | 现状 | 锚 |
|---|---|---|
| 入口 | 同一 issue 评论触发；inputs: issue_number＋project_number=33 | `team.yml:37`、`env-check.yml:64-72`（job 头与 outputs） |
| 出口 | L0 墙 foreman-run.json（env_check_wall.py 写 env 切片）＋issue 体检评论 | `env-check.yml:64-72` |
| 工具面 | gh api / gh issue view / gh project view / yq；无 droid | `env-check.yml:82-86` |
| 写目标 | issue 评论；墙 artifact `foreman-run-{run_id}` | 同上 |
| 凭证 | github.token（contents:read, issues:write, actions:read）；**五 secrets 全部进入本 job 环境**（S_FACTORY_API_KEY/S_WORKER_CI_KEY/S_GW_TOKEN_KNOWN/S_GO_GITHUB_RUN_TOKEN/S_PROJECTS_STATE_PAT） | `env-check.yml:82-86`（五 secrets 注入行） |

---

## 9. 跨席现状事实（墙本体）

1. **墙只记结局不记授权**：`schemas/foreman-run.v1.schema.json` 记录结局（session_outcome 枚举 `:65`、session_outcome_by_pid `:146-150`、droid_exit_code_by_pid `:153`、stream_tail_marker_by_pid `:157`、human_stop `:33`），**无任何席位能力面字段**（可用工具/可写目标/令牌 scope）——「组件手握无授权能力」在 schema 层不可表达、不可执法。锚：`schemas/foreman-run.v1.schema.json:146-157`。
2. **59 轮四问题全部在「零逃逸」已宣称判据集（I1-I8）之外**——机制解释见 §10。
3. **版本口径漂移**：team.yml:7 标 v2.7.0；README 交付段标 v2.9/v2.10（README 段落随版本演化漂移，本件不锚行号，以 team.yml:7 为锚定对照）。
4. **工人预算账面化**：墙 budgets.roles.worker.droid_wall_sec=900（`foreman_run_lib.py:53-54`）不接线；执行预算硬编码在裸跑命令里（team.yml:599/:2784）；budgets lint 明文豁免该形态（`lint_workflow_budgets.py:43-51`）。
5. **PAT 只在两处**：assemble 写板（team.yml:4431）与 env-check 探板（env-check.yml:86）；与会话凭证（BYOM 三件＋FACTORY_API_KEY）已分离，但会话凭证在 8 个 droid 步重复展开无席位差异（lead :120/:157、worker :531/:568、validate :1463/:1501、replan :2178/:2209、worker2 :2725/:2757、validate2 :3705/:3738、revalidate2 :4115/:4147、revalidate :1883/:1916）。

---

## 10. 59 轮四问题机制级证据指针

> 59 轮事件原始记录不在 repo docs（证据链止于第 58 轮）；以下为四问题的**机制级仓内证据**。设计稿 §验收线（F4）的 59 轮回归样本以本节为证据底座。

### ① replan 虚构「F-1 检查拒绝」死因

- 机制根源（脚本内置推断，非机器记录）：分支缺席→推定 F-1 拒绝的文案写死在 replan 步 heredoc（Round-53 fix）；F-1 拒绝只会在 worker job 日志留一行，该日志从不进 replan 输入面。锚：`team.yml:2259-2282`（推断注释起于 `:2259`，F-1 文案赋值落 `:2278-2279`，else 分支 `:2282`）。
- 测试把该推断钉成正确行为（逐字断言 prompt 必含该文案）：`tests/test_replan_context_and_skipped_outcome_r53c.py:190-205`（test_replan_prompt_names_absent_branch_as_real_cause：`:198-202` 逐字行构造、`:205` count==1 断言）。
- 归责缺陷立号：`docs/第58轮-D单追认口径与replan归责缺陷立号.md` §二（「硬编码归责预设『缺件归该工序补齐』对一切缺件形态输出工人归责措辞」）。
- 关联：归责分支只认 wall_killed，补卷接纳的 exit-1 自崩族仍输出工人归责措辞——`scripts/team/worker_salvage.py` docstring（守卫子句 4 明示 exit-1/137 族被 classify 保留 ok，但补卷接纳）。

### ② 900s 进程墙对工具长挂不执法（执法与会话同体）

- 执法体形态：`team.yml:599`（一轮）/`:2784`（二轮）——GNU timeout 外墙，无回合预算/收束/续作。上游特性登记三裁定理由：`docs/回合熔断上游特性需求登记-droidCLI.md`（「droid CLI 无回合预算接口／外层早杀对工件保护更差／被杀即终」）。
- 不执法实证（45B）：孤儿子进程持管道使 step 活到 job 墙——TERM/KILL 与 runner 取消两套机制都未及时终结 step，实测墙钟 1800s vs 900s 名义墙。锚：仓外工作目录件 `adversarial/report-review/audit-numeric.md`（不在 repo 树内，佐证性质）。
- 关联：工人 verify 步 subprocess 无超时（team.yml:700 区段 verify 面）；prep 面已加步级超时（v2.6.4）。
- 结构对照：引擎侧已有体外执法形制可抄——哨兵先行→SIGTERM 组→宽限→SIGKILL 组（`form-basis.md §10 补遗 b`），执法通道不依赖被管进程配合。

### ③ 板面 Status 图外写入口（Item closed 自动化翻板）

- 专档三单实测：写板「已验收」→人工关单→1 秒后 Status 被翻回「施工中」，演员 `github-project-automation`（#761/#763/#764 同构）。锚：`docs/板面关单翻板-最小操作指引.md`。
- 结论原文：翻板不是流水线代码造成的，repo 内无可拦截、可修正的写入点；修法在板侧（Disable 或改终态选项）。同锚。
- 仓内唯一板面写点：assemble project_state_write.py（PAT）。锚：`team.yml:4431`（PAT 注入）、`:4441`（调用行）。
- PAT 时间线演员定性（第 50 轮审计）：`docs/W-14-写板活验通过判据-修订.md`。

### ④ recorder 必落字段与约定首步静默缺席

- 生产首验服从率：4 会话中 2 个调用了 recorder，逐件落盘服从率 0/4（B/D 均最后回合批量落盘）；墙杀场景回收 0/2。锚：`docs/V-3-closeout-收档报告.md` §一（Opus 终审原文）。
- 工人席对应口径（58-D）：13 次工具调用零次以 handoffs/status 为目标。锚：`docs/第58轮-死亡账分型登记-58D归第1类.md`；死亡链机器侧重建：`scripts/team/worker_salvage.py:4-9` docstring（hslconv worker 死于 900s 墙前未写 evidence 件）。
- V-3 门仅证明受控会话可达标，生产 per-run 无报警：同 `docs/V-3-closeout-收档报告.md`（V-3 门重跑节）。
- 关联：墙上无 recorder 调用数字段可报警——schema 层缺口见 §9.1。

---

## 11. 根治 1+2+4 现状（已批并入失败规范格式的既有层）

> 来源：`docs/R58D-收尾决策留痕-NC6与遗留决策点.md` §一、`docs/回合熔断上游特性需求登记-droidCLI.md` 结论行。批准范围＝四层根治中的 1+2+4 层加收尾留痕；第 3 层（回合预算/安全收束/续作）待上游能力再立项。

| 层 | 现状载体 | 锚 |
|---|---|---|
| 第 1 层（M2）补卷守卫/补卷器 | prep 补卷器：墙杀死工序的证据由机器补齐并标记 salvaged_from_machine；守卫四条件机器判定 fail-closed | `scripts/team/worker_salvage.py:13-15`（docstring） |
| 第 2 层（M3）模板单源＋守卫 | worker prompt 单源模板增量落盘引导＋里程碑序措辞；按 P-2 口径预期封顶（措辞无运行时效力），价值是给补卷器更丰富中间状态 | `scripts/team/worker_prompt_template.py`（接线 `team.yml:599` 前置 prompt 组装面） |
| 第 4 层（M1）死亡上墙＋归责根治 | worker-delta 结构化结局上墙＋replan 输入面死因注入＋归责模板分支化；三字段确定性分类 session_outcome/droid_exit_code/stream_tail_marker | `team.yml:836`（write_worker_delta）、`:885`（merge_worker_deltas）、`schemas/foreman-run.v1.schema.json:146-157` |

**明文口径**：补卷覆盖面 ≠ 中性归因覆盖面（`scripts/team/worker_salvage.py` docstring）——引用本表时不得假设「补了卷 ⟹ 归因已中性化」。

---

## 12. 五 lint 执法面现状（设计稿论证「无一覆盖能力授权」的对照基座）

| lint | 执法不变量 | 锚 |
|---|---|---|
| lint_workflow_foreman.py | 禁 legacy replan 门/静态 fail_text/状态代偿文案/\|\| true/init_wall/pick --chain-result；prep 必须读 wall-merge outputs；墙/delta 下载禁 continue-on-error；assemble 收口必须 --wall-patch final_status_card；每个 post_comment_hard 步必须设 GH_TOKEN | `scripts/team/lint_workflow_foreman.py` |
| lint_workflow_wall_exits.py | 每链席 always() 记墙退出；merge job 接纳上游 cancelled | `scripts/team/lint_workflow_wall_exits.py` |
| lint_gh_project_parse.py | gh project JSON 必须过解析层 | `scripts/team/lint_gh_project_parse.py` |
| lint_workflow_budgets.py | 禁 lead/validator/replan 裸 droid exec；**worker/900s 豁免**；三步必须 run_droid_session＋FOREMAN_RUN_PATCH=1；adopt 步必须 run_adopt_step.py | `scripts/team/lint_workflow_budgets.py:16-18`/`:43-51` |
| lint_workflow_needs.py | needs 悬空引用 | `scripts/team/lint_workflow_needs.py` |

**结论（现状一句话定位）**：五 lint＋既有契约测试无一覆盖「席位能力授权／死因佐证／板面终态一致性／recorder 纪律」四类——现行墙是「产物与采认语义墙」，59 轮四问题全部落在其未覆盖的席位能力与叙事授权面。设计稿 v3.0 的对象即此缺口。

---

## 附：席位锚索引（后续 feature 引用现状行号的一级入口）

| 席位 | job 行 | 裸跑/包装 | 预算锚 | 凭证锚 |
|---|---|---|---|---|
| env-check | team.yml:37 | 无 droid | — | env-check.yml:82-86 |
| lead | team.yml:52 | 包装 :203 | foreman_run_lib.py:37-40（600） | :120/:157/:79/:241 |
| worker | team.yml:503 | **裸跑 :599** | 账面 foreman_run_lib.py:53-54（900，不接线） | :531/:568/:710 |
| workers-wall-merge | team.yml:851 | 纯脚本 | — | 无 secret |
| prep | team.yml:936 | 纯脚本 | 步级 600s/300s（:1223 区段） | :1321 |
| validate | team.yml:1382 | 包装 :1534 | foreman_run_lib.py:42-45（480/120） | :1463/:1501（零 GH 权 :1390-1391/:1502-1503） |
| revalidate | team.yml:1779 | 包装 :1949 | 同 validate | :1883/:1916/:1787-1788 |
| replan | team.yml:2141 | 包装 :2405 | foreman_run_lib.py:48-50（480） | :2178/:2209（会话零 token :2210-2211；落单 :2423） |
| worker2 | team.yml:2697 | **裸跑 :2784** | 同 worker（账面） | :2725/:2757/:2895 |
| validate2 | team.yml:3618 | 包装 :3771 | 同 validate | :3705/:3738/:3626-3627/:3739-3740 |
| revalidate2 | team.yml:4010 | 包装 :4180 | 同 validate | :4115/:4147/:4018-4019/:4148-4149 |
| assemble | team.yml:4389 | 纯脚本 | timeout :4396（10m） | :4431（PAT 唯一点）/:4448/:4659 |
| recorder（无独立 job） | 承载点 :1515 与 :1223-1226 | — | — | 同 validator/无 |

> 行号随 team.yml 演化可能漂移；**F2/F3/F4/F5 引用现状一律以本件为准**，本件未覆盖的新锚点须实读核实后先补入本件再引用。
