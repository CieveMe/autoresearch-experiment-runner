# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`7d9c6111dca1d4c7f86074980a0fd623414b94172196b295ec4a10bd1fcc4889`

## 最优方案

`schedule_free_sgd`：主指标 `test_loss` = **0.118575**，测试准确率 **95.50%**，测试损失 `0.1185749`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_sgd | 95.50% | 0.1185749 | 200 | 34 | 2477.712 |
| sgd_cosine | 95.50% | 0.12106211 | 200 | 22 | 2525.123 |
| schedule_free_adamw | 95.00% | 0.12812487 | 200 | 6 | 2445.622 |
| adamw_cosine | 94.50% | 0.12857465 | 200 | 6 | 2393.917 |
| adamw_constant | 94.00% | 0.13394786 | 200 | 6 | 2398.051 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
