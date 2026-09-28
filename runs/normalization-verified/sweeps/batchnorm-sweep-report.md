# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], batchnorm on the hidden pre-activations (Xavier init): tuning sweep (pre-registered N1-N4)
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on this modelling choice (batchnorm on the hidden pre-activations (Xavier init)). Grid identical to the [32] reference so the comparison is controlled; every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`8dd935de4644f0039f5f01c4a4676a0ce544bc5234fe7a9a32cf26261f28d5db`

## 最优方案

`adagrad_lr0.1`：主指标 `test_loss` = **0.119308**，测试准确率 **93.50%**，测试损失 `0.11930848`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad_lr0.1 | 93.50% | 0.11930848 | 200 | 未达标 | 17096.461 |
| schedule_free_adamw_lr0.03 | 93.50% | 0.11937209 | 200 | 未达标 | 16715.59 |
| adamw_constant_lr0.3 | 93.50% | 0.11962998 | 200 | 未达标 | 16031.072 |
| adam_lr0.3 | 93.50% | 0.11962998 | 200 | 未达标 | 16470.979 |
| ademamix_lr0.3 | 93.50% | 0.11964048 | 200 | 未达标 | 16646.865 |
| adamw_cosine_lr0.3 | 93.50% | 0.11967868 | 200 | 未达标 | 16091.939 |
| adamw_cosine_lr0.03 | 94.00% | 0.11968419 | 200 | 未达标 | 16362.483 |
| sgd_momentum_lr0.6 | 94.00% | 0.11969273 | 200 | 未达标 | 18381.222 |
| sgd_momentum_lr0.3 | 94.00% | 0.11972474 | 200 | 未达标 | 17579.857 |
| adamw_constant_lr0.1 | 94.00% | 0.11972903 | 200 | 未达标 | 18538.755 |
| adam_lr0.1 | 94.00% | 0.11972903 | 200 | 未达标 | 17633.523 |
| adamw_cosine_lr0.1 | 94.00% | 0.11973561 | 200 | 未达标 | 14071.605 |
| ademamix_lr0.03 | 94.00% | 0.11973715 | 200 | 未达标 | 19085.866 |
| adagrad_lr0.3 | 94.00% | 0.11973749 | 200 | 未达标 | 16787.247 |
| adamw_constant_lr0.03 | 94.00% | 0.11974022 | 200 | 未达标 | 15142.685 |
| adam_lr0.03 | 94.00% | 0.11974022 | 200 | 未达标 | 12935.898 |
| ademamix_lr0.1 | 94.00% | 0.11974381 | 200 | 未达标 | 16524.668 |
| schedule_free_adamw_lr0.1 | 94.00% | 0.11977357 | 200 | 未达标 | 16527.793 |
| sgd_momentum_lr1.0 | 94.00% | 0.11983879 | 200 | 未达标 | 19328.275 |
| schedule_free_adamw_lr0.3 | 94.00% | 0.11986439 | 200 | 未达标 | 16442.858 |
| adagrad_lr1.0 | 94.00% | 0.12111368 | 200 | 未达标 | 17101.289 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
