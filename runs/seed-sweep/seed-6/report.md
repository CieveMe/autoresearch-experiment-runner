# AutoResearch Lite 实验报告

- 任务：paper-inspired binary classification optimization
- 论文：Adam: A Method for Stochastic Optimization
- 论文标识：arXiv:1412.6980
- 假设：Adam 的一阶/二阶矩估计与偏差修正，可以在相同任务上比固定学习率 SGD 更快收敛。
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`f942cba4ef3ae4ff19a592c0daad24fa225a5758d27e81c82e12b68b72c24675`

## 最优方案

`adam_reproduction`：主指标 `test_loss` = **0.197325**，测试准确率 **94.50%**，测试损失 `0.19732487`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adam_reproduction | 94.50% | 0.19732487 | 80 | 未达标 | 83.164 |
| sgd_control | 95.50% | 0.26883512 | 80 | 未达标 | 81.705 |
| adam_regularized | 95.50% | 0.30928906 | 100 | 未达标 | 101.882 |
| baseline | 95.50% | 0.37240638 | 80 | 未达标 | 80.258 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
