# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: tuning sweep (pre-registered A1-A3)
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered predictions as the ReLU run: the schedule-free architecture effect and AdEMAMix's no-advantage verdict should survive a change of hidden activation, and so should the metric trap. Rates are retuned for GELU.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`1e6f0e399e51da03778137d7373595d94dfae9b1222956ed99a230396868b17d`

## 最优方案

`adamw_constant_lr0.01`：主指标 `test_loss` = **0.122540**，测试准确率 **93.50%**，测试损失 `0.1225396`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant_lr0.01 | 93.50% | 0.1225396 | 200 | 未达标 | 9845.517 |
| adam_lr0.01 | 93.50% | 0.1225396 | 200 | 未达标 | 9829.536 |
| adagrad_lr0.1 | 93.50% | 0.12256457 | 200 | 未达标 | 9844.855 |
| ademamix_lr0.01 | 93.50% | 0.12260606 | 200 | 未达标 | 9876.791 |
| schedule_free_adamw_lr0.01 | 93.50% | 0.12260671 | 200 | 未达标 | 9952.401 |
| schedule_free_adamw_lr0.03 | 93.50% | 0.12273812 | 200 | 未达标 | 9811.035 |
| adamw_cosine_lr0.03 | 93.50% | 0.12281536 | 200 | 未达标 | 9687.582 |
| adamw_constant_lr0.03 | 93.50% | 0.12305048 | 200 | 未达标 | 9865.63 |
| adam_lr0.03 | 93.50% | 0.12305048 | 200 | 未达标 | 9941.039 |
| ademamix_lr0.03 | 93.50% | 0.12317559 | 200 | 未达标 | 11184.059 |
| adamw_cosine_lr0.01 | 93.50% | 0.12347276 | 200 | 未达标 | 11570.555 |
| adamw_cosine_lr0.1 | 93.50% | 0.12437396 | 200 | 未达标 | 10906.895 |
| adagrad_lr0.03 | 93.50% | 0.13091245 | 200 | 未达标 | 9906.57 |
| ademamix_lr0.003 | 93.50% | 0.14476121 | 200 | 未达标 | 9767.708 |
| adamw_constant_lr0.003 | 93.50% | 0.14692416 | 200 | 未达标 | 10251.754 |
| adam_lr0.003 | 93.50% | 0.14692416 | 200 | 未达标 | 9841.723 |
| adamw_cosine_lr0.003 | 94.00% | 0.24652878 | 200 | 未达标 | 9994.312 |
| schedule_free_adamw_lr0.003 | 93.50% | 0.25617467 | 200 | 未达标 | 12009.632 |
| adagrad_lr0.01 | 94.50% | 0.2932496 | 200 | 未达标 | 9912.284 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
