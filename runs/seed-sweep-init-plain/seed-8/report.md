# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], plain fixed-0.05 initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (plain fixed-0.05 initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`d2e4dc0a5381c7a93e2e3e0e1d8769119b2dde16cb3c5770bfbe7986bde20245`

## 最优方案

`adamw_cosine`：主指标 `test_loss` = **0.159653**，测试准确率 **94.00%**，测试损失 `0.15965272`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_cosine | 94.00% | 0.15965272 | 200 | 6 | 7985.552 |
| schedule_free_adamw | 94.00% | 0.15996797 | 200 | 10 | 7940.458 |
| adagrad | 93.00% | 0.16914303 | 200 | 7 | 7997.374 |
| adamw_constant | 93.00% | 0.20089607 | 200 | 3 | 8007.158 |
| adam | 93.00% | 0.20089607 | 200 | 3 | 8096.619 |
| ademamix | 93.00% | 0.20222834 | 200 | 3 | 8017.198 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
