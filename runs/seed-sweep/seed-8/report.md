# AutoResearch Lite 实验报告

- 任务：paper-inspired binary classification optimization
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：Adam 的一阶/二阶矩估计与偏差修正，可以在相同任务上比固定学习率 SGD 更快收敛。
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`36dad03c0b389738be0aa5e80ce109532de6a9ad396bfdb53c52035b915ece91`

## 最优方案

`adam_reproduction`：主指标 `test_loss` = **0.226114**，测试准确率 **94.50%**，测试损失 `0.22611405`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adam_reproduction | 94.50% | 0.22611405 | 80 | 未达标 | 89.014 |
| sgd_control | 93.50% | 0.30168357 | 80 | 未达标 | 86.562 |
| adam_regularized | 93.50% | 0.34124891 | 100 | 未达标 | 105.061 |
| baseline | 94.50% | 0.39869362 | 80 | 未达标 | 88.923 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
