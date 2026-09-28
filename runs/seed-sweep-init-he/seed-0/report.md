# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], He initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (He initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`1d3064b5070cebd845eaae696fd728267032cea7f377d94e01830853b935fd1b`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.132985**，测试准确率 **92.50%**，测试损失 `0.13298507`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 92.50% | 0.13298507 | 200 | 6 | 8187.592 |
| schedule_free_adamw | 92.50% | 0.16198603 | 200 | 3 | 8009.98 |
| adamw_cosine | 92.50% | 0.16259999 | 200 | 3 | 8757.242 |
| adamw_constant | 93.00% | 0.16949387 | 200 | 3 | 8816.819 |
| adam | 93.00% | 0.16949387 | 200 | 3 | 8544.598 |
| ademamix | 93.00% | 0.17116761 | 200 | 3 | 8161.398 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
