# 批 B / B1（W-11）诊断报告 — validate `chain.validate` 死亡未落账

> 基线：`main` @ `84ce898`（含批 A）。**本文件仅诊断，不含修复。**
> 正本任务书：`round50-repair-orders.md`「批 B」节（外部）

## 1. 事实陈述（49 轮 C/D 观测）

- validate job 内已接线 `wall_sync_job.py --job validate`（`team.yml`「Derive validate job conclusion (W4)」步）。
- 活跑/工件中存世墙 `foreman-run.json` 上，`validation` 切片（`adoption_status`、`job_conclusion_derived`、`budgets.session_outcome` 等）**往往已写入**。
- 同期 `chain.validate` 仍停在 `init_wall` 初始态：`result: "unknown"`、`started: false`。
- 结论：**validator 在会话启动前死亡或超时采认失败时，链席位未与实情对齐** — 不是「无 wall_sync 步」，而是 **wall_sync 未执行或未生效**。

## 2. 同构复现（本地，零 workflow 补丁）

运行：

```bash
PYTHONPATH=scripts/team python3 scripts/team/diagnose_w11_validate_chain_sync.py
PYTHONPATH=scripts/team python3 scripts/team/diagnose_w11_validate_chain_sync.py --json
```

脚本模拟 validate 尾步 shell：**`set -eo pipefail` + 先 `compute_validate_conclusion` 再 `wall_sync_job`**（与 `team.yml` L1586–1594 同序）。

| 场景 | 采认 | `job_conclusion_derived` | `chain.validate.result` | `wall_sync` 是否执行 |
|------|------|--------------------------|-------------------------|----------------------|
| 会话启动前死亡（`droid_exit=None`，无 stream/草稿） | `failed` / `missing_output` | `failure`（derive 已 `save_wall`） | **`unknown`** | **否** |
| 会话超时（`droid_exit=124`） | `failed` / `draft_timeout` | `failure` | **`unknown`** | **否** |

两场景 shell 尾步 **exit code 均为 1**（derive 有意在非绿采认时返回 1），第二行 `wall_sync_job` **被 bash 截断**。

## 3. 机制定因（主因，可 lint 对位）

### 3.1 步序 + Actions 默认 `set -e`（主因）

`team.yml` validate / validate2 的 W4 步将 **derive 与 chain 写账捆绑在同一段 `run:`**：

```1586:1594:.github/workflows/team.yml
      - name: Derive validate job conclusion (W4)
        id: validate_conclusion
        if: always()
        run: |
          PYTHONPATH=scripts/team python3 scripts/team/compute_validate_conclusion.py \
            --wall foreman-run.json --github-output "$GITHUB_OUTPUT"
          PYTHONPATH=scripts/team python3 scripts/team/wall_sync_job.py \
            --job validate --result "$(python3 -c "import json;print(json.load(open('foreman-run.json'))['validation'].get('job_conclusion_derived','failure'))")" \
            --produced "$(python3 -c "import json;a=json.load(open('foreman-run.json'))['artifacts'];k=[x for x in a if x.startswith('team-verdict')][0];print('true' if a[k]['complete'] else 'false')")"
```

`compute_validate_conclusion.py` 在采认失败或 verdict artifact 不完整时 **仍持久化** `validation.job_conclusion_derived`，但 **以退出码 1 结束**（W6 机器门）：

```69:71:scripts/team/compute_validate_conclusion.py
    if val.get("adoption_status") == "failed" or not complete:
        return 1
    return 0
```

GitHub Actions `run:` 默认 **`bash -e`**：derive 返回 1 → **同一步内后续命令不执行** → `wall_sync_job` 从未调用 → `chain.validate` 保持 `unknown`。

对比：**lead / prep / worker merge** 的 `wall_sync` 置于独立 `if: always()` 步，或前置命令不非零退出；**lint**（`lint_workflow_wall_exits.py`）只检查 `if: always()` 存在，**不检查** derive 非零是否阻断同壳内 wall_sync。

validate2（L3196–3204）**同构**，故 round2 亦存在相同链席位空洞。

### 3.2 候选面查证（非主因 / 已排除或次要）

| 入口 | 查证结果 |
|------|----------|
| **wall_sync 门控** | W4 步 `if: always()` 满足；死亡路径下 **derive 步仍会启动**，失败点在步内 `-e`，非 `if:` 跳过。 |
| **墙文件 job 间传递** | adopt 步 `if: always()` 在 foreman-run 缺失时从 `wall-in` 复制（L1562–1568）；死亡前 droid 步失败时 **validation 切片可在 adopt 后存在**。与「chain 未写」并存，符合步内截断而非「无墙文件」。 |
| **失败步后步序** | 「Fail validate job when adoption failed (W6)」为 **独立步**（L1622–1625），再跑 derive；**不补写** `chain.validate`。upload foreman-run（L1614–1620）`always()` 可上传 **缺 chain 写账** 的墙，固化 49 轮工件形态。 |

### 3.3 会话启动前死亡路径（与超时共用尾步）

- droid 步 `if: steps.pre.outputs.judgeable != '[]'`；启动前失败（无 `verdict-droid.json`、`droid-exit` 缺省 -1）→ adopt 记 `missing_output` / `merge_skipped`（`adopt_verdict.py` + W-12 单测）。
- `run_droid_session` 若在写墙前失败，job 根目录可能无 `foreman-run.json`；adopt 从 `wall-in` 恢复 — **不阻止** validation 切片更新。
- **链席位漏洞与 droid 是否 patch 墙无关**，仅取决于 W4 壳内 derive→sync 是否连跑。

## 4. 与批 A / lint 的关系

- 批 A（W-10/W-12/W-13）已修 PYTHONPATH、droid stream 上传、adopt 不误报 session ok；**未改** validate W4 步序。
- `lint_workflow_wall_exits.py` 对 validate 仅要求 **Upload foreman-run wall** 带 `always()`，**不要求** `wall_sync` 与 derive 分步 — 故 CI 绿灯不能捕获 W-11。

## 5. 修复方向（待你确认后再开修复 PR，此处不施工）

建议验收约束（来自任务书）：

1. **会话启动前死亡**、**会话超时** 两场景：`chain.validate.result` 与 `JOB_STATUS`/派生结论一致（`failure`），`chain_facts.summary_code` 为 `failed`，schema 合法。
2. PR 说明附两段诊断输出（本脚本 `--json` 的 before 快照 + 修复后 after）。

候选修法（供批准时选用，**本 PR 不实施**）：

- 将 `wall_sync_job --job validate|validate2` 拆为 **独立 `if: always()` 步**，且 **derive 非零不得阻断 sync**（`set +e` 或 sync 移入 Python 单入口）。
- 可选：收紧 lint，禁止 validate W4 步内「可失败命令紧邻 wall_sync」。
- `compute_validate_conclusion` 返回 1 的机器门语义保留在 **后续 W6 步**，不与 chain 写账互斥。

## 6. 本轮交付物

- 本文档
- `scripts/team/diagnose_w11_validate_chain_sync.py` — 可重复试跑

**未改动**：`foreman_mode`、会话预算 600s、validate 业务逻辑；**未开** B2 / 小件 PR。