# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], He initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (He initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`1da336133e6fe169760deb46442b6c28571f229918362460375c807342feedb0`

## 最优方案

`ademamix`：主指标 `test_loss` = **0.123066**，测试准确率 **93.00%**，测试损失 `0.12306551`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix | 93.00% | 0.12306551 | 200 | 37 | 8064.631 |
| adamw_constant | 93.50% | 0.12321829 | 200 | 37 | 8158.695 |
| adam | 93.50% | 0.12321829 | 200 | 37 | 7916.1 |
| adagrad | 93.50% | 0.12455205 | 200 | 33 | 8052.752 |
| schedule_free_adamw | 93.00% | 0.12610458 | 200 | 11 | 8175.861 |
| adamw_cosine | 92.50% | 0.12722933 | 200 | 37 | 7871.73 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
