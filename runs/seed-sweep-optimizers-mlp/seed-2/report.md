# AutoResearch Lite 实验报告

- 任务：optimizer convergence speed on the two-layer MLP trainer
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：The logistic head has two weights and a bias, so 'Adam is mid-pack on time-to-target' could be an artefact of an almost-convex model. This runs the same question on a two-layer tanh MLP with every family retuned for that model: at a matched epoch budget, does Adam reach a training-loss target in fewer epochs than SGD, momentum, AdaGrad and RMSProp?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`b00696365439fe7f9bc55039b4a9a2da5ba5e01a4abd7c7dac6559df58ca2358`

## 最优方案

`adam`：主指标 `epochs_to_target` = **4**，测试准确率 **90.50%**，测试损失 `0.14824553`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adam | 90.50% | 0.14824553 | 120 | 4 | 1344.86 |
| adagrad | 92.00% | 0.14777904 | 120 | 6 | 1334.718 |
| sgd_momentum | 92.50% | 0.14805441 | 120 | 8 | 1286.824 |
| rmsprop | 92.50% | 0.14764579 | 120 | 37 | 1335.859 |
| sgd | 91.50% | 0.14280686 | 120 | 47 | 1341.119 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
