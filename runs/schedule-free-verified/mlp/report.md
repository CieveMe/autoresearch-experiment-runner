# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`e420acd848306e2138a703ca937279b4abf79fb2e0c2868b2ccbf75ac59a233f`

## 最优方案

`adamw_constant`：主指标 `test_loss` = **0.125013**，测试准确率 **93.00%**，测试损失 `0.12501296`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant | 93.00% | 0.12501296 | 200 | 22 | 2285.565 |
| sgd_cosine | 93.50% | 0.12501563 | 200 | 71 | 2329.718 |
| schedule_free_adamw | 93.50% | 0.12506323 | 200 | 11 | 2313.741 |
| schedule_free_sgd | 93.50% | 0.12530471 | 200 | 79 | 2269.494 |
| adamw_cosine | 93.00% | 0.12699107 | 200 | 23 | 2288.527 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
