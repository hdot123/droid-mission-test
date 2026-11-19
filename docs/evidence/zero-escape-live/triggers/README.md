# I8 活验触发器（push）

Cloud Agent 无 `workflow_dispatch` / 建单权限时，向 `main` 合并下列 **空 marker 文件** 即可触发对应活验（`contents:write` 即可）：

| 文件 | 触发的 workflow |
|---|---|
| `B.scene` | orchestrator 场景 B（锁定工单 → 评论硬失败） |
| `C-team.scene` | orchestrator 场景 C（工单缺段 → team L0 硬失败） |
| `C-fixture.scene` | PAT 缺席 L0 夹具（不删生产 secret） |
| `A.scene` / `D.scene` | orchestrator 场景 A / D（完整 team 链） |

每次触发：在 `main` 上 **新增或修改** 对应 `.scene` 文件（内容可为空行 + 时间戳注释）。