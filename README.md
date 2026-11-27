# droid-mission-test
Factory droid mission behavior test - validator workers in development missions. Created 2026-11-16 for testing only.

Released under the [MIT License](LICENSE).

## 领班制流水线（v2.8.0）

v2.8.0 起（PR #757），领班（lead）不再手写整份 team-plan.json：计划改为**分段唯一手写源＋机器拼装**——lead 只在 `team/lead-plan-segments/` 下写 `00-header.json` 与 `process-<id>.json` 分段卡，`team-plan.json` 由工作流 Stitch 步（`scripts/team/lead_plan_segments.py` 的 `stitch` / `assert-ready`）在 Validate 步读取前自动拼装生成。计划形态为三态磁盘真相：`none`（无可拼装分段）/ `partial`（盘上有分段但含残留）/ `complete`（header＋全部卡片干净）。原先「整份计划与分段逐字对账」的等价闸已随双写产物一并删除。

进程卡 id 派生规则：由模块名 stem 派生——小写化、下划线转连字符，须匹配 `^[a-z0-9][a-z0-9-]*$`，且 id 与文件名一致（`process-<id>.json`）。

## 预算族回合测量（M2）

`scripts/team/turn_metrics.py` 提供回合级预算测量（字符量 / 速率 / 首响延迟）：

```bash
PYTHONPATH=scripts/team python -m turn_metrics <流工件或目录>
```

输入为单个流工件（`.jsonl` / `.log`）或运行目录；目录输入会递归查找 `droid-stream-*-run-*` 工件，未知文件自动跳过。加 `--json` 输出完整报告。相关文档：[回合测量数据表 r44–r51](docs/预算族-回合测量数据表-r44-r51.md)、[预算族治理方案呈批件](docs/预算族治理方案-呈批件.md)（待批清单 P-1～P-8，批准后另单实施）。

## 验收协议根治（v2.9，PR #835–#844）

第 54 轮 validator 被 480s 墙杀（exit 124）后整单 human_stop 的死法，经 `adversarial/round54-root-cure/` 三份对抗报告收敛后根治。要点：

- **I-5 自动重验**：首次 `draft_timeout` 不再终局 human_stop——`adopt_verdict.py` 写 `replan_gate.should_revalidate=true`，触发 `team.yml` 的 revalidate / revalidate2 job（只重跑 validator 会话、复用已上传证据包、`EXPECTED_MANIFEST_SHA` 不变、`revalidate_run_started` 哨兵保证至多 1 次）；二次失败仍 human_stop（fail-closed 保持）。改动了 `compute_replan_gate.py`、`compute_validate_conclusion.py` 与 schema 的 replan_gate 切片。
- **I-6 盘上产物优先**：采认以盘上产物完整性为准、不以退出码为准——完整草稿在盘（即使 exit 124）正常采认；`verdict-partial.json` 全盖 judgeable＋manifest sha 通过＋`--final` 收口时，由 `salvage_assemble.py` 机器组装草稿走正常采认（pytest_exit / conflicts / 机器闸照常适用）。
- **recorder CLI**：`scripts/team/salvage_verdict.py` 逐件落盘（读一件→recorder 一件），支持 `--conflict`（可重复）与 `--final`（收口标记，seal 粘性——迟到的补记不解封）。
- **S-2 机器闸**：HARD RULE 不再依赖模型如实报告——`adopt_verdict.py` 的 `machine_gate_reds` 在采认汇合点机器判定：`packs/<id>/checks-exit.json` 非零退出码（exit 127 pytest 不可用例外）或 `checks-failed.marker` 按内容判定为红（非 0 check exit / status 非法 / 不可解析，仅缺件为绿），模型 pass 被翻转并标注 `machine_gate` 证据。
- **validator prompt 单源模板**：两轮 prompt 抽成 `scripts/team/validator_prompt_template.py`（team.yml 四个渲染位 export `REPO_ROOT` 引用）；prompt 声明 team/handoffs、team/status 为协议自产物非冲突，计数以 prep 产的 `evidence/check-summary.json`（每卡聚焦 check 计数）为唯一权威。
- **worker 预装依赖（U-10）**：worker / worker2 会话前预装 `requirements-dev.txt`（第 54 轮 12/12 worker 首测 `No module named pytest` 的环境根因）。
- **V-3 上线门**：prompt 变更须先用真实证据包跑真会话验证 recorder 触发面（判据：流中 tool_call 的 parameters 含 `salvage_verdict` 且 tool_result 成功）。2026-11-26 重跑过门：A=4 / C=3 次 recorder tool_call；门证据与收档见 `docs/evidence/v3-gate-rerun/` 与 `docs/V-3-closeout-收档报告.md`。

## 测试

```bash
pytest tests/ -q
python3 scripts/team/lint_workflow_foreman.py
python3 scripts/team/lint_workflow_wall_exits.py
python3 scripts/team/lint_gh_project_parse.py
python3 scripts/team/lint_workflow_budgets.py
python3 scripts/team/lint_workflow_needs.py
```

以上即 CI（foreman-wall contract workflow）在 push/PR 时运行的全部检查：契约测试子集＋五个 lint 脚本（foreman 接线、墙退出、Projects 解析、预算参数、needs 悬空引用）。

当前基线：342 passed, 2 skipped。
