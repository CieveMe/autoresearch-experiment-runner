# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], layernorm on the hidden pre-activations (Xavier init): tuning sweep (pre-registered N1-N4)
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on this modelling choice (layernorm on the hidden pre-activations (Xavier init)). Grid identical to the [32] reference so the comparison is controlled; every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`133fa96eebff6074b2eb8f53007c1a0ef9c701762eec84f6ba298ad29ab97474`

## 最优方案

`sgd_momentum_lr0.3`：主指标 `test_loss` = **0.123197**，测试准确率 **93.00%**，测试损失 `0.12319741`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| sgd_momentum_lr0.3 | 93.00% | 0.12319741 | 200 | 未达标 | 15182.496 |
| sgd_momentum_lr0.6 | 93.00% | 0.12410894 | 200 | 未达标 | 15140.349 |
| schedule_free_adamw_lr0.3 | 93.00% | 0.12414847 | 200 | 未达标 | 15054.236 |
| schedule_free_adamw_lr0.1 | 93.00% | 0.12431813 | 200 | 未达标 | 15707.205 |
| adagrad_lr1.0 | 93.50% | 0.12573881 | 200 | 未达标 | 15352.657 |
| adagrad_lr0.3 | 93.00% | 0.12604799 | 200 | 未达标 | 15948.155 |
| sgd_momentum_lr1.0 | 93.00% | 0.12612413 | 200 | 未达标 | 15132.42 |
| adamw_constant_lr0.3 | 93.50% | 0.1272969 | 200 | 未达标 | 10745.965 |
| adam_lr0.3 | 93.50% | 0.1272969 | 200 | 未达标 | 10809.518 |
| ademamix_lr0.3 | 93.50% | 0.1274158 | 200 | 未达标 | 15642.198 |
| adagrad_lr0.1 | 93.00% | 0.12782436 | 200 | 未达标 | 11418.51 |
| schedule_free_adamw_lr0.03 | 93.00% | 0.12793947 | 200 | 未达标 | 15664.891 |
| ademamix_lr0.03 | 93.50% | 0.12807276 | 200 | 未达标 | 15711.826 |
| adamw_constant_lr0.03 | 93.50% | 0.12812247 | 200 | 未达标 | 11100.089 |
| adam_lr0.03 | 93.50% | 0.12812247 | 200 | 未达标 | 10280.548 |
| ademamix_lr0.1 | 93.50% | 0.12820191 | 200 | 未达标 | 15442.961 |
| adamw_constant_lr0.1 | 93.50% | 0.12821322 | 200 | 未达标 | 10815.352 |
| adam_lr0.1 | 93.50% | 0.12821322 | 200 | 未达标 | 10549.984 |
| adamw_cosine_lr0.3 | 93.50% | 0.12878638 | 200 | 未达标 | 10486.421 |
| adamw_cosine_lr0.03 | 93.50% | 0.12904488 | 200 | 未达标 | 11598.808 |
| adamw_cosine_lr0.1 | 93.00% | 0.12921722 | 200 | 未达标 | 10472.97 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
