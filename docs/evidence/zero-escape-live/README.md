# I8 活验归档（P3）

**合入 SHA**：`96051ba13658c895cadf306a6831f6286c3047cb`（PR [#508](https://github.com/hdot123/droid-mission-test/pull/508) → `main`）

**基础设施**：orchestrator（[#509](https://github.com/hdot123/droid-mission-test/pull/509)）、`C-fixture`、push 触发器、建单 `github.token` + 触发 PAT 分层（[#530](https://github.com/hdot123/droid-mission-test/pull/530)、[#533](https://github.com/hdot123/droid-mission-test/pull/533)）。

**声明**：四类活验 **未全部达标**；**不得**对外宣称「零逃逸 / 硬性 API 墙」（P4 对抗审未做）。

| 场景 | 归档 | Team / 夹具 run | 达标 |
|---|---|---|---|
| **A** 采认失败 | [A-D-C-team-blocked.md](./A-D-C-team-blocked.md) | 未跑 | **否**（缺 GitHub PAT 触发） |
| **B** 评论硬失败 | [44467648427-B-blocked.md](./44467648427-B-blocked.md) | Orchestrator [44467648427](https://github.com/hdot123/droid-mission-test/actions/runs/44467648427)；**无** team run | **否** |
| **C** PAT 缺失 | [44465372141-C.md](./44465372141-C.md) | 夹具 [44465372141](https://github.com/hdot123/droid-mission-test/actions/runs/44465372141) | **是**（夹具等价；未删生产 `PROJECTS_STATE_PAT`） |
| **C-team** L0 | [A-D-C-team-blocked.md](./A-D-C-team-blocked.md) | 未跑 | **否** |
| **D** 半套 artifact | [A-D-C-team-blocked.md](./A-D-C-team-blocked.md) | 未跑 | **否** |

## 当前阻塞（B/A/D/C-team）

向 `team.yml` 发 `@team-droid` 需要 **GitHub PAT**（非 `GITHUB_TOKEN`、非 Factory `GO_GITHUB_RUN_TOKEN`）。仓库内 orchestrator 可见：

- `PROJECTS_STATE_PAT`：**空**
- `GO_GITHUB_RUN_TOKEN`：**401** on `gh api user`

**运维**：添加 Actions secret **`I8_TEAM_TRIGGER_PAT`**（推荐）或确保 `PROJECTS_STATE_PAT` 对 orchestrator 可见 → 再按顺序合并 `B.scene` → `C-team.scene` → `A.scene` → `D.scene`。

## 触发方式（main）

见 [triggers/README.md](./triggers/README.md)。

**禁止**在战役工单 #407–#410 及第 43–46 轮同类 issue 上 `@team-droid`。