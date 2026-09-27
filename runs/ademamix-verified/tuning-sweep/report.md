# AutoResearch Lite 实验报告

- 任务：tuning sweep for the AdEMAMix comparison (learning rate x warmup length)
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：AdEMAMix adds a slow EMA mixed in with a growing coefficient, so it has one more hyper-parameter than AdamW (the length of the alpha/beta3 warmup) and its learning rate may need retuning. Giving every arm the same grid is what keeps the later comparison from measuring tuning luck.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`4d4b14197c75bd47259da7691ea2f96b7d453e9ff8cd19c75c26e45b80a90f48`

## 最优方案

`ademamix_w0_lr0.8`：主指标 `test_loss` = **0.122023**，测试准确率 **93.50%**，测试损失 `0.1220232`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix_w0_lr0.8 | 93.50% | 0.1220232 | 97 | 未达标 | 97.409 |
| ademamix_w45_lr0.4 | 93.50% | 0.12241913 | 120 | 未达标 | 122.2 |
| baseline | 93.50% | 0.12255737 | 72 | 未达标 | 69.826 |
| adamw_lr0.8 | 93.50% | 0.12255737 | 72 | 未达标 | 72.309 |
| ademamix_w0_lr0.4 | 93.50% | 0.12317874 | 120 | 未达标 | 121.143 |
| sgd_momentum_lr0.8 | 93.50% | 0.123455 | 120 | 未达标 | 131.176 |
| adamw_lr0.4 | 93.50% | 0.12346246 | 120 | 未达标 | 122.669 |
| ademamix_w120_lr0.2 | 93.50% | 0.12415636 | 120 | 未达标 | 122.016 |
| ademamix_w120_lr0.4 | 93.50% | 0.1254779 | 120 | 未达标 | 125.508 |
| ademamix_w45_lr0.2 | 93.50% | 0.12716626 | 120 | 未达标 | 122.358 |
| ademamix_w45_lr0.8 | 93.50% | 0.12926405 | 120 | 未达标 | 123.279 |
| sgd_momentum_lr0.4 | 93.00% | 0.12994884 | 120 | 未达标 | 140.552 |
| ademamix_w0_lr0.2 | 93.00% | 0.1321513 | 120 | 未达标 | 123.801 |
| adamw_lr0.2 | 93.00% | 0.132963 | 120 | 未达标 | 122.316 |
| ademamix_w120_lr0.8 | 93.50% | 0.14436725 | 120 | 未达标 | 120.262 |
| sgd_momentum_lr0.2 | 94.00% | 0.14444219 | 120 | 未达标 | 126.469 |
| ademamix_w120_lr0.1 | 93.50% | 0.14631901 | 120 | 未达标 | 118.349 |
| ademamix_w45_lr0.1 | 93.50% | 0.15190072 | 120 | 未达标 | 120.999 |
| ademamix_w0_lr0.1 | 93.50% | 0.15840283 | 120 | 未达标 | 122.975 |
| adamw_lr0.1 | 93.50% | 0.15982558 | 120 | 未达标 | 119.717 |
| sgd_momentum_lr0.1 | 94.00% | 0.16995618 | 120 | 未达标 | 121.129 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
