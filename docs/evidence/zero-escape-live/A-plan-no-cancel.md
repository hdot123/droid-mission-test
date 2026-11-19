# I8 场景 A — 方法变更（禁止 cancel）

## 编排（已合 main，#574/#578）

- **删除** scene A 的 `gh run cancel` 与 adopt 轮询 cancel。
- **改为** `gh run watch "$RUN_ID" --exit-status || true`，让 validate 内 **Adopt / assert / Upload foreman-run** 有机会跑完。

## 活验路径（计划）

1. 人为 **droid timeout（124）** 或 **缺草稿**，使 `adopt_verdict.py` 自然写入：
   - `validation.adoption_status=failed`
   - `human_stop=true`
   - `artifacts.team-verdict-*.complete=false`
2. validate job **红**；`replan_gate.should_replan` 不为 true。

## 禁止

- 不得再用 **cancel 打断 Adopt**（[44473343701](https://github.com/hdot123/droid-mission-test/actions/runs/44473343701) 已证：墙上无采认字段）。

## 阻塞

- 自 #572 起 orchestrator **resolve-scene 秒败**（见 `44476313896-orchestrator-D-blocked.md`），**尚无** #553 后、无 cancel 的 A 全链 run。

## 若自然失败仍无墙字段

- 归档为 **墙实现缺陷**（不在本轮改 `team.yml` 墙逻辑）；参考 [44472075472](https://github.com/hdot123/droid-mission-test/actions/runs/44472075472)（`foreman-run missing before adopt` / validator failure）。