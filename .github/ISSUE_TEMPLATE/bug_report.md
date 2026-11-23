name: Bug Report
description: 报告一个缺陷（测试失败、流水线异常、wall 契约破坏）
labels: ["bug"]
body:
  - type: textarea
    id: what-happened
    attributes:
      label: 发生了什么
      description: 附上报错输出 / pytest 失败摘录 / run 链接
      placeholder: |
        pytest tests/test_xxx.py 输出…
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: 预期行为
    validations:
      required: true
  - type: input
    id: repro
    attributes:
      label: 复现命令
      placeholder: pytest tests/test_xxx.py -q
    validations:
      required: true
