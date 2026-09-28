# AutoResearch Lite 实验报告

- 任务：optimizer convergence speed on a fixed synthetic task
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：At a matched epoch budget, and with each optimizer family tuned by the same coarse learning-rate sweep, Adam reaches a training-loss target close to the converged floor in as few epochs as SGD, SGD with momentum, AdaGrad and RMSProp — and disabling Adam's bias correction changes when the target is reached.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`b0e86067c81c9b52073b422b0849d912866085710b2d9667e549664c28a508d3`

## 最优方案

`adagrad`：主指标 `epochs_to_target` = **5**，测试准确率 **91.50%**，测试损失 `0.14104896`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 91.50% | 0.14104896 | 120 | 5 | 131.763 |
| adam_no_bias_correction | 91.50% | 0.13808494 | 71 | 11 | 76.62 |
| sgd_momentum | 91.50% | 0.14353002 | 120 | 18 | 126.259 |
| adam | 91.50% | 0.14382211 | 120 | 25 | 125.074 |
| rmsprop | 92.00% | 0.13866758 | 120 | 48 | 127.316 |
| baseline | 93.00% | 0.23022377 | 120 | 未达标 | 132.101 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.16` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
