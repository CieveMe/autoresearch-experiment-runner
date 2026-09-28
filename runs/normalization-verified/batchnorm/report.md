# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], batchnorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (batchnorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`9166f25495ece439c4022465c234e238d865a239200712a0d8e996af695b549c`

## 最优方案

`adamw_constant`：主指标 `test_loss` = **0.119630**，测试准确率 **93.50%**，测试损失 `0.11962998`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant | 93.50% | 0.11962998 | 200 | 5 | 10417.149 |
| adam | 93.50% | 0.11962998 | 200 | 5 | 10517.56 |
| ademamix | 93.50% | 0.11964048 | 200 | 5 | 10505.188 |
| adamw_cosine | 93.50% | 0.11967868 | 200 | 5 | 10605.328 |
| adagrad | 94.00% | 0.11973749 | 200 | 12 | 10537.212 |
| schedule_free_adamw | 94.00% | 0.11986439 | 200 | 7 | 10613.008 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
