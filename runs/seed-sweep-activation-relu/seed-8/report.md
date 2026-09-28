# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on the hidden activation. This suite is the tanh [32] suite with ReLU instead, same budget, every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`74e790ec38db50f4ecd5f7b8dde426da072ef7622b2d9b076a94461e02ecd5d4`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.159906**，测试准确率 **93.50%**，测试损失 `0.15990574`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.15990574 | 200 | 11 | 8195.351 |
| schedule_free_adamw | 94.00% | 0.16535767 | 200 | 30 | 8182.411 |
| adamw_constant | 93.00% | 0.18043398 | 200 | 18 | 8235.382 |
| adam | 93.00% | 0.18043398 | 200 | 18 | 8227.689 |
| ademamix | 93.00% | 0.18138288 | 200 | 18 | 8218.098 |
| adamw_cosine | 93.00% | 0.19666076 | 200 | 7 | 8203.453 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
