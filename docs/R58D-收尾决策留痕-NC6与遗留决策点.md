# R58-D 工人席落盘根治 · 收尾决策留痕（NC-6 CI 子集裁定 + 遗留决策点）

## 一、NC-6 编排裁定：foreman-wall-ci 十文件 CI 子集本 mission 不扩

**裁定：`.github/workflows/foreman-wall-ci.yml` 的十文件契约测试子集维持现状，本 mission 不加文件。**

理由（超出批准范围的 workflow 门清单变更）：批准的 mission 范围是四层根治中的 1+2+4 层（补卷器/模板单源+守卫/死亡上墙+归责根治）加收尾留痕；CI 子集的文件清单是 workflow 门结构变更，不属批准面。十文件子集现有的门语义（schema + 契约测试 + 五 lint）不动。

**全套件门覆盖全部新测试**：本 mission 全部新增测试（worker-delta 结局契约、归责分支、补卷守卫与产物、模板单源、r58 夹具、端到端重放）都在 `pytest tests/ -q` 全套件门内，五 lint（foreman / wall_exits / gh_project_parse / budgets / needs）全绿为验收门。

## 二、遗留决策点（留大哥裁决）

**CI 子集是否纳入归责/夹具/补卷三测试文件。** 本 mission 新增的三个测试文件不在 foreman-wall-ci 十文件子集内，CI 绿不覆盖它们的回归，只有全套件门（`pytest tests/ -q`）与本地手跑能发现：

| 文件 | 覆盖面 | 不进 CI 子集的风险窗口 |
|---|---|---|
| `tests/test_replan_death_context_attribution.py` | replan 输入面死因注入 + 四合并步归责模板分支（含 clean-subprocess 回放） | 归责措辞回退到工人归责、heredoc import 破坏不会让 CI 红 |
| `tests/test_worker_r58d_fixtures.py` | r58 夹具完整性 + sha256 对账 + 死亡形态钉子 | 夹具字节漂移/PROVENANCE 失真不会让 CI 红 |
| `tests/test_worker_salvage.py` | 补卷守卫正反例 + 产物字段 + manifest 标记 + 工作流 salvage 块重放 | 补卷守卫/fail-closed 回归不会让 CI 红 |
| `tests/test_worker_prompt_single_source.py` | 模板单源渲染（执行级）+ verify 步守卫形状 | 模板漂移 / verify 守卫守卫条件回退不会让 CI 红 |
| `tests/test_r58d_e2e_replay.py` | 死链/对照端到端重放（VAL-CROSS-001/002） | 端到端链回退不会让 CI 红 |

（后两文件为 M3 新增，晚于本表初稿；一并列入以保持表格完整。）

纳入方式（若大哥裁决扩）：把三个文件名追加进 foreman-wall-ci.yml 的 `pytest tests/...` 文件清单并过五 lint——属 workflow 门清单变更，需重新走批准。

**当前保护状况**：三个文件共 60+ 用例全部在全套件门内跑（本 mission 终验 533 passed + 2 skipped 全绿）；replan heredoc 的 CI 保真回放（clean-subprocess）与补卷守卫的工作流级重放已把「测试绿但 CI 破」的窗口本身钉成测试（r58 scrutiny round-1 的 import-path 缺陷类已有专项守卫）。

## 三、PROVENANCE 精度修正（user-testing/scrutiny 遗留，同件顺手）

本轮对 `tests/fixtures/worker-r58d/PROVENANCE.txt` 做三处精度修正（不改动 sha256 表、不动任何夹具字节，PROVENANCE 自身不在表内）：

1. **(a) Used by 补全真实消费测试**：由「只点名 test_worker_r58d_fixtures.py、其余笼统作 downstream features」改为逐一点名五个真实消费测试文件（test_worker_r58d_fixtures / test_fixture_manifest_hash_lifecycle / test_foreman_wall_worker_delta_outcome / test_replan_death_context_attribution / test_worker_salvage）并各注一行覆盖面。
2. **(b) synthetic 成员句限根级文件**：「the one synthetic member of this fixture root」改为「Among the root-level fixture files, worker-delta-wall-killed.json is the one synthetic member」，并指向 control-ok-missing/README.txt 的自带 SYNTHETIC 声明——消除「整棵树只有一个 synthetic 成员」的误读。
3. **(c) 标题括号与残留 verbatim 措辞改精确表述**：标题「(verbatim, read-only source)」改为「(read-only verbatim-attested source)」——「verbatim」降为对 sha256 表逐字节核对的「attested」限定；正文「byte-verbatim from that corpus」改为「byte-identical to its counterpart in that corpus」（表中确有一个 rebuild 成员，逐字 verbatim 全称命题为假）。全文残留「verbatim」仅 3 处（标题限定 + 两处否定性范围声明）。

钉子：`tests/test_worker_r58d_fixtures.py` 新增四用例（Used-by 五文件点名+存在性+引用核实、synthetic 句限定根级、verbatim 措辞三处白名单）。
