# AutoResearch Lite 实验报告

- 任务：Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：Same question as the logistic suite, on a model with curvature: does schedule-free AdamW beat, or at least match, a cosine schedule that was tuned over both its learning rate and its minimum-learning-rate factor - and does a constant learning rate remain competitive?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`82cac0b2819e0ff535416328e493946b7b824f108d8e5f2573d98588513199d0`

## 最优方案

`sgd_cosine`：主指标 `test_loss` = **0.124976**，测试准确率 **95.00%**，测试损失 `0.12497644`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_cosine | 95.00% | 0.12497644 | 200 | 20 | 2318.468 |
| schedule_free_sgd | 95.00% | 0.12850354 | 200 | 32 | 2297.52 |
| schedule_free_adamw | 95.00% | 0.13455127 | 200 | 7 | 2295.06 |
| adamw_cosine | 94.50% | 0.13580841 | 200 | 5 | 2333.689 |
| adamw_constant | 95.00% | 0.13639211 | 200 | 5 | 2332.37 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.148` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
