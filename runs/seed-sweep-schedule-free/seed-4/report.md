# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule, at a matched budget
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：The paper claims a schedule-free method needs no learning-rate schedule and still matches, or beats, a well-tuned cosine decay. The comparison is only meaningful if the cosine baseline is tuned, so its learning rate AND its minimum-learning-rate factor were swept (examples/schedule-free-sweep.json, 21 trials); the strongest constant-learning-rate baseline is included as well, because a constant rate is exactly what schedule-free is meant to replace.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`7e4dbf6e3cb97631e576fdcde1ddc94907ca9e79fb0067156d333faed9994c90`

## 最优方案

`adamw_constant`：主指标 `test_loss` = **0.083989**，测试准确率 **98.00%**，测试损失 `0.08398865`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant | 98.00% | 0.08398865 | 200 | 29 | 211.634 |
| adamw_cosine | 98.00% | 0.08637586 | 200 | 30 | 223.574 |
| schedule_free_adamw | 98.00% | 0.08651179 | 200 | 83 | 226.631 |
| schedule_free_sgd | 97.50% | 0.15849437 | 200 | 未达标 | 247.091 |
| sgd_cosine | 97.50% | 0.17983007 | 199 | 未达标 | 226.487 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
