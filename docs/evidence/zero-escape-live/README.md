# I8 活验归档（P3）

**合入 SHA（墙）**：`96051ba`（PR [#508](https://github.com/hdot123/droid-mission-test/pull/508)）

**声明**：**A/D 未达标**；**不得**宣称「零逃逸 / 硬性 API 墙」（P4 对抗审未做）。

| 场景 | 达标 | Team / 夹具 run | 归档 |
|---|---|---|---|
| **A** 采认失败 | **否** | [44469188184](https://github.com/hdot123/droid-mission-test/actions/runs/44469188184) | [44469188184-A.md](./44469188184-A.md) |
| **B** 评论硬失败 | **是** | [44468619417](https://github.com/hdot123/droid-mission-test/actions/runs/44468619417) | [44468619417-B.md](./44468619417-B.md) |
| **C** PAT 缺失 | **是**（夹具） | [44465372141](https://github.com/hdot123/droid-mission-test/actions/runs/44465372141) | [44465372141-C.md](./44465372141-C.md) |
| **C-team** L0 | **是** | [44468989446](https://github.com/hdot123/droid-mission-test/actions/runs/44468989446) | [44468989446-C-team.md](./44468989446-C-team.md) |
| **D** 半套 artifact | **否** | [44470162674](https://github.com/hdot123/droid-mission-test/actions/runs/44470162674) | [44470162674-D.md](./44470162674-D.md) |

## 历史阻塞（已解除 / 仍影响 A·D）

- ✅ **PAT 触发**：`PROJECTS_STATE_PAT` 已配置 → orchestrator 可发 `@team-droid`（[#538](https://github.com/hdot123/droid-mission-test/pull/538) 起）。
- ⚠️ **A/D 全链**：v2.7 lead **Post plan dispatch** 调用 `gh` 时 job 未设 `GH_TOKEN` → 活验在 lead 即断（见 A/D 归档）。**非** PAT 问题；在用户「勿改墙」约束下待产品侧修。

## 触发（main）

[triggers/README.md](./triggers/README.md)

**禁止**在战役工单 #407–#410 上 `@team-droid`。

## 过期占位文档

- [44467648427-B-blocked.md](./44467648427-B-blocked.md)、[A-D-C-team-blocked.md](./A-D-C-team-blocked.md) — PAT 阻塞期的记录，已被上表替代。