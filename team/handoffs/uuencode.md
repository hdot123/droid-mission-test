# Handoff: uuencode 经典编解码组件（sub-issue #941）

## What was requested

Work order #929, process card `uuencode` (D 单三件之一，另两件 radixsort／hslconv 不归本单)。
只新增两个文件：`uuencode.py` 与 `tests/test_uuencode.py`；只用标准库；不改任何存量文件；
逐字实现经典 uuencode 编解码，验收要点全覆盖（详见卡内 SPEC／ACCEPTANCE）。

## What I did

- `uuencode.py`
  - `uuencode(data: bytes) -> str`：45 字节分行；行首长度字符 = 本行字节数 + 32（整行 "M"）；
    每 3 字节转 4 个 6 位组字符（+32），**零值写反引号**；全部行后以单反引号行收尾；
    行间 "\n" 连接、无尾随换行；不带 begin/end 头尾行；空输入返回单个反引号。
    非 bytes 入参抛 `TypeError`。
  - `uudecode(text: str) -> bytes`：按长度字符逐行还原（反引号解码为零值，空格同样容忍为零值）；
    空文本、缺收尾行、正文长度与长度字符不合、收尾行不在末行、含空行 → `ValueError`；
    非 str 入参抛 `TypeError`。
- `tests/test_uuencode.py`：覆盖全部验收要点——`b"Cat"` 精确向量、空输入、零值反引号向量
  （并断言编码输出不含空格）、roundtrip、46 字节三行且首行首字符 "M"、解码容忍空格、
  随机 0–100 长度性质测试（roundtrip + 与 `int.from_bytes` 24 位提取的独立参照实现逐字一致）、
  `uuencode`/`uudecode` 的 TypeError、七类 ValueError（含尾随换行、正文空行、收尾行不在末行）。

## What I did not do

- 未触碰 `radixsort.py`、`hslconv.py` 或任何存量文件（未改、未删）。
- 未提交、未推送（交由工作流）。
- 未生成或处理 `verdict.json`／`verdict.md`（跑全量测试后若出现属流水线副产物，已确认当前不存在）。

## Checks run and results

1. `python3 -m pytest tests/test_uuencode.py -q` → **10 passed**（首次跑曾因解码器未把反引号按零值处理而 1 failed，已修复：解码侧将 "`" 视作 0，再复跑通过）。
2. `python3 -m pytest tests/ -q` → **352 passed, 2 skipped**（退出码 0）。

## Notes for the validator

- 关键易错点：**编码侧零值必须写反引号**（写空格必挂——测试里有显式断言 `"\x00"*45` 编码结果不含空格）；解码侧才容忍空格。
- 45 字节整行长度字符是 "M"（45+32）；46 字节样例首行即 "M"。
- 收尾行必须恰好是最后一行；尾随 "\n" 会使 `split` 产生空行从而抛 ValueError（符合规格）。
- 参照实现使用 `int.from_bytes(..., "big")` 逐 24 位提取，与实现无共享代码路径。
