# AutoResearch Lite 实验报告

- 任务：AdEMAMix on the two-layer MLP: speed versus final quality
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：The logistic head is almost convex and converges in tens of steps, which is the wrong regime for a second, slower moving average. On a two-layer tanh MLP the same comparison may show an effect: does AdEMAMix reach a training-loss target sooner than AdamW, and does it end up at a better loss? Ranked here by final test loss, with epochs-to-target reported alongside.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`fd4050b69ad065512df153c6cd02bcaf669e9fd52f0da61a56ec4bb4920d9728`

## 最优方案

`sgd_momentum`：主指标 `test_loss` = **0.148054**，测试准确率 **92.50%**，测试损失 `0.14805441`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_momentum | 92.50% | 0.14805441 | 120 | 8 | 1964.932 |
| adamw | 92.00% | 0.14939966 | 120 | 7 | 1959.393 |
| ademamix_no_warmups | 92.50% | 0.1499343 | 120 | 7 | 1956.633 |
| ademamix_warmup_45 | 92.50% | 0.15532986 | 120 | 7 | 1923.048 |
| ademamix_warmup_120 | 93.00% | 0.15745413 | 120 | 7 | 1918.878 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.143` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
