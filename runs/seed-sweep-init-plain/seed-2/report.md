# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], plain fixed-0.05 initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (plain fixed-0.05 initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`761bf01dbf18a3fc0fe1fc23f96d393ed541a0e6ef7f707498c95eb99e3cd17e`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.138179**，测试准确率 **92.50%**，测试损失 `0.13817888`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 92.50% | 0.13817888 | 200 | 26 | 8135.568 |
| schedule_free_adamw | 92.00% | 0.13983568 | 200 | 13 | 7968.47 |
| adamw_cosine | 92.00% | 0.14315527 | 200 | 8 | 8258.881 |
| adamw_constant | 92.50% | 0.15291875 | 200 | 23 | 8079.272 |
| adam | 92.50% | 0.15291875 | 200 | 23 | 8241.345 |
| ademamix | 92.50% | 0.15337268 | 200 | 23 | 8047.646 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
