# AutoResearch Lite 实验报告

- 任务：paper-inspired binary classification optimization
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：Adam 的一阶/二阶矩估计与偏差修正，可以在相同任务上比固定学习率 SGD 更快收敛。
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`fe34bbeb3881da8f8c37e6e032b735202b7f237d1a277d8de292ed630b727748`

## 最优方案

`adam_reproduction`：主指标 `test_loss` = **0.228829**，测试准确率 **92.00%**，测试损失 `0.22882864`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adam_reproduction | 92.00% | 0.22882864 | 80 | 未达标 | 80.204 |
| sgd_control | 94.50% | 0.30370702 | 80 | 未达标 | 81.737 |
| adam_regularized | 93.00% | 0.34081904 | 100 | 未达标 | 104.284 |
| baseline | 93.00% | 0.40094415 | 80 | 未达标 | 81.616 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
