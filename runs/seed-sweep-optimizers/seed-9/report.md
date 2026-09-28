# AutoResearch Lite 实验报告

- 任务：optimizer convergence speed on a fixed synthetic task
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：At a matched epoch budget, and with each optimizer family tuned by the same coarse learning-rate sweep, Adam reaches a training-loss target close to the converged floor in as few epochs as SGD, SGD with momentum, AdaGrad and RMSProp — and disabling Adam's bias correction changes when the target is reached.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`e9867a91839052b3381540379a64d8692ea6919e7d299d9d3257aae387b1ff5e`

## 最优方案

`adagrad`：主指标 `epochs_to_target` = **2**，测试准确率 **93.00%**，测试损失 `0.14336217`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.00% | 0.14336217 | 120 | 2 | 130.98 |
| adam_no_bias_correction | 93.00% | 0.14382444 | 120 | 9 | 131.025 |
| sgd_momentum | 93.50% | 0.14366816 | 120 | 15 | 129.846 |
| adam | 93.00% | 0.14397553 | 120 | 19 | 127.337 |
| rmsprop | 93.50% | 0.14142939 | 120 | 37 | 127.395 |
| baseline | 93.50% | 0.21270791 | 120 | 未达标 | 126.615 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.16` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
