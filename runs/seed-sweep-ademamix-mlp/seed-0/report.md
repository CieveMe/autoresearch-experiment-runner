# AutoResearch Lite 实验报告

- 任务：AdEMAMix on the two-layer MLP: speed versus final quality
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：The logistic head is almost convex and converges in tens of steps, which is the wrong regime for a second, slower moving average. On a two-layer tanh MLP the same comparison may show an effect: does AdEMAMix reach a training-loss target sooner than AdamW, and does it end up at a better loss? Ranked here by final test loss, with epochs-to-target reported alongside.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`bf5363802d3172f44734bddfc3fa3b343f1ca2c82499f99265d7c90b4d341130`

## 最优方案

`ademamix_warmup_45`：主指标 `test_loss` = **0.099815**，测试准确率 **95.50%**，测试损失 `0.09981541`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix_warmup_45 | 95.50% | 0.09981541 | 120 | 6 | 1727.44 |
| ademamix_warmup_120 | 95.50% | 0.10295264 | 120 | 6 | 1914.072 |
| ademamix_no_warmups | 94.50% | 0.10621263 | 120 | 6 | 1283.475 |
| adamw | 94.50% | 0.10625349 | 120 | 6 | 1288.161 |
| sgd_momentum | 95.50% | 0.10666138 | 120 | 5 | 1924.501 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.143` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
