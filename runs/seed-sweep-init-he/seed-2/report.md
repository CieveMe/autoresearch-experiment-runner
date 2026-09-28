# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], He initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (He initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`1375879fc98b4a21197d3b0e6694ad9d209454bd8e36f32523a6f30d8464b50c`

## 最优方案

`adamw_cosine`：主指标 `test_loss` = **0.150410**，测试准确率 **92.50%**，测试损失 `0.15040999`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_cosine | 92.50% | 0.15040999 | 200 | 24 | 8236.427 |
| schedule_free_adamw | 92.50% | 0.15047756 | 200 | 7 | 8128.792 |
| adamw_constant | 93.00% | 0.1525016 | 200 | 24 | 8267.435 |
| adam | 93.00% | 0.1525016 | 200 | 24 | 8168.259 |
| ademamix | 93.00% | 0.15259798 | 200 | 24 | 8210.181 |
| adagrad | 92.00% | 0.15486478 | 200 | 17 | 8179.624 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
