# AutoResearch Lite 实验报告

- 任务：paper-inspired binary classification optimization
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：Adam 的一阶/二阶矩估计与偏差修正，可以在相同任务上比固定学习率 SGD 更快收敛。
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`7bfe308e676d457e8f2e729e4bf28ea792d25797af826dda819e2d9faf0ee0f8`

## 最优方案

`adam_reproduction`：主指标 `test_loss` = **0.211997**，测试准确率 **93.50%**，测试损失 `0.21199707`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adam_reproduction | 93.50% | 0.21199707 | 80 | 未达标 | 86.148 |
| sgd_control | 93.50% | 0.28303419 | 80 | 未达标 | 85.24 |
| adam_regularized | 93.50% | 0.32322469 | 100 | 未达标 | 107.4 |
| baseline | 92.50% | 0.38104976 | 80 | 未达标 | 81.954 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
