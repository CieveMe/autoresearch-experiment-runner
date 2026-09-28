# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], plain fixed-0.05 initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (plain fixed-0.05 initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`61e0446fb001dc58ab9c74126b29d97b6cd87f3070f79c58de04014c02746396`

## 最优方案

`adamw_cosine`：主指标 `test_loss` = **0.125417**，测试准确率 **94.50%**，测试损失 `0.12541731`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_cosine | 94.50% | 0.12541731 | 200 | 10 | 8204.812 |
| schedule_free_adamw | 94.50% | 0.1257092 | 200 | 15 | 8023.02 |
| adamw_constant | 94.50% | 0.1379499 | 200 | 31 | 8112.284 |
| adam | 94.50% | 0.1379499 | 200 | 31 | 8087.915 |
| ademamix | 94.50% | 0.1403651 | 200 | 31 | 8070.959 |
| adagrad | 94.00% | 0.1450132 | 200 | 30 | 8061.946 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
