# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], plain fixed-0.05 initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (plain fixed-0.05 initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`dfaf91c1d2d383f82c615130956baae123763cdef5af3e269debf942ca562865`

## 最优方案

`ademamix`：主指标 `test_loss` = **0.074792**，测试准确率 **97.50%**，测试损失 `0.07479193`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix | 97.50% | 0.07479193 | 200 | 20 | 8196.259 |
| adamw_constant | 97.50% | 0.07529784 | 200 | 20 | 8035.919 |
| adam | 97.50% | 0.07529784 | 200 | 20 | 8085.215 |
| adamw_cosine | 98.00% | 0.080648 | 200 | 8 | 8106.151 |
| schedule_free_adamw | 98.00% | 0.08180586 | 200 | 11 | 8021.426 |
| adagrad | 97.50% | 0.09096551 | 200 | 24 | 8071.439 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
