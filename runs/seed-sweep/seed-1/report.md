# AutoResearch Lite 实验报告

- 任务：paper-inspired binary classification optimization
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：Adam 的一阶/二阶矩估计与偏差修正，可以在相同任务上比固定学习率 SGD 更快收敛。
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`f8b0b46a7a620869d7faefbc771ba4a7952a6ed5c9f4b7430b01ff47809898b9`

## 最优方案

`adam_reproduction`：主指标 `test_loss` = **0.205804**，测试准确率 **94.00%**，测试损失 `0.20580388`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adam_reproduction | 94.00% | 0.20580388 | 80 | 未达标 | 84.08 |
| sgd_control | 93.00% | 0.28520789 | 80 | 未达标 | 79.18 |
| adam_regularized | 93.50% | 0.32228396 | 100 | 未达标 | 106.82 |
| baseline | 93.50% | 0.38525401 | 80 | 未达标 | 81.421 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
