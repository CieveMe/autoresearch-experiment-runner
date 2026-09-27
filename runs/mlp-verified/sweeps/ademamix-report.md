# AutoResearch Lite 实验报告

- 任务：learning-rate and warmup sweep for AdEMAMix on the MLP trainer
- 论文：AdEMAMix: A Smarter Learning Rate Schedule for Adam
- 论文标识：arXiv:2409.03137
- 假设：AdEMAMix's slow EMA needs a long horizon; if any model in this repository can show an effect, it is the non-convex MLP rather than the two-parameter logistic head. Every arm, including AdEMAMix's extra warmup-length hyper-parameter, is tuned by the same rule as everywhere else in this repository.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`37420f472f3d2040fb52de67a2011c63ea6ba984ea6d677fe753b059dc75e5e8`

## 最优方案

`ademamix_w45_lr0.3`：主指标 `test_loss` = **0.121241**，测试准确率 **93.50%**，测试损失 `0.12124079`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix_w45_lr0.3 | 93.50% | 0.12124079 | 120 | 未达标 | 1416.814 |
| ademamix_w0_lr0.03 | 93.50% | 0.12394494 | 120 | 未达标 | 1338.788 |
| adamw_lr0.03 | 93.50% | 0.12394506 | 120 | 未达标 | 1382.905 |
| ademamix_w45_lr0.03 | 93.50% | 0.12424134 | 120 | 未达标 | 1330.834 |
| ademamix_w120_lr0.3 | 93.50% | 0.12454467 | 120 | 未达标 | 1314.22 |
| ademamix_w120_lr0.03 | 93.50% | 0.12513752 | 120 | 未达标 | 1360.57 |
| sgd_momentum_lr1.0 | 93.00% | 0.12544684 | 120 | 未达标 | 1330.8 |
| adamw_lr0.1 | 93.50% | 0.12573518 | 120 | 未达标 | 1357.38 |
| ademamix_w0_lr0.1 | 93.50% | 0.12580038 | 120 | 未达标 | 1339.277 |
| ademamix_w0_lr0.3 | 93.00% | 0.12682993 | 120 | 未达标 | 1326.548 |
| adamw_lr0.3 | 93.00% | 0.12697878 | 120 | 未达标 | 1388.26 |
| ademamix_w45_lr0.1 | 93.50% | 0.12804984 | 120 | 未达标 | 1365.068 |
| ademamix_w120_lr0.1 | 93.50% | 0.12923513 | 120 | 未达标 | 1330.878 |
| ademamix_w120_lr0.01 | 93.50% | 0.13544442 | 120 | 未达标 | 1362.917 |
| ademamix_w45_lr0.01 | 93.00% | 0.13838271 | 120 | 未达标 | 1338.129 |
| ademamix_w0_lr0.01 | 93.00% | 0.14134189 | 120 | 未达标 | 1397.934 |
| adamw_lr0.01 | 93.00% | 0.14252384 | 120 | 未达标 | 1408.963 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
