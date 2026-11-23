name: Feature Request
description: 提议一个新能力（流水线阶段、契约字段、工具改进）
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: 要解决的问题
      description: 现状哪里不满足，缺少什么能力
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: 设想方案
      description: 涉及 wall 契约变更时，注明 schemas/foreman-run.v1.schema.json 的影响
    validations:
      required: true
