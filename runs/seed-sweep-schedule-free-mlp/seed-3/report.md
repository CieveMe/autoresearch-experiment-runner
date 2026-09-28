# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`468d669fd324939ba934ed11dc09b87e5de49f3e362e47ac0228630e666714df`

## 最优方案

`sgd_cosine`：主指标 `test_loss` = **0.124413**，测试准确率 **93.50%**，测试损失 `0.12441329`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_cosine | 93.50% | 0.12441329 | 200 | 53 | 2346.39 |
| schedule_free_sgd | 94.00% | 0.12865717 | 200 | 65 | 2342.974 |
| schedule_free_adamw | 94.00% | 0.13374991 | 200 | 14 | 2352.505 |
| adamw_cosine | 94.50% | 0.1343782 | 200 | 9 | 2369.058 |
| adamw_constant | 93.50% | 0.1367019 | 200 | 9 | 2535.587 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
