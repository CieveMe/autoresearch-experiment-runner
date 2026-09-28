# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`44352819f7acb8a3bfffea2c4c46dc1fef82b9e78efffe5eaa47bb5bb52571b9`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.078371**，测试准确率 **97.50%**，测试损失 `0.07837142`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 97.50% | 0.07837142 | 200 | 13 | 2293.49 |
| adamw_cosine | 97.00% | 0.08190946 | 200 | 11 | 2342.784 |
| schedule_free_sgd | 98.00% | 0.08226629 | 200 | 54 | 2305.816 |
| adamw_constant | 97.50% | 0.08387601 | 200 | 11 | 2309.196 |
| sgd_cosine | 98.00% | 0.08566149 | 200 | 39 | 2296.448 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
