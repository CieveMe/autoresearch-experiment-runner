# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], He initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (He initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`d2f963afb80b6b3c9985310ee77cdec68bb328c62ae959ca375201e2b8b55426`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.191441**，测试准确率 **93.00%**，测试损失 `0.19144076`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.00% | 0.19144076 | 200 | 11 | 8157.154 |
| schedule_free_adamw | 93.00% | 0.20754148 | 200 | 3 | 7942.43 |
| adamw_cosine | 92.00% | 0.22916305 | 200 | 4 | 8143.952 |
| adamw_constant | 92.00% | 0.28232302 | 200 | 4 | 8058.477 |
| adam | 92.00% | 0.28232302 | 200 | 4 | 8084.735 |
| ademamix | 92.00% | 0.28907951 | 200 | 4 | 8080.062 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
