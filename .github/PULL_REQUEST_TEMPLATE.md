## 变更说明

<!-- 这個 PR 改了什么、为什么 -->

## 验证

<!-- 勾选并粘贴本地验证输出 -->

- [ ] `pytest tests/ -q` 全绿（基线 187 passed, 2 skipped）
- [ ] 四个 lint 脚本通过（foreman / wall_exits / gh_project_parse / budgets）
- [ ] `ruff check .` 无错误
- [ ] `mypy` 无错误

## 契约影响

<!-- 若改动 wall 契约：schemas/foreman-run.v1.schema.json 与契约测试是否同步更新 -->

- [ ] 不涉及契约变更 / 已同步更新 schema 与测试
