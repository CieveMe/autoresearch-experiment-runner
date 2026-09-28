# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on the hidden activation. This suite is the tanh [32] suite with ReLU instead, same budget, every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`9ab5e0c2ae117f5b16963ee211dcbbb2d0222206736c446d83ab4f4d185e8045`

## 最优方案

`adamw_constant`：主指标 `test_loss` = **0.105381**，测试准确率 **95.00%**，测试损失 `0.1053807`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant | 95.00% | 0.1053807 | 200 | 17 | 8244.749 |
| adam | 95.00% | 0.1053807 | 200 | 17 | 8269.867 |
| ademamix | 95.00% | 0.105443 | 200 | 17 | 8525.702 |
| adagrad | 95.50% | 0.10546473 | 200 | 12 | 8242.742 |
| schedule_free_adamw | 95.50% | 0.10568892 | 200 | 29 | 8212.518 |
| adamw_cosine | 95.50% | 0.10932659 | 200 | 6 | 8363.924 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
