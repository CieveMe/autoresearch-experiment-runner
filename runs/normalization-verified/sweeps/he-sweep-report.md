# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], He initialisation (no normalisation): tuning sweep (pre-registered N1-N4)
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on this modelling choice (He initialisation (no normalisation)). Grid identical to the [32] reference so the comparison is controlled; every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`57fce78de1a8f683175cdb2269e0a9ffcb2ec547d8e75a33074533b381404227`

## 最优方案

`ademamix_lr0.3`：主指标 `test_loss` = **0.123066**，测试准确率 **93.00%**，测试损失 `0.12306551`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix_lr0.3 | 93.00% | 0.12306551 | 200 | 未达标 | 7979.005 |
| adamw_constant_lr0.3 | 93.50% | 0.12321829 | 200 | 未达标 | 8192.443 |
| adam_lr0.3 | 93.50% | 0.12321829 | 200 | 未达标 | 8141.617 |
| adagrad_lr1.0 | 93.50% | 0.12455205 | 200 | 未达标 | 8084.937 |
| sgd_momentum_lr1.0 | 93.50% | 0.12459054 | 200 | 未达标 | 8103.949 |
| sgd_momentum_lr0.6 | 93.50% | 0.12466122 | 200 | 未达标 | 8045.09 |
| schedule_free_adamw_lr0.03 | 93.50% | 0.12483386 | 200 | 未达标 | 7981.904 |
| adagrad_lr0.1 | 93.50% | 0.12521105 | 200 | 未达标 | 8162.76 |
| sgd_momentum_lr0.3 | 93.50% | 0.12524622 | 200 | 未达标 | 8028.766 |
| adagrad_lr0.3 | 93.50% | 0.12538941 | 200 | 未达标 | 8184.152 |
| schedule_free_adamw_lr0.1 | 93.50% | 0.12549574 | 200 | 未达标 | 7926.034 |
| ademamix_lr0.03 | 93.50% | 0.12569691 | 200 | 未达标 | 8265.605 |
| adamw_constant_lr0.03 | 93.50% | 0.12572264 | 200 | 未达标 | 8041.952 |
| adam_lr0.03 | 93.50% | 0.12572264 | 200 | 未达标 | 8117.884 |
| adamw_cosine_lr0.03 | 93.50% | 0.12592659 | 200 | 未达标 | 11412.827 |
| schedule_free_adamw_lr0.3 | 93.00% | 0.12610458 | 200 | 未达标 | 7998.401 |
| adamw_constant_lr0.1 | 93.00% | 0.12618744 | 200 | 未达标 | 8128.845 |
| adam_lr0.1 | 93.00% | 0.12618744 | 200 | 未达标 | 8238.522 |
| ademamix_lr0.1 | 93.00% | 0.12621958 | 200 | 未达标 | 8006.87 |
| adamw_cosine_lr0.1 | 93.50% | 0.12673478 | 200 | 未达标 | 10165.765 |
| adamw_cosine_lr0.3 | 92.50% | 0.12722933 | 200 | 未达标 | 7686.554 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
