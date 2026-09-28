# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on the hidden activation. This suite is the tanh [32] suite with ReLU instead, same budget, every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`9f5bd71d4b5a548396feaa9376f7c1eaf10026dc3135ba6f3618faa7932b1793`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.127655**，测试准确率 **95.00%**，测试损失 `0.12765473`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 95.00% | 0.12765473 | 200 | 9 | 8209.562 |
| adamw_constant | 95.00% | 0.12780698 | 200 | 15 | 8257.261 |
| adam | 95.00% | 0.12780698 | 200 | 15 | 8178.805 |
| ademamix | 95.50% | 0.12783871 | 200 | 15 | 8327.978 |
| schedule_free_adamw | 95.00% | 0.13151474 | 200 | 27 | 8300.764 |
| adamw_cosine | 94.50% | 0.1356748 | 200 | 5 | 8302.984 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
