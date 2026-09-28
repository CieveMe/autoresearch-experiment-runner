# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with ReLU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Pre-registered A1-A3: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should not depend on the hidden activation. This suite is the tanh [32] suite with ReLU instead, same budget, every arm retuned.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`cdb71abaa87cc408bdbdee50b1e43587311b8d9c3328e2ba00b39743aba830d7`

## 最优方案

`adamw_cosine`：主指标 `test_loss` = **0.126668**，测试准确率 **93.50%**，测试损失 `0.12666802`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_cosine | 93.50% | 0.12666802 | 128 | 7 | 5267.404 |
| adamw_constant | 94.00% | 0.12755999 | 200 | 21 | 8219.178 |
| adam | 94.00% | 0.12755999 | 200 | 21 | 8184.598 |
| ademamix | 94.00% | 0.12778264 | 200 | 21 | 8245.325 |
| adagrad | 94.00% | 0.12784627 | 200 | 23 | 8274.541 |
| schedule_free_adamw | 94.00% | 0.12914231 | 200 | 44 | 8169.528 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
