# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on the hidden activation. This suite is the tanh [32] suite with ReLU instead, same budget, every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`e88a34eb56b8b46bd7c6ff4d62d2f1090d7cc2f97a471128b63592050294a931`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.082229**，测试准确率 **97.00%**，测试损失 `0.08222949`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 97.00% | 0.08222949 | 200 | 11 | 8270.929 |
| adamw_constant | 97.00% | 0.08252366 | 200 | 14 | 8209.964 |
| adam | 97.00% | 0.08252366 | 200 | 14 | 8198.566 |
| ademamix | 97.00% | 0.0825481 | 200 | 14 | 8269.051 |
| adamw_cosine | 97.50% | 0.08263973 | 200 | 5 | 8277.033 |
| schedule_free_adamw | 97.50% | 0.08274705 | 200 | 27 | 8260.039 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
