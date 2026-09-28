# AutoResearch Lite 实验报告

- 任务：paper-inspired binary classification optimization
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：Adam 的一阶/二阶矩估计与偏差修正，可以在相同任务上比固定学习率 SGD 更快收敛。
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`5aa54ce6a0d99640f8ef305e93d604a1aeca484d1e93f0890106dd353ecc22e6`

## 最优方案

`adam_reproduction`：主指标 `test_loss` = **0.166607**，测试准确率 **98.00%**，测试损失 `0.16660726`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adam_reproduction | 98.00% | 0.16660726 | 80 | 未达标 | 80.808 |
| sgd_control | 97.00% | 0.24736677 | 80 | 未达标 | 82.535 |
| adam_regularized | 97.50% | 0.28119885 | 100 | 未达标 | 102.249 |
| baseline | 96.00% | 0.35596295 | 80 | 未达标 | 83.348 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
