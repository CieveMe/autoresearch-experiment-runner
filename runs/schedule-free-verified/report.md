# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule, at a matched budget
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：The paper claims a schedule-free method needs no learning-rate schedule and still matches, or beats, a well-tuned cosine decay. The comparison is only meaningful if the cosine baseline is tuned, so its learning rate AND its minimum-learning-rate factor were swept (examples/schedule-free-sweep.json, 21 trials); the strongest constant-learning-rate baseline is included as well, because a constant rate is exactly what schedule-free is meant to replace.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`3592a75bdfd388764ba55cf75fe77af25b2e25a7ce4240eb5c9f226259f0d779`

## 最优方案

`adamw_constant`：主指标 `test_loss` = **0.122283**，测试准确率 **93.50%**，测试损失 `0.12228349`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant | 93.50% | 0.12228349 | 200 | 70 | 217.105 |
| adamw_cosine | 93.50% | 0.12381987 | 200 | 80 | 215.862 |
| schedule_free_adamw | 93.50% | 0.12395906 | 200 | 154 | 214.615 |
| schedule_free_sgd | 94.00% | 0.1954666 | 200 | 未达标 | 220.695 |
| sgd_cosine | 93.50% | 0.2159042 | 199 | 未达标 | 215.493 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
