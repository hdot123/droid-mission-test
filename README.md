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

当前基线：314 passed, 2 skipped。
