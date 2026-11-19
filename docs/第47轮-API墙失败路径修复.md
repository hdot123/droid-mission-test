# 第 47 轮活验 · API 墙失败路径修复（W-1–W-4）

## 缺陷与根因（对照活验）

| 编号 | 现象 | 根因 | 修法 |
|------|------|------|------|
| **W-1** | A/D 在 assemble 写板：`issue #nnn not linked to project #33`（PAT 有权限但找不到 item） | `project_state_write.py` 第 41 行 `or`/`if` 优先级错误：`gh project item-list` 返回 **dict** 时 `items` 恒为 `[]` | 抽出 `parse_project_item_list()`，dict 读 `items` 数组 |
| **W-2** | 写板失败后 `save_wall` 抛 schema 错，收口字段一无所写 | 失败时写入 `project_state_enum: null`，schema 要求 **string** | 仅成功时写 `project_state_enum`；失败保留 `run_must_fail` + `project_state_error` |
| **W-3** | B 路 workers-wall-merge 等步可能因墙不合法中断 | `wall_sync_job.py` 把 GitHub `failure` 直抄进 `chain_facts.summary_code`，枚举只允许 `failed` 等 | `normalize_chain_job_result` + `chain_summary_code_for_result` 双词汇映射 |
| **W-4** | B 路工人会话超时/零输出，delta 仍为 `success` | 矩阵步默认 `RESULT=success`，只补 `cancelled` 与 checks marker，**未读 `job.status=failure`** | `write_worker_delta.py` 读取 `JOB_STATUS` 环境变量（workflow 已注入） |

C 路验收器 `draft_timeout` + fail-closed **未改动**，行为保持。

## 改动文件

- `scripts/team/foreman_run_lib.py` — 解析板 item、链结果归一化、summary_code 映射
- `scripts/team/project_state_write.py` — W-1、W-2
- `scripts/team/wall_sync_job.py` — W-3
- `scripts/team/write_worker_delta.py` — W-4
- `tests/test_foreman_wall_failure_paths.py` — 失败路径回归（非开心路径）
- 本文档

## 测试

```bash
cd /path/to/droid-mission-test
pip install -q -r requirements-dev.txt
pytest tests/test_foreman_wall_contract.py tests/test_foreman_wall_failure_paths.py -q
```

## 如何验证（运维 / 活验）

1. **单测**：上述 pytest 全绿；`test_foreman_wall_contract.py` 仍通过。
2. **写板（W-1/W-2）**：工单已挂 Projects #33 时，assemble 写板应能解析 item；写板失败时 `foreman-run.json` 仍有合法 `closeout`（无 null enum），assemble 因 `board_write.outcome == failure` 标红。
3. **同步（W-3）**：任意 job `failure` 汇入墙后，`chain.*.chain_facts.summary_code` 为 `failed`，`save_wall` 不因 schema 失败。
4. **工人账本（W-4）**：工人 job 红（含超时、无产出）且无误标 marker 时，`worker-delta.json` 的 `result` 为 `failure`，merge 后 `workers.any_failed` 为真。

## 证据索引（第 47 轮）

- A #630 — run `44532706766`，PR #651（assemble 写板）
- B #631 — run `44532754302`（工人超时 + 墙同步/账本）
- C #632 — run `44532812733`（fail-closed，对照）
- D #633 — run `44532866411`，PR #650（assemble 写板）