# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], batchnorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (batchnorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`9e52c86461f71ce7b2e886cd8d8f9d6f4f14eb527418e9d09b84dbe37c173b2c`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.131020**，测试准确率 **93.50%**，测试损失 `0.13101954`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.13101954 | 200 | 7 | 11106.787 |
| adamw_cosine | 93.50% | 0.13179762 | 200 | 3 | 12996.042 |
| schedule_free_adamw | 93.50% | 0.13233031 | 200 | 5 | 10844.201 |
| ademamix | 93.50% | 0.13250895 | 200 | 3 | 11525.405 |
| adamw_constant | 93.50% | 0.13250987 | 200 | 3 | 10542.184 |
| adam | 93.50% | 0.13250987 | 200 | 3 | 10593.707 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
