# AutoResearch Lite 实验报告

- 任务：optimizer convergence speed on a fixed synthetic task
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：At a matched epoch budget, and with each optimizer family tuned by the same coarse learning-rate sweep, Adam reaches a training-loss target close to the converged floor in as few epochs as SGD, SGD with momentum, AdaGrad and RMSProp — and disabling Adam's bias correction changes when the target is reached.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`b5d8543a0ad0819105fb01ef42499e6cb67e76ee5d04b061b416adc2a60ceb0d`

## 最优方案

`adagrad`：主指标 `epochs_to_target` = **7**，测试准确率 **94.00%**，测试损失 `0.12508883`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.00% | 0.12508883 | 120 | 7 | 130.935 |
| adam_no_bias_correction | 94.00% | 0.12436026 | 79 | 12 | 85.051 |
| sgd_momentum | 94.00% | 0.12684141 | 120 | 20 | 125.138 |
| adam | 94.00% | 0.12654099 | 120 | 28 | 131.465 |
| rmsprop | 94.50% | 0.12345586 | 120 | 50 | 131.853 |
| baseline | 94.50% | 0.21869154 | 120 | 未达标 | 125.947 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.16` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
