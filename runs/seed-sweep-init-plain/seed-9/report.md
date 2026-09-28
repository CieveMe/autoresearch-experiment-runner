# AutoResearch Lite 实验报告

- 任务：normalisation/initialisation robustness check, hidden [32], plain fixed-0.05 initialisation (no normalisation): do the two negative results survive?
- 论文：Normalisation/initialisation robustness (AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-normalization-expansion
- 假设：Pre-registered N1-N4 in docs/normalization-init-preregistration.md. Not a new topic: this asks whether the schedule-free architecture effect and AdEMAMix's no-advantage verdict depend on this modelling choice (plain fixed-0.05 initialisation (no normalisation)). Every arm retuned on the same grid as the [32] reference, ten seeds, threshold curves.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`b2609fcb1958faf2d96ec2ce1706034a1a361831f4dae03f4c69c5bda316cf02`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.145935**，测试准确率 **93.00%**，测试损失 `0.14593458`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 93.00% | 0.14593458 | 200 | 13 | 8035.191 |
| adamw_cosine | 93.00% | 0.1460642 | 200 | 8 | 8069.719 |
| adamw_constant | 93.50% | 0.15527532 | 200 | 9 | 8034.668 |
| adam | 93.50% | 0.15527532 | 200 | 9 | 8115.708 |
| ademamix | 93.50% | 0.1554998 | 200 | 9 | 8045.584 |
| adagrad | 93.00% | 0.17395064 | 200 | 17 | 8145.56 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
