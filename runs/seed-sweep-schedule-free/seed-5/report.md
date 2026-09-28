# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule, at a matched budget
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：The paper claims a schedule-free method needs no learning-rate schedule and still matches, or beats, a well-tuned cosine decay. The comparison is only meaningful if the cosine baseline is tuned, so its learning rate AND its minimum-learning-rate factor were swept (examples/schedule-free-sweep.json, 21 trials); the strongest constant-learning-rate baseline is included as well, because a constant rate is exactly what schedule-free is meant to replace.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`669f265148793fd90efa3a91e639e24c002e25134434abd45a88dd561433eb45`

## 最优方案

`adamw_constant`：主指标 `test_loss` = **0.124721**，测试准确率 **94.00%**，测试损失 `0.12472085`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant | 94.00% | 0.12472085 | 200 | 44 | 237.168 |
| adamw_cosine | 94.00% | 0.12703685 | 200 | 46 | 245.198 |
| schedule_free_adamw | 94.00% | 0.12733484 | 200 | 115 | 230.031 |
| schedule_free_sgd | 94.50% | 0.21024941 | 200 | 未达标 | 244.262 |
| sgd_cosine | 94.50% | 0.23170823 | 199 | 未达标 | 234.764 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
