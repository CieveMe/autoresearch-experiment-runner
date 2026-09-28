# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], layernorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (layernorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`9f3127047a2bee54a2f0c5fcbeae080fdb86b019f3019493835e2332aaad040e`

## 最优方案

`adamw_cosine`：主指标 `test_loss` = **0.135581**，测试准确率 **93.50%**，测试损失 `0.13558088`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_cosine | 93.50% | 0.13558088 | 200 | 20 | 10093.286 |
| adagrad | 93.50% | 0.1358193 | 200 | 15 | 10271.598 |
| schedule_free_adamw | 93.50% | 0.13782789 | 200 | 7 | 10309.269 |
| ademamix | 93.50% | 0.13818288 | 200 | 13 | 10001.857 |
| adamw_constant | 93.50% | 0.13819853 | 200 | 13 | 10276.005 |
| adam | 93.50% | 0.13819853 | 200 | 13 | 10250.39 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
