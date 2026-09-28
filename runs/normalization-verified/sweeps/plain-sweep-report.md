# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], plain fixed-0.05 initialisation (no normalisation): tuning sweep (pre-registered N1-N4)
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on this modelling choice (plain fixed-0.05 initialisation (no normalisation)). Grid identical to the [32] reference so the comparison is controlled; every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`b6089d044885f22133b71ea70a5cab2bbd24bc431ec977403a3c2231f7e463ce`

## 最优方案

`schedule_free_adamw_lr0.03`：主指标 `test_loss` = **0.122524**，测试准确率 **93.50%**，测试损失 `0.12252436`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw_lr0.03 | 93.50% | 0.12252436 | 200 | 未达标 | 8369.354 |
| adamw_cosine_lr0.03 | 93.50% | 0.12253431 | 200 | 未达标 | 7867.799 |
| adamw_constant_lr0.03 | 93.50% | 0.12255185 | 200 | 未达标 | 8005.941 |
| adam_lr0.03 | 93.50% | 0.12255185 | 200 | 未达标 | 8237.281 |
| ademamix_lr0.03 | 93.50% | 0.12258621 | 200 | 未达标 | 8047.517 |
| adagrad_lr0.1 | 93.50% | 0.12263045 | 200 | 未达标 | 8010.986 |
| sgd_momentum_lr0.3 | 93.50% | 0.12321482 | 200 | 未达标 | 8070.708 |
| adamw_cosine_lr0.1 | 93.50% | 0.12341791 | 200 | 未达标 | 7941.094 |
| schedule_free_adamw_lr0.1 | 93.50% | 0.12350441 | 200 | 未达标 | 7941.612 |
| sgd_momentum_lr0.6 | 93.50% | 0.12352024 | 200 | 未达标 | 8199.077 |
| adagrad_lr0.3 | 93.50% | 0.1235732 | 200 | 未达标 | 8119.337 |
| sgd_momentum_lr1.0 | 93.50% | 0.12386679 | 200 | 未达标 | 8197.206 |
| adagrad_lr1.0 | 93.00% | 0.1241794 | 200 | 未达标 | 8130.49 |
| adamw_constant_lr0.1 | 93.50% | 0.12491925 | 200 | 未达标 | 8189.18 |
| adam_lr0.1 | 93.50% | 0.12491925 | 200 | 未达标 | 8039.036 |
| schedule_free_adamw_lr0.3 | 93.50% | 0.12522362 | 200 | 未达标 | 7870.947 |
| ademamix_lr0.1 | 93.50% | 0.12523009 | 200 | 未达标 | 8108.703 |
| ademamix_lr0.3 | 93.00% | 0.12785982 | 200 | 未达标 | 8273.542 |
| adamw_constant_lr0.3 | 93.00% | 0.12787876 | 200 | 未达标 | 8188.859 |
| adam_lr0.3 | 93.00% | 0.12787876 | 200 | 未达标 | 8029.371 |
| adamw_cosine_lr0.3 | 93.50% | 0.13195066 | 200 | 未达标 | 7993.915 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
