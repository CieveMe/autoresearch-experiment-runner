# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`d2217b1cdef855b07fbdcd81ebc13aedfcef0e86b24cead3d7f031f1c8b0ad45`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.105456**，测试准确率 **95.50%**，测试损失 `0.10545637`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 95.50% | 0.10545637 | 200 | 5 | 2338.236 |
| schedule_free_sgd | 95.50% | 0.10554433 | 200 | 26 | 2292.951 |
| adamw_cosine | 94.50% | 0.10680872 | 200 | 3 | 2222.886 |
| sgd_cosine | 95.00% | 0.10753157 | 200 | 16 | 2297.844 |
| adamw_constant | 94.00% | 0.12382114 | 200 | 3 | 2285.097 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
