# I8 活验归档（P3）

**墙合入**：`96051ba`（#508） · **lead GH_TOKEN**：`997240f`（[#553](https://github.com/hdot123/droid-mission-test/pull/553)）

**声明**：活验 **A/B/C/C-team/D 均有达标归档**；**P4 未做 → 不得宣称零逃逸**。

**Billing（2026-11-19）**：曾阻塞 hosted runner（见 [44476313896-orchestrator-D-blocked.md](./44476313896-orchestrator-D-blocked.md)）；恢复后 orchestrator [44522049816](https://github.com/hdot123/droid-mission-test/actions/runs/44522049816) 已正常。编排 **watch 无 cancel**（#574/#578）。

| 场景 | 达标 | Team / 夹具 run | 归档 |
|---|---|---|---|
| **A** 采认失败 | **是** | [44526511233](https://github.com/hdot123/droid-mission-test/actions/runs/44526511233) | [44526511233-A.md](./44526511233-A.md) · 历史 [44473343701-A.md](./44473343701-A.md) |
| **B** 评论硬失败 | **是** | [44468619417](https://github.com/hdot123/droid-mission-test/actions/runs/44468619417) | [44468619417-B.md](./44468619417-B.md) |
| **C** PAT 缺失 | **是**（夹具） | [44465372141](https://github.com/hdot123/droid-mission-test/actions/runs/44465372141) | [44465372141-C.md](./44465372141-C.md) |
| **C-team** L0 | **是** | [44468989446](https://github.com/hdot123/droid-mission-test/actions/runs/44468989446) | [44468989446-C-team.md](./44468989446-C-team.md) |
| **D** 半套 artifact | **是** | [44525110357](https://github.com/hdot123/droid-mission-test/actions/runs/44525110357) | [44525110357-D.md](./44525110357-D.md) |

## 本次 A/D 重跑基础设施（非墙）

- [#554](https://github.com/hdot123/droid-mission-test/pull/554)：`PROJECTS_STATE_PAT` 用于 `gh run cancel`
- [#564](https://github.com/hdot123/droid-mission-test/pull/564) / [#571](https://github.com/hdot123/droid-mission-test/pull/571)：orchestrator run-pick 调整
- [#574](https://github.com/hdot123/droid-mission-test/pull/574) / [#578](https://github.com/hdot123/droid-mission-test/pull/578)：**A/D 无 cancel**，`gh run watch`
- [#599](https://github.com/hdot123/droid-mission-test/pull/599)：`[I8]*` 门 + `VALIDATOR_DROID_TIMEOUT_SECONDS`（validator 非墙注入）

历史尝试：`44469188184-A.md`、`44470162674-D.md` 为 #553 前记录，保留备查。

## 触发

[triggers/README.md](./triggers/README.md) · 禁止战役工单 #407–#410。