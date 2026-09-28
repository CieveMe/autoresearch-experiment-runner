# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`e880722d289e0c22a28812f543fdcc4b55ebc1c90feb969c813508954433b1c0`

## 最优方案

`sgd_cosine`：主指标 `test_loss` = **0.144319**，测试准确率 **93.00%**，测试损失 `0.14431902`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_cosine | 93.00% | 0.14431902 | 200 | 24 | 2295.264 |
| schedule_free_sgd | 93.00% | 0.14538767 | 200 | 37 | 2282.652 |
| schedule_free_adamw | 92.50% | 0.15366708 | 200 | 7 | 2321.613 |
| adamw_cosine | 93.50% | 0.1599486 | 200 | 5 | 2310.615 |
| adamw_constant | 94.00% | 0.16816464 | 200 | 5 | 2378.88 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
