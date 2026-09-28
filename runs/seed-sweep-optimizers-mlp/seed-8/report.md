# AutoResearch Lite 实验报告

- 任务：optimizer convergence speed on the two-layer MLP trainer
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：The logistic head has two weights and a bias, so 'Adam is mid-pack on time-to-target' could be an artefact of an almost-convex model. This runs the same question on a two-layer tanh MLP with every family retuned for that model: at a matched epoch budget, does Adam reach a training-loss target in fewer epochs than SGD, momentum, AdaGrad and RMSProp?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`a36a650f7c571079ba7ce7f607be37b8824124c2105e04117f5b3e180344d78a`

## 最优方案

`adagrad`：主指标 `epochs_to_target` = **3**，测试准确率 **93.00%**，测试损失 `0.16276741`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.00% | 0.16276741 | 120 | 3 | 1338.088 |
| sgd_momentum | 93.50% | 0.16283995 | 120 | 6 | 1332.416 |
| rmsprop | 93.50% | 0.1663102 | 120 | 18 | 1320.406 |
| adam | 92.00% | 0.21724299 | 120 | 18 | 1323.046 |
| sgd | 94.00% | 0.15660128 | 120 | 21 | 1341.389 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
