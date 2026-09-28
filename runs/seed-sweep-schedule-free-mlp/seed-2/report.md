# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`71d7887beb16b26997655c5a25bc94954434aeda3c4116d6996bf91dff67d924`

## 最优方案

`schedule_free_sgd`：主指标 `test_loss` = **0.139172**，测试准确率 **91.50%**，测试损失 `0.13917162`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_sgd | 91.50% | 0.13917162 | 200 | 61 | 2514.636 |
| sgd_cosine | 91.50% | 0.14420389 | 200 | 47 | 2686.089 |
| schedule_free_adamw | 92.00% | 0.14771333 | 200 | 11 | 2482.187 |
| adamw_cosine | 92.50% | 0.15005743 | 200 | 7 | 2527.814 |
| adamw_constant | 92.50% | 0.15223806 | 200 | 7 | 2561.184 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
