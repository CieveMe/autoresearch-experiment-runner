# AutoResearch Lite 实验报告

- 任务：AdEMAMix on the two-layer MLP: speed versus final quality
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：The logistic head is almost convex and converges in tens of steps, which is the wrong regime for a second, slower moving average. On a two-layer tanh MLP the same comparison may show an effect: does AdEMAMix reach a training-loss target sooner than AdamW, and does it end up at a better loss? Ranked here by final test loss, with epochs-to-target reported alongside.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`338aada836cd682dc52875bb668bc45895dfb478285fdb6e0294ab97f7db0d35`

## 最优方案

`sgd_momentum`：主指标 `test_loss` = **0.162840**，测试准确率 **93.50%**，测试损失 `0.16283995`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_momentum | 93.50% | 0.16283995 | 120 | 6 | 1426.095 |
| adamw | 93.50% | 0.16607861 | 120 | 6 | 1374.192 |
| ademamix_no_warmups | 93.50% | 0.16629654 | 120 | 6 | 1393.467 |
| ademamix_warmup_45 | 92.00% | 0.19632853 | 120 | 6 | 1367.284 |
| ademamix_warmup_120 | 92.00% | 0.2126496 | 120 | 6 | 1396.443 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.143` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
