# I8 活验归档（P3）

**合入 SHA**：`96051ba13658c895cadf306a6831f6286c3047cb`（PR [#508](https://github.com/hdot123/droid-mission-test/pull/508) → `main`）

**基础设施**：PR [#509](https://github.com/hdot123/droid-mission-test/pull/509)–[#522](https://github.com/hdot123/droid-mission-test/pull/522)（orchestrator、`C-fixture`、`push` 触发器、`GO_GITHUB_RUN_TOKEN` 修复）。

**声明**：未完成四类归档并通过独立对抗审（P4）前，不得对外宣称「零逃逸 / 硬性 API 墙」。

| 场景 | 归档文件 | Run / 状态 |
|---|---|---|
| A 采认失败 | （待补） | **进行中/阻塞**：合并 `A.scene` 触发 orchestrator；预计 30–90min 全链 |
| B 评论硬失败 | （待补） | **进行中**：`GO_GITHUB_RUN_TOKEN` 修复后 `B.scene` 重触发（见 [#523](https://github.com/hdot123/droid-mission-test/pull/523)） |
| C PAT 缺失 | [44465372141-C.md](./44465372141-C.md) | **达标（夹具等价）**：[run 44465372141](https://github.com/hdot123/droid-mission-test/actions/runs/44465372141)；team L0 补档见 `C-team.scene` |
| D 半套 artifact | （待补） | **待跑**：合并 `D.scene` 后归档 |

## 触发方式（main）

见 [triggers/README.md](./triggers/README.md)：向 `main` 合并对应 `*.scene` marker 即可（无需 `workflow_dispatch`）。

**禁止**在战役工单 #407–#410 及第 43–46 轮同类 issue 上 `@team-droid`。