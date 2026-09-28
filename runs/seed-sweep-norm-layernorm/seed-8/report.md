# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], layernorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (layernorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`dfafdab4eec7010f24e9f64a63e4a6954f446c06d10788f96f41ce03c3487cef`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.173592**，测试准确率 **93.00%**，测试损失 `0.17359218`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.00% | 0.17359218 | 200 | 6 | 10887.348 |
| adamw_cosine | 92.50% | 0.17518164 | 200 | 6 | 10280.882 |
| ademamix | 92.50% | 0.17935586 | 200 | 8 | 11878.171 |
| adamw_constant | 92.50% | 0.17968908 | 200 | 8 | 11065.033 |
| adam | 92.50% | 0.17968908 | 200 | 8 | 11079.257 |
| schedule_free_adamw | 92.50% | 0.18991776 | 200 | 4 | 11579.592 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
