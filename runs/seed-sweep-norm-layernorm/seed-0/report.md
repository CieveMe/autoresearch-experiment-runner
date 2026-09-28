# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], layernorm on the hidden pre-activations (Xavier init): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (layernorm on the hidden pre-activations (Xavier init)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`fbfb5c39f3b45cc5ebf160de135f22a84b2132fa5b1bcd38b9920ad1fbe34dab`

## 最优方案

`adamw_cosine`：主指标 `test_loss` = **0.121064**，测试准确率 **94.00%**，测试损失 `0.12106439`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_cosine | 94.00% | 0.12106439 | 200 | 5 | 9887.545 |
| adagrad | 94.50% | 0.12302474 | 200 | 5 | 10928.957 |
| ademamix | 94.00% | 0.12337946 | 200 | 7 | 10928.69 |
| adamw_constant | 94.00% | 0.12356712 | 200 | 7 | 10446.973 |
| adam | 94.00% | 0.12356712 | 200 | 7 | 10120.874 |
| schedule_free_adamw | 94.00% | 0.12682521 | 200 | 4 | 11155.136 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
