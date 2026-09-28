# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`287c2c36e56c5995e92812c454f21f09d26283a0e7cace0fab7ab4d2e9cb462c`

## 最优方案

`sgd_cosine`：主指标 `test_loss` = **0.156026**，测试准确率 **94.00%**，测试损失 `0.15602591`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_cosine | 94.00% | 0.15602591 | 200 | 21 | 2301.568 |
| schedule_free_sgd | 93.50% | 0.15987465 | 200 | 33 | 2336.337 |
| adamw_cosine | 93.50% | 0.16577598 | 200 | 6 | 2354.652 |
| schedule_free_adamw | 93.00% | 0.17194125 | 200 | 5 | 2346.546 |
| adamw_constant | 93.00% | 0.17947897 | 200 | 6 | 2308.08 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
