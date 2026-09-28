# AutoResearch Lite 实验报告

- 任务：optimizer convergence speed on the two-layer MLP trainer
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：The logistic head has two weights and a bias, so 'Adam is mid-pack on time-to-target' could be an artefact of an almost-convex model. This runs the same question on a two-layer tanh MLP with every family retuned for that model: at a matched epoch budget, does Adam reach a training-loss target in fewer epochs than SGD, momentum, AdaGrad and RMSProp?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`aaba734bb5efa86e026e2b313b24ac4a1851b52090d86f2e254adf560172507f`

## 最优方案

`sgd_momentum`：主指标 `epochs_to_target` = **8**，测试准确率 **93.00%**，测试损失 `0.12544684`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_momentum | 93.00% | 0.12544684 | 120 | 8 | 1325.545 |
| adagrad | 93.50% | 0.12775166 | 120 | 14 | 1349.254 |
| adam | 93.00% | 0.12363451 | 120 | 36 | 1340.788 |
| rmsprop | 93.00% | 0.12958927 | 120 | 45 | 1326.506 |
| sgd | 93.50% | 0.12460319 | 120 | 70 | 1327.383 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
