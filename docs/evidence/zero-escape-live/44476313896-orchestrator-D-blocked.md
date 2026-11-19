# I8 D 触发受阻 — orchestrator resolve-scene 秒败

| 字段 | 值 |
|---|---|
| Orchestrator | [44476313896](https://github.com/hdot123/droid-mission-test/actions/runs/44476313896) |
| 预期场景 | D（#579 `D.scene` only） |
| Team run | **未产生** |
| 达标 | **否**（全链未起跑） |

## 现象

- `resolve-scene`：`conclusion=failure`，**`runner_id=0`**，**steps 为空**（runner 未分配 / 作业未真正起跑）。
- 同模式自 [44475203577](https://github.com/hdot123/droid-mission-test/actions/runs/44475203577)（#572）起持续；对照末次正常 resolve：[44474201821](https://github.com/hdot123/droid-mission-test/actions/runs/44474201821)（#569）。

## 已做编排侧（main）

- [#574](https://github.com/hdot123/droid-mission-test/pull/574) / [#578](https://github.com/hdot123/droid-mission-test/pull/578)：**A/D 改为 `gh run watch`，去掉 `gh run cancel`**。
- [#571](https://github.com/hdot123/droid-mission-test/pull/571)：A/D `gh run list` 可取已完成 run。

## 仍待 D 活验

上一有效 team 尝试 [44474237836](https://github.com/hdot123/droid-mission-test/actions/runs/44474237836)：**env-check 即 failure**（见 `44474237836-D.md`）。

**未宣称零逃逸。**