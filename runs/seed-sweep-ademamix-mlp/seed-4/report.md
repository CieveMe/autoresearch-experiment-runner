# AutoResearch Lite 实验报告

- 任务：AdEMAMix on the two-layer MLP: speed versus final quality
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：The logistic head is almost convex and converges in tens of steps, which is the wrong regime for a second, slower moving average. On a two-layer tanh MLP the same comparison may show an effect: does AdEMAMix reach a training-loss target sooner than AdamW, and does it end up at a better loss? Ranked here by final test loss, with epochs-to-target reported alongside.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`e91b2148e01a96a1ded16c7f2ca080742407ae758251e07e7fec9c54d4bc2f48`

## 最优方案

`sgd_momentum`：主指标 `test_loss` = **0.080582**，测试准确率 **97.50%**，测试损失 `0.08058201`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_momentum | 97.50% | 0.08058201 | 120 | 9 | 1589.384 |
| adamw | 97.50% | 0.08174844 | 120 | 11 | 1913.056 |
| ademamix_no_warmups | 97.50% | 0.08213844 | 120 | 11 | 1948.133 |
| ademamix_warmup_45 | 97.00% | 0.09015425 | 120 | 11 | 1836.022 |
| ademamix_warmup_120 | 97.00% | 0.09454079 | 120 | 11 | 1941.597 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.143` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
