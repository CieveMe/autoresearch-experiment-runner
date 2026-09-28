# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: tuning sweep (pre-registered A1-A3)
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3 in docs/capacity-expansion-preregistration.md: the schedule-free architecture effect (A1) and AdEMAMix's no-advantage verdict (A2) should not depend on the hidden activation, and neither should the metric trap (A3). Rates must be retuned for ReLU.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`810b229b8216aef98f19d37a78a693af9011de59dad955e946eb816b1cdcfd87`

## 最优方案

`adamw_constant_lr0.01`：主指标 `test_loss` = **0.122127**，测试准确率 **93.50%**，测试损失 `0.12212702`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant_lr0.01 | 93.50% | 0.12212702 | 200 | 未达标 | 8336.859 |
| adam_lr0.01 | 93.50% | 0.12212702 | 200 | 未达标 | 8224.52 |
| ademamix_lr0.01 | 93.50% | 0.12215907 | 200 | 未达标 | 8119.224 |
| schedule_free_adamw_lr0.01 | 93.50% | 0.12221691 | 200 | 未达标 | 8488.104 |
| adagrad_lr0.1 | 93.50% | 0.12227444 | 200 | 未达标 | 8284.374 |
| adamw_cosine_lr0.03 | 93.50% | 0.12228063 | 200 | 未达标 | 8135.869 |
| schedule_free_adamw_lr0.03 | 93.50% | 0.12257026 | 200 | 未达标 | 8324.214 |
| adamw_constant_lr0.03 | 93.50% | 0.12283661 | 200 | 未达标 | 8204.805 |
| adam_lr0.03 | 93.50% | 0.12283661 | 200 | 未达标 | 8179.155 |
| ademamix_lr0.03 | 93.50% | 0.12293117 | 200 | 未达标 | 8157.84 |
| adamw_cosine_lr0.01 | 93.50% | 0.12323159 | 200 | 未达标 | 8047.764 |
| adamw_cosine_lr0.1 | 93.50% | 0.12467221 | 200 | 未达标 | 8209.478 |
| adagrad_lr0.03 | 93.50% | 0.13050896 | 200 | 未达标 | 8741.714 |
| ademamix_lr0.003 | 93.50% | 0.14069128 | 200 | 未达标 | 8087.804 |
| adamw_constant_lr0.003 | 93.50% | 0.1424558 | 200 | 未达标 | 8035.766 |
| adam_lr0.003 | 93.50% | 0.1424558 | 200 | 未达标 | 8108.443 |
| adamw_cosine_lr0.003 | 94.00% | 0.22051877 | 200 | 未达标 | 8272.912 |
| schedule_free_adamw_lr0.003 | 93.50% | 0.22918308 | 200 | 未达标 | 8323.414 |
| adagrad_lr0.01 | 94.00% | 0.25963537 | 200 | 未达标 | 8165.953 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
