# I8 场景 A / D / C-team — 未跑通（与 B 同一阻塞）

## 阻塞摘要

`team.yml` 仅由 **非 `github-actions` 身份** 的 `issue_comment`（含 `@team-droid`）触发。I8 orchestrator 依赖仓库 GitHub PAT secret；当前：

- `PROJECTS_STATE_PAT`：**未注入** orchestrator job
- `GO_GITHUB_RUN_TOKEN`：**非** GitHub PAT（`gh` → 401）
- Cloud Agent 本机 `gh`：**integration token 无法** `addComment`（GraphQL 403）

因此 **A、D、C-team** 尚未产生可归档的 `team.yml` run。

## 场景状态

| 场景 | Orchestrator | Team run | 归档 |
|---|---|---|---|
| **A** 采认失败 | 未触发（无 `A.scene` 合并） | 无 | 本文 |
| **D** 半套 artifact | 未触发（无 `D.scene` 合并） | 无 | 本文 |
| **C-team** PAT/L0 | 未触发 | 无 | 本文；**C 夹具**见 [44465372141-C.md](./44465372141-C.md) |

## 解除阻塞后顺序（计划）

1. 配置 `I8_TEAM_TRIGGER_PAT` 或可见的 `PROJECTS_STATE_PAT`
2. `B.scene` → `*-B.md`
3. `C-team.scene` → team L0 归档
4. `A.scene` → `D.scene`

**未**宣称零逃逸。