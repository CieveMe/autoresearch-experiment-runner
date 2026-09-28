# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], layernorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (layernorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`51c2b8c3056f9a7f995d62f51e29b11c110c9809bd98a9724c3973ce15bb56cc`

## 最优方案

`ademamix`：主指标 `test_loss` = **0.082276**，测试准确率 **97.00%**，测试损失 `0.08227596`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix | 97.00% | 0.08227596 | 200 | 14 | 12659.781 |
| adamw_constant | 97.00% | 0.08232065 | 200 | 14 | 11166.18 |
| adam | 97.00% | 0.08232065 | 200 | 14 | 11259.974 |
| adamw_cosine | 98.00% | 0.08311056 | 200 | 9 | 11235.089 |
| adagrad | 97.50% | 0.08327266 | 200 | 5 | 10745.042 |
| schedule_free_adamw | 97.50% | 0.08481521 | 200 | 5 | 11630.188 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
